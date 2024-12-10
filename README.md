# LTI Provider

A FastAPI-based Learning Tools Interoperability (LTI) 1.3 provider implementation.

## About

LTI Provider is a FastAPI-based implementation of the Learning Tools Interoperability (LTI) 1.3 standard, designed to facilitate seamless integration of external learning tools within Learning Management Systems (LMS) like Canvas. This application supports OIDC (OpenID Connect) for secure authentication and JWT (JSON Web Tokens) for message signing, ensuring a robust and secure connection between the LMS and external tools.

Key Features:

- LTI 1.3 Compliance: Fully compliant with the LTI 1.3 standard, enabling secure tool launches and user authentication.
- Dynamic Configuration: Automatically generates configuration settings for easy integration with Canvas.
- JWT Validation: Utilizes JSON Web Tokens for secure communication and user identity verification.
- CORS Support: Configured to allow requests from Canvas, ensuring smooth operation within the LMS environment.
- Local Development: Easy setup for local testing with Docker and ngrok support.

This project is ideal for developers looking to create and integrate educational tools into existing LMS platforms, enhancing the learning experience for students and educators alike.

Feel free to modify any part of it to better fit your project's vision or specific features!

## Technical Overview

### LTI 1.3 Protocol Flow

1. **OIDC Login Initiation**

   - Canvas initiates login by sending a POST request to `/lti/login`
   - Contains platform info, client_id, and login hints
   - Provider validates and redirects to Canvas auth endpoint

2. **Authentication & Launch**

   - Canvas authenticates and sends signed JWT (id_token) to `/lti/launch`
   - Provider validates JWT signature using platform's public JWK
   - Claims are verified (issuer, audience, expiry, etc.)
   - User is redirected to the tool's interface

3. **Security**
   - Uses RSA key pairs for message signing
   - JWT validation ensures message authenticity
   - OIDC (OpenID Connect) handles identity verification
   - Session management via secure cookies

### Developer Key Configuration Explained

The Developer Key JSON configuration establishes the security and communication parameters between Canvas and your tool:

```json
{
  "title": "Your Tool Name",
  "description": "Your tool description",
  "target_link_uri": "http://your-domain/lti/launch",
  "oidc_initiation_url": "http://your-domain/lti/login",
  "public_jwk_url": "http://your-domain/.well-known/jwks.json",
  "scopes": [
    "https://purl.imsglobal.org/spec/lti-ags/scope/lineitem",
    "https://purl.imsglobal.org/spec/lti-ags/scope/result.readonly",
    "https://purl.imsglobal.org/spec/lti-nrps/scope/contextmembership.readonly"
  ]
}
```

1. **Authentication Endpoints**

   - `target_link_uri`: Entry point for tool launches
   - `oidc_initiation_url`: Handles OIDC login flow initiation
   - `public_jwk_url`: Provides RSA public keys for JWT verification

2. **Security Flow**

   - Canvas initiates OIDC login via `oidc_initiation_url`
   - Tool validates request and redirects to Canvas
   - Canvas sends authenticated launch to `target_link_uri`
   - Tool verifies JWT using keys from `public_jwk_url`

3. **Scopes**

   - `lineitem`: Create/manage gradebook columns
   - `result.readonly`: Read student results
   - `contextmembership.readonly`: Access course roster

4. **JWT Claims**
   The launch JWT includes:

   - `iss`: Canvas instance URL
   - `aud`: Your Client ID
   - `sub`: User identifier
   - `https://purl.imsglobal.org/spec/lti/claim/...`: LTI-specific data

5. **Security Considerations**
   - All URLs must use HTTPS in production
   - JWKs must be regularly rotated
   - Nonce validation prevents replay attacks
   - State parameter ensures request continuity

## API Endpoints

### LTI Configuration

- `GET /lti/config`
  - Returns tool configuration for Canvas integration
  - Defines scopes, URLs, and placement settings
  - Used during tool installation in Canvas

### OIDC Flow

- `POST /lti/login`

  - Handles OIDC login initiation
  - Validates required parameters
  - Redirects to Canvas authorization endpoint

- `POST /lti/launch`
  - Main entry point for tool launch
  - Validates JWT token and claims
  - Establishes user session
  - Redirects to tool interface

### Tool Registration

- `GET /lti/register`

  - Returns LTI 2.0 registration configuration
  - Defines tool capabilities and settings

- `POST /lti/register`
  - Handles registration callback from Canvas
  - Stores deployment information

### Security Endpoints

