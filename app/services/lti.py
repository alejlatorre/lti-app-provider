from jose import jwt, jwk
from fastapi import HTTPException
import httpx
from ..config import settings
from ..models.lti import LTIDeployment, LTINonce
import time
import secrets

class LTIService:
    async def validate_login(self, form_data: dict) -> dict:
        """Validate the OIDC login initiation request"""
        required_params = [
            'iss', 'target_link_uri', 'login_hint',
            'lti_message_hint', 'client_id'
        ]
        
        for param in required_params:
            if param not in form_data:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing required parameter: {param}"
                )
        
        return {
            'state': secrets.token_urlsafe(),
            'nonce': secrets.token_urlsafe(),
            'prompt': 'none',
            'response_type': 'id_token',
            'response_mode': 'form_post',
            'scope': 'openid',
            'login_hint': form_data['login_hint'],
            'lti_message_hint': form_data['lti_message_hint'],
            'client_id': form_data['client_id'],
            'redirect_uri': settings.TOOL_LAUNCH_URL
        }
    
    async def get_auth_redirect_url(self, params: dict) -> str:
        """Generate the authorization redirect URL"""
        query_params = "&".join([
            f"{k}={v}" for k, v in params.items()
        ])
        return f"{settings.LTI_AUTH_TOKEN_URL}?{query_params}"
    
    async def validate_launch(self, form_data: dict) -> dict:
        """Validate the LTI resource launch"""
        if 'id_token' not in form_data:
            raise HTTPException(
                status_code=400,
                detail="Missing id_token"
            )
            
        # Decode and validate the JWT token
        try:
            # Fetch JWKs from Canvas
            async with httpx.AsyncClient() as client:
                response = await client.get(settings.LTI_JWK_URL)
                jwks = response.json()
            
            # Verify the token
            token = jwt.decode(
                form_data['id_token'],
                jwks,
                algorithms=['RS256'],
                audience=settings.LTI_CLIENT_ID
            )
            
            # Validate the token claims
            self._validate_token_claims(token)
            
            return token
            
        except Exception as e:
            raise HTTPException(
                status_code=401,
                detail=f"Invalid launch request: {str(e)}"
            )
    
    def _validate_token_claims(self, token: dict):
        """Validate the required token claims"""
        required_claims = [
            'iss', 'sub', 'aud', 'exp', 'iat', 'nonce',
            'https://purl.imsglobal.org/spec/lti/claim/message_type',
            'https://purl.imsglobal.org/spec/lti/claim/version',
            'https://purl.imsglobal.org/spec/lti/claim/deployment_id'
        ]
        
        for claim in required_claims:
            if claim not in token:
                raise ValueError(f"Missing required claim: {claim}") 