import logging

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.database import get_session
from app.models.lti import LTIDeployment
from app.services.lti import LTIService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
lti_service = LTIService()


@router.get("/lti/config")
async def lti_config():
    """Return the LTI configuration for Canvas"""
    return {
        "title": settings.APP_NAME,
        "description": settings.TOOL_DESCRIPTION,
        "scopes": [
            "https://purl.imsglobal.org/spec/lti-ags/scope/lineitem",
            "https://purl.imsglobal.org/spec/lti-ags/scope/result.readonly",
            "https://purl.imsglobal.org/spec/lti-nrps/scope/contextmembership.readonly",
        ],
        "public_jwk_url": f"{settings.TOOL_URL}/.well-known/jwks.json",
        "target_link_uri": settings.TOOL_LAUNCH_URL,
        "oidc_initiation_url": settings.TOOL_LOGIN_URL,
        "extensions": [
            {
                "platform": "canvas.instructure.com",
                "settings": {
                    "platform": "canvas.instructure.com",
                    "text": settings.APP_NAME,
                    "icon_url": settings.TOOL_ICON_URL,
                    "placements": [
                        {
                            "placement": "course_navigation",
                            "enabled": True,
                            "default": "enabled",
                            "text": settings.APP_NAME,
                            "message_type": "LtiResourceLinkRequest",
                            "target_link_uri": settings.TOOL_LAUNCH_URL,
                        }
                    ],
                },
            }
        ],
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

    logger.info(launch_data)

    return RedirectResponse(
        url=f"{settings.TOOL_REDIRECT_URL}?session={launch_data.get('sub')}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/lti/register")
async def lti_register():
    """Return the LTI 2.0 registration configuration"""
    return {
        "tool_proxy": {
            "@context": ["http://purl.imsglobal.org/ctx/lti/v2/ToolProxy"],
            "@type": "ToolProxy",
            "lti_version": "LTI-2p0",
            "tool_proxy_guid": settings.TOOL_PROXY_GUID,
            "tool_consumer_profile": "http://lms.example.com/profile/download",
            "tool_profile": {
                "lti_version": "LTI-2p0",
                "product_instance": {
                    "guid": settings.TOOL_PROXY_GUID,
                    "product_info": {
                        "product_name": {"default_value": settings.APP_NAME},
                        "description": {"default_value": settings.TOOL_DESCRIPTION},
                        "technical_description": {
                            "default_value": "LTI 2.0 Tool Provider"
                        },
                        "product_version": "1.0",
                        "product_family": {
                            "code": settings.TOOL_VENDOR_CODE,
                            "vendor": {
                                "code": settings.TOOL_VENDOR_CODE,
                                "vendor_name": {
                                    "default_value": settings.TOOL_VENDOR_NAME
                                },
                                "description": {
                                    "default_value": settings.TOOL_VENDOR_DESCRIPTION
                                },
                                "website": settings.TOOL_VENDOR_URL,
                                "contact": {"email": settings.TOOL_CONTACT_EMAIL},
                            },
                        },
                    },
                },
                "resource_handler": [
                    {
                        "@type": "ResourceHandler",
                        "resource_type": {"code": settings.TOOL_CODE},
                        "resource_name": {"default_value": settings.APP_NAME},
                        "message": [
                            {
                                "message_type": "basic-lti-launch-request",
                                "path": "/lti/launch",
                                "parameter": [
                                    {
                                        "name": "launch_presentation_document_target",
                                        "fixed": "iframe",
                                    }
                                ],
                            }
                        ],
                    }
                ],
                "base_url_choice": [
                    {
                        "default_base_url": settings.TOOL_URL,
                        "selector": {"applies_to": ["MessageHandler"]},
                    }
                ],
                "service_offered": [],
            },
            "security_contract": {
                "tool_service": [],
                "context_type": ["CourseSection"],
                "message_security": [
                    {
                        "message_type": "basic-lti-launch-request",
                        "tool_message_security_profile": {
                            "security_profile_name": "lti_oauth_hash_message_security"
                        },
                    }
                ],
            },
        }
    }


@router.post("/lti/register")
async def handle_registration(
    request: Request, db: AsyncSession = Depends(get_session)
):
    """Handle the LTI 2.0 registration request from Canvas"""
    form_data = await request.form()

    # Store the registration data
    deployment = LTIDeployment(
        client_id=form_data.get("reg_key", ""),
        deployment_id=form_data.get("reg_password", ""),
        platform_issuer=form_data.get("tc_profile_url", ""),
    )

    db.add(deployment)
    await db.commit()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"status": "success", "message": "Registration successful"},
    )


@router.get("/.well-known/jwks.json")
async def get_jwks():
    """Serve the public JWK set"""
    jwk = lti_service.get_public_jwk()
    return {"keys": [jwk]}
