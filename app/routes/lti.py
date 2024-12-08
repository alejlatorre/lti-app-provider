from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from app.config import settings
from app.services.lti import LTIService

router = APIRouter()
lti_service = LTIService()


@router.get("/lti/config")
async def lti_config():
    """Return the LTI configuration for Canvas"""
    return {
        "title": settings.APP_NAME,
        "scopes": [
            "https://purl.imsglobal.org/spec/lti-ags/scope/lineitem",
            "https://purl.imsglobal.org/spec/lti-ags/scope/result.readonly",
            "https://purl.imsglobal.org/spec/lti-nrps/scope/contextmembership.readonly",
        ],
        "public_jwk_url": f"{settings.TOOL_URL}/.well-known/jwks.json",
        "target_link_uri": settings.TOOL_LAUNCH_URL,
        "oidc_initiation_url": settings.TOOL_LOGIN_URL,
        "extensions": [],
    }


@router.post("/lti/login")
async def lti_login(request: Request):
    """Handle the OIDC login initiation"""
    form_data = await request.form()

    # Validate the login request
    login_params = await lti_service.validate_login(form_data)

    # Generate the authorization redirect URL
    auth_url = await lti_service.get_auth_redirect_url(login_params)

    return RedirectResponse(url=auth_url)


@router.post("/lti/launch")
async def lti_launch(request: Request):
    """Handle the LTI resource launch"""
    form_data = await request.form()

    # Validate the launch request
    launch_data = await lti_service.validate_launch(form_data)

    # Here you would typically:
    # 1. Create or get a user session
    # 2. Redirect to your actual application
    # 3. Pass any necessary context from the launch

    return RedirectResponse(
        url=f"{settings.TOOL_URL}/app?session={launch_data.session_id}"
    )
