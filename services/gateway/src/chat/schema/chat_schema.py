from pydantic import BaseModel, Field
class ChatRequest(BaseModel):
    message:str =Field(
        ...,
        description="The message to be sent to the chat service",
        min_length=1,
    )
class ChatResponse(BaseModel):
    response:str 
    