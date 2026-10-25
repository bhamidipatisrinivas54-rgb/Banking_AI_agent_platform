# Banking AI Agent Platform

An AI-powered banking assistant built with FastAPI, PostgreSQL, Retrieval-Augmented Generation (RAG), and the Model Context Protocol (MCP). The platform combines banking policy retrieval with tool-based interactions for mock account balances and recent transactions.

## Features

- **API Gateway:** Entry point for chat requests and health checks.
- **AI Agent:** Uses an LLM to interpret user questions and decide when to call tools.
- **RAG Service:** Retrieves relevant information from banking policy documents.
- **MCP Server:** Exposes banking tools to the agent.
- **PostgreSQL + pgvector:** Stores chat history and document embeddings.
- **Database migrations:** Uses Alembic to manage schema changes.
- **LLM integration:** Uses Groq for language model inference.

> **Disclaimer:** This is a learning/demo project. Banking account balances and transactions are mock data. Do not use it with real customer data or for production banking without appropriate authentication, authorization, security controls, and testing.

## Architecture

```text
Client
  |
  v
Gateway API (:8000)
  |
  v
Agent Service (:8001)
  |                  |
  v                  v
RAG Service (:8002)  MCP Server (:8003)
  |                  |
  v                  v
PostgreSQL + pgvector
  |
  +-- Chat history
  +-- Document chunks and embeddings
```

The agent can retrieve policy information through the RAG service and invoke banking tools through the MCP server. The exact tool used depends on the user's request.

## Technology Stack

- Python 3.13
- FastAPI and Uvicorn
- PostgreSQL and pgvector
- SQLAlchemy and Alembic
- Groq API
- MCP Python SDK
- HTTPX
- Sentence Transformers

## Project Structure

```text
Banking_AI_agent_platform/
├── alembic/                 # Database migrations
├── alembic.ini              # Alembic configuration
├── compose.yaml             # PostgreSQL development setup
├── data/
│   └── documents/           # Sample banking policy document
├── database/                # Database models and connections
├── services/
│   ├── gateway/             # Gateway API
│   ├── agent/               # Agent and tool orchestration
│   ├── rag/                 # Document retrieval and generation
│   └── mcp_server/          # Banking tools exposed through MCP
├── .env.example             # Environment variable template
├── .gitignore
└── README.md
```

## Prerequisites

- Python 3.13
- Docker Desktop
- A Groq API key
- Git

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Banking_AI_agent_platform.git
cd Banking_AI_agent_platform
```

Replace `YOUR_USERNAME` with the GitHub account that hosts the repository.

### 2. Create a virtual environment

On macOS:

```bash
python3.13 -m venv .venv_mac
source .venv_mac/bin/activate
python --version
```

### 3. Install dependencies

Install the dependencies required by the project. If a root `requirements.txt` or `pyproject.toml` is added later, use that file as the source of truth.

The packages used by the services include FastAPI, Uvicorn, SQLAlchemy, Alembic, psycopg, HTTPX, Groq, MCP, and Sentence Transformers. Check the imports in each service before installing packages.

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and set your own Groq API key and local database credentials. Never commit `.env` or share your API key.

Ensure `DATABASE_URL`, `AGENT_SERVICE_URL`, `RAG_SERVICE_URL`, `GROQ_API_KEY`, and `GROQ_MODEL` match your local configuration.

### 5. Start PostgreSQL

```bash
docker compose up -d postgres
docker compose ps
```

The database is available locally on port `5432`. The Compose file uses a persistent Docker volume for database data.

### 6. Apply database migrations

With the virtual environment activated and `DATABASE_URL` configured:

```bash
alembic upgrade head
alembic current
```

### 7. Ingest the policy document

Ensure the sample policy PDF is present at the path expected by the RAG ingestion code. Review `services/rag/src/ingestion/run_ingestion.py` for the exact command and configuration before running ingestion.

### 8. Start the services

Open a separate terminal for each service. Activate the same virtual environment in each terminal and run commands from the project root.

Gateway:

```bash
uvicorn services.gateway.src.main:app --host 127.0.0.1 --port 8000 --reload
```

Agent:

```bash
uvicorn services.agent.src.main:app --host 127.0.0.1 --port 8001 --reload
```

RAG:

```bash
uvicorn services.rag.src.main:app --host 127.0.0.1 --port 8002 --reload
```

MCP server:

```bash
uvicorn services.mcp_server.src.main:app --host 127.0.0.1 --port 8003 --reload
```

**Note:** These commands assume each module exposes a FastAPI `app` object and supports running from the project root. Confirm the MCP server's actual transport and startup requirements in its source code; it may need to be started using a different command.

## API and Testing

- Gateway base URL: `http://127.0.0.1:8000`
- Agent base URL: `http://127.0.0.1:8001`
- RAG base URL: `http://127.0.0.1:8002`
- MCP endpoint: `http://127.0.0.1:8003/mcp`

When a FastAPI service is running, open its `/docs` endpoint to inspect the available routes, if Swagger documentation is enabled.

Example:

```text
http://127.0.0.1:8000/docs
```

Use the test scripts in the service directories to test MCP connectivity, retrieval, and LLM behavior. Run tests only after the required environment variables and dependent services are configured.

## Security Notes

- Never commit `.env`, API keys, database dumps, or credentials.
- The included account and transaction tools use mock data.
- Do not expose development services publicly without appropriate security controls.
- Use proper authentication, authorization, input validation, and secret management before any production use.

## Future Improvements

- Add dependency lock files and reproducible installation instructions.
- Add automated unit and integration tests.
- Add service health checks and structured logging.
- Add authentication and authorization.
- Add Dockerfiles and a complete multi-service Compose deployment.

## License

No license has been specified yet. Add a license only after deciding how you want others to use and redistribute this project.
