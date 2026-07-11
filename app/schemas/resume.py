from pydantic import BaseModel


class ResumeUploadResponse(BaseModel):
    filename: str
    pages: int
    character_count: int
    extracted_text: str