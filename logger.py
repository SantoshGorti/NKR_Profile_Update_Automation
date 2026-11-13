"""
Logging module for Naukri profile automation.
Provides structured logging to file and console with error tracking and screenshots on failure.
"""

import logging
import json
from datetime import datetime
from pathlib import Path
from config import LOG_LEVEL, LOG_FILE, EXECUTION_LOG_FILE, SCREENSHOTS_DIR


class ExecutionLogger:
    """Structured execution log manager for tracking automation runs."""

    def __init__(self):
        """Initialize the execution logger."""
        self.execution_log_file = EXECUTION_LOG_FILE
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Ensure the execution log file exists."""
        if not self.execution_log_file.exists():
            with open(self.execution_log_file, "w") as f:
                json.dump([], f, indent=2)

    def log_execution(
        self,
        status,
        headline=None,
        verification_result=None,
        error_message=None,
        screenshot_path=None,
    ):
        """
        Log an execution record to JSON.

        Args:
            status (str): SUCCESS or FAILURE
            headline (str): The headline that was used
            verification_result (bool): Whether the update was verified
            error_message (str): Error details if failed
            screenshot_path (str): Path to screenshot if captured
        """
        try:
            # Load existing logs
            logs = []
            if self.execution_log_file.exists():
                with open(self.execution_log_file, "r") as f:
                    logs = json.load(f)

            # Create new log entry
            entry = {
                "timestamp": datetime.now().isoformat(),
                "status": status,
                "headline": headline,
                "verification_result": verification_result,
                "error_message": error_message,
                "screenshot_path": screenshot_path,
            }

            logs.append(entry)

            # Write back to file
            with open(self.execution_log_file, "w") as f:
                json.dump(logs, f, indent=2)

        except Exception as e:
            logging.error(f"Error writing to execution log: {str(e)}")

    @staticmethod
    def get_last_used_headline():
        """
        Get the headline used in the last successful execution.

        Returns:
            str or None: The last used headline, or None if no previous execution.
        """
        try:
            if not EXECUTION_LOG_FILE.exists():
                return None

            with open(EXECUTION_LOG_FILE, "r") as f:
                logs = json.load(f)

            # Find last successful execution with a headline
            for log in reversed(logs):
                if log["status"] == "SUCCESS" and log.get("headline"):
                    return log["headline"]

            return None
        except Exception:
            return None


def setup_logging():
    """Configure logging to file and console."""
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, LOG_LEVEL))

    # Remove existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # File handler
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(getattr(logging, LOG_LEVEL))

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOG_LEVEL))

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def get_logger(name):
    """
    Get a logger instance with the given name.

    Args:
        name (str): Logger name (usually __name__)

    Returns:
        Logger: Configured logger instance
    """
    return logging.getLogger(name)


def take_screenshot(driver, failure_name="failure"):
    """
    Take a screenshot on failure for debugging.

    Args:
        driver: Selenium WebDriver instance
        failure_name (str): Name for the screenshot

    Returns:
        str: Path to the saved screenshot or None
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_filename = f"{failure_name}_{timestamp}.png"
        screenshot_path = SCREENSHOTS_DIR / screenshot_filename

        driver.save_screenshot(str(screenshot_path))
        logger = get_logger(__name__)
        logger.info(f"✓ Screenshot saved: {screenshot_path}")
        return str(screenshot_path)

    except Exception as e:
        logger = get_logger(__name__)
        logger.error(f"Failed to take screenshot: {str(e)}")
        return None


# Initialize logging
setup_logging()
