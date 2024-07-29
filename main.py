import threading
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from webhook import webhook_router
from routes import auth_router, engagements_router, sessions_router, subcriptions_router,attachment_router
import os
from fastapi.staticfiles import StaticFiles



# Initialize a app component for docket to run a container
app = None

# creating security middleware with headers
class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Add custom headers here
        response = await call_next(request)
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["X-Frame-Options"] = "DENY"
        return response

def run_uv_app():
    # Create a FastAPI instance
    global app

    app = FastAPI()

    #attachments_server_path = os.getenv('file_server_path')
    # Configure FastAPI to serve static files from the "client/static" directory and adding extra secuity
    app.mount("/static", StaticFiles(directory="client/static"), name="static")
    #app.mount("/attachments", StaticFiles(directory=attachments_server_path), name="static")

    # Add the custom middleware to your FastAPI app
    app.add_middleware(CustomMiddleware)

    # include application routers here
    app.include_router(webhook_router, prefix="/webhook")
    app.include_router(auth_router, prefix="/api")
    app.include_router(subcriptions_router, prefix="/api")
    app.include_router(engagements_router, prefix="/api")
    app.include_router(sessions_router, prefix="/api")
    app.include_router(attachment_router, prefix='/attachments')

    # Add CORS middleware to allow all origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    uvicorn.run(app, host='0.0.0.0', port=9000,
                ssl_keyfile=os.getenv("ssl_keyfile"),
                ssl_certfile=os.getenv("ssl_certfile"))


if __name__ == '__main__':
    uvicorn_thread = threading.Thread(target=run_uv_app)
    uvicorn_thread.start()

