from loguru import logger
import sys

# Configure Loguru for console output and file logging
logger.remove()
logger.add(sys.stdout, format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
logger.add("rapports/execution_agent.log", rotation="5 MB", level="INFO")