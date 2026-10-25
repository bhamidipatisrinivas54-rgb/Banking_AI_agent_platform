
import asyncio

from services.rag.src.generation.llm_service import generate_answer


async def main():
    question = "What should I do if my banking complaint is not resolved?"

    context = """
    Example policy context:
    Customers can raise complaints through the bank's designated
    grievance channels. The bank should communicate the process
    for escalating complaints and the expected response timeline.
    """

    answer = await generate_answer(question, context)

    print("\nQuestion:", question)
    print("\nGenerated answer:\n", answer)


if __name__ == "__main__":
    asyncio.run(main())
