from pydantic import BaseModel, field_validator

VALID_STATUSES = {"Pending", "In Progress", "Resolved"}

class ComplaintCreate(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Complaint text cannot be empty")
        return v.strip()

class StatusUpdate(BaseModel):
    status: str

    @field_validator("status")
    @classmethod
    def valid_status(cls, v):
        if v not in VALID_STATUSES:
            raise ValueError(f"Status must be one of {VALID_STATUSES}")
        return v
