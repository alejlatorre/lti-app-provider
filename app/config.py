from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    DEBUG_MODE: bool

    # Database settings
    DATABASE_URL: str

    # LTI settings
    LTI_CLIENT_ID: str
    LTI_DEPLOYMENT_ID: str
    LTI_ISSUER: str
    LTI_AUTH_TOKEN_URL: str
    LTI_JWK_URL: str

    # Your application settings
    TOOL_URL: str
    TOOL_LOGIN_URL: str
    TOOL_LAUNCH_URL: str
    TOOL_REDIRECT_URL: str
    TOOL_CODE: str

    # LTI 2.0 Registration settings
    TOOL_PROXY_GUID: str = "test_ai_tool"  # Unique identifier for your tool
    TOOL_PROXY_URL: str = ""  # Will be ided by Canvas during registration
    REGISTRATION_PASSWORD: str = ""  # Will be set during registration

    # Additional tool settings
    TOOL_DESCRIPTION: str
    TOOL_CONTACT_EMAIL: str = "support@test.dev"
    TOOL_VENDOR_CODE: str = "test"
    TOOL_VENDOR_NAME: str = "test"
    TOOL_VENDOR_DESCRIPTION: str = "test"
    TOOL_VENDOR_URL: str = "https://test.dev"

    # Tool UI settings
    TOOL_ICON_URL: str = ""  # URL to your tool's icon (optional)

    # Security settings
    SECRET_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
