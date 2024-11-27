"""Configuration module for environment and logging setup.

This module handles loading environment variables and configuring logging.
"""

from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
