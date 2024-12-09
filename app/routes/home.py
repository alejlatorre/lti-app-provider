from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/home", response_class=HTMLResponse)
async def home_app(request: Request):
    """Render the application page"""
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Test LTI Tool</title>
        </head>
        <body>
            <h1>uDocz POC LTI Tool</h1>
            <div id="app">
                <!-- Your LTI interface will go here -->
                <p>Successfully logged in to uDocz POC LTI Tool!</p>
            </div>
        </body>
    </html>
    """
