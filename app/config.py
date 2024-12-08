from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "LTI Provider"
    DEBUG_MODE: bool = False
    
    # Database settings
    DATABASE_URL: str
    
    # LTI settings
    LTI_CLIENT_ID: str
    LTI_DEPLOYMENT_ID: str
    LTI_ISSUER: str = "https://canvas.instructure.com"
    LTI_AUTH_TOKEN_URL: str = "https://canvas.instructure.com/api/lti/authorize_redirect"
    LTI_JWK_URL: str = "https://canvas.instructure.com/api/lti/security/jwks"
    
    # Your application settings
    TOOL_URL: str
    TOOL_LOGIN_URL: str
    TOOL_LAUNCH_URL: str
    TOOL_REDIRECT_URL: str
    
    class Config:
        env_file = ".env"

settings = Settings() 