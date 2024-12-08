from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


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
