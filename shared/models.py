from pydantic import BaseModel, Field

class FileMetadata(BaseModel):
    """
    The format every file metadata has to have
    """
    file_path: str = Field(..., description="The file path in the local computer")
    file_name: str = Field(..., description="The name of the file")
    file_size: int = Field(gt=0, description="The size of the file in bytes")
    file_format: str = Field(..., description="The format of the file")
    created_at: str = Field(..., description="The time when the file was created at, Full format")
