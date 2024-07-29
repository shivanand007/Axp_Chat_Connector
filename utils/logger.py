from loguru import logger
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()


# Configure Loguru to write logs to a file
logger.add(os.getenv("log_file_path"), rotation="500 MB", retention="10 days", level="INFO")

