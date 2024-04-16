# Standard imports
import os

# Load dotenv
from dotenv import load_dotenv

print(os.getcwd())
DOTENV_FILE = os.path.join("app", "config", os.getenv('BUILD', 'dev'), ".env")
DOTENV_LOADED = load_dotenv(DOTENV_FILE)

# Third party imports
from fastapi import FastAPI
from app.infrastructure.utils import custom_logs
from app.presentation.api.v1.endpoints import router_orchestator


# Initialize logger
logger = custom_logs.getLogger(__name__)
logger.info(f"dotenv loaded: {DOTENV_LOADED} at {DOTENV_FILE}")

# Initialize FastAPI app
app = FastAPI()

# Include Routers
app.include_router(router_orchestator)


if __name__ == "__main__":

    # Run the FastAPI application
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9003)
