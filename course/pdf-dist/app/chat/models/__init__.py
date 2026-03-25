from pydantic import BaseModel, ConfigDict


class Metadata(BaseModel):
    model_config = ConfigDict(extra="allow")

    conversation_id: str
    user_id: str
    pdf_id: str


class ChatArgs(BaseModel):
    model_config = ConfigDict(extra="allow")

    conversation_id: str
    pdf_id: str
    metadata: Metadata
    streaming: bool
