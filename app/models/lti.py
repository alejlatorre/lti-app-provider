from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class LTIDeployment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: str = Field(index=True)
    deployment_id: str
    platform_issuer: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
class LTINonce(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nonce: str = Field(index=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow) 