- `GET /.well-known/jwks.json`
  - Serves public JWK for token verification
  - Used by Canvas to verify tool messages

## Local Development Setup

1. **Prerequisites**

   ```bash
   - Python 3.12+
   - PostgreSQL
   - Poetry
   ```

2. **Installation**

   ```bash
   git clone <repository>
   cd lti-provider
   poetry install
   ```

3. **Environment Configuration**

   ```bash
   cp .env.example .env
   # Edit .env with your settings:
   # - Database URL
   # - LTI credentials
   # - Tool URLs
   ```

4. **Database Setup**

   ```bash
   # The application will automatically create tables on startup
   ```

5. **Run Development Server**

   ```bash
   poetry run uvicorn app.main:app --reload
   ```

6. **Canvas Configuration**
   - Add Developer Key in Canvas
   - Configure with your tool's URLs
   - Install in desired course

## Simplified Flow

1. Teacher adds tool to Canvas course
2. Student clicks tool link
3. Canvas sends login request to tool
4. Tool validates and redirects to Canvas
5. Canvas authenticates and launches tool
6. Tool verifies launch and shows interface

## Folder Structure

```markdown
lti-provider/
├── app/
│ ├── main.py
│ ├── config.py
│ ├── models/
│ │ ├── database.py
│ │ └── lti.py
│ ├── routes/
│ │ └── lti.py
│ └── services/
│ └── lti.py
├── pyproject.toml
├── poetry.lock
├── .tool-versions
└── .env.example
```

## Canvas Integration Setup

### 1. Create Developer Key

1. Access Canvas Admin settings
2. Navigate to "Developer Keys"
3. Click "+ Developer Key" and select "LTI Key"
4. Configure the key:

   You can get the configuration by making a GET request to:

   ```bash
   curl http://your-domain/lti/config
   ```

   Which returns:

   ```json
   {
     "title": "Your Tool Name",
     "description": "Your tool description",
     "target_link_uri": "http://your-domain/lti/launch",
     "oidc_initiation_url": "http://your-domain/lti/login",
     "public_jwk_url": "http://your-domain/.well-known/jwks.json",
     "scopes": [
       "https://purl.imsglobal.org/spec/lti-ags/scope/lineitem",
       "https://purl.imsglobal.org/spec/lti-ags/scope/result.readonly",
       "https://purl.imsglobal.org/spec/lti-nrps/scope/contextmembership.readonly"
     ],
     "extensions": [
       {
         "platform": "canvas.instructure.com",
         "settings": {
           "platform": "canvas.instructure.com",
           "text": "Your Tool Name",
           "placements": [
             {
               "placement": "course_navigation",
               "enabled": true,
               "default": "enabled",
               "message_type": "LtiResourceLinkRequest",
               "target_link_uri": "http://your-domain/lti/launch"
             }
           ]
         }
       }
     ]
   }
   ```

   Copy this configuration into the Developer Key settings in Canvas.

5. Save and enable the Developer Key
6. Note the Client ID (will be used in .env)

### 2. Configure Environment Variables

Update your `.env` file with the Developer Key information:

```env
# LTI Settings
LTI_CLIENT_ID="10000000000001"        # From Developer Key
LTI_DEPLOYMENT_ID="1:df26f9c414..."   # Generated during course installation
LTI_ISSUER="http://canvas.domain"     # Your Canvas instance URL

# Tool Settings
TOOL_URL="http://your-domain"
TOOL_LOGIN_URL="http://your-domain/lti/login"
TOOL_LAUNCH_URL="http://your-domain/lti/launch"
TOOL_REDIRECT_URL="http://your-domain/home"

# Database
DATABASE_URL="postgresql://user:pass@localhost:5432/lti_db"
```

### 3. Install in Course

1. Go to Course Settings
2. Select "Apps" tab
3. Click "+ App"
4. Choose "By Client ID"
5. Enter the Client ID from Developer Key
6. Submit and authorize the installation
7. The tool will appear in course navigation

### 4. Testing the Integration

1. **Development Environment**

   ```bash
   # Start your development server
   poetry run uvicorn app.main:app --reload

   # For local testing, use ngrok to expose your server
   ngrok http 8000
   ```

2. **Update Canvas Configuration**

   - If testing locally, update Developer Key URLs with ngrok domain
   - Update .env with corresponding URLs

3. **Verify Installation**
   - Access course as instructor
   - Tool should appear in course navigation
   - Click to test launch flow
   - Check application logs for debugging
