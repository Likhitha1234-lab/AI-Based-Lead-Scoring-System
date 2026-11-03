from pydantic import BaseModel, EmailStr
from typing import Optional


class LeadInput(BaseModel):

    name: str
    company_name: str
    website: Optional[str] = None
    job_title: str
    industry: str
    company_location: str
    company_size: str
    lead_source: str
    requirement: str
    email: EmailStr
    phone: Optional[str] = None