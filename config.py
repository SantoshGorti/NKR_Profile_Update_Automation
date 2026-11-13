"""
Configuration module for Naukri Profile Automation.
Loads settings from environment variables and config files.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project root directory
PROJECT_ROOT = Path(__file__).parent.resolve()

# Directories
LOGS_DIR = PROJECT_ROOT / "logs"
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
CONFIG_DIR = PROJECT_ROOT / "config"

# Ensure directories exist
LOGS_DIR.mkdir(exist_ok=True)
SCREENSHOTS_DIR.mkdir(exist_ok=True)
CONFIG_DIR.mkdir(exist_ok=True)

# ============== Naukri Credentials ==============
NAUKRI_EMAIL = os.getenv("NAUKRI_EMAIL", "").strip()
NAUKRI_PASSWORD = os.getenv("NAUKRI_PASSWORD", "").strip()

if not NAUKRI_EMAIL or not NAUKRI_PASSWORD:
    raise ValueError(
        "ERROR: NAUKRI_EMAIL and NAUKRI_PASSWORD must be set in .env file. "
        "Copy .env.example to .env and update with your credentials."
    )

# ============== Naukri URLs ==============
NAUKRI_HOME_URL = "https://www.naukri.com/"
NAUKRI_LOGIN_PAGE_URL = "https://login.naukri.com/nLogin/Login.php"
NAUKRI_LOGGED_IN_HOMEPAGE = "https://www.naukri.com/mnjuser/homepage"
NAUKRI_PROFILE_URL = "https://www.naukri.com/mnjuser/profile"

# ============== Browser Configuration ==============
HEADLESS_MODE = os.getenv("HEADLESS_MODE", "False").lower() == "true"
BROWSER_TIMEOUT = int(os.getenv("BROWSER_TIMEOUT", "15"))
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 30

# ============== Logging Configuration ==============
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = LOGS_DIR / "naukri_automation.log"
EXECUTION_LOG_FILE = LOGS_DIR / "execution_log.json"

# ============== Scheduling Configuration ==============
SCHEDULE_INTERVAL_HOURS = 1
SCHEDULE_INTERVAL_MINUTES = 0

# ============== Retry Configuration ==============
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 5

# ============== Element Locators ==============
# These are configurable and should be updated if Naukri changes their page structure
LOCATORS = {
    # Homepage login button
    "login_button_homepage": ("id", "login_Layer"),
    
    # Login page elements
    "login_email_field": ("xpath", "//input[contains(@placeholder, 'Email') or @name='usernameField' or @id='usernameField']"),
    "login_password_field": ("xpath", "//input[@type='password' and @placeholder='Enter your password']"),
    "login_button": ("xpath", "//button[contains(text(), 'Login') or contains(@class, 'loginButton') or @type='submit']"),
    
    # Profile page - Resume headline elements
    "edit_headline_button": ("xpath", "//span[@class='edit icon' and @role='button']"),
    "resume_headline_textarea": ("id", "resumeHeadlineTxt"),
    "resume_headline_field": ("xpath", "//textarea[@id='resumeHeadlineTxt' or @name='resumeHeadline']"),
    
    # Save operation
    "save_button": ("xpath", "//button[@class='btn-dark-ot' and @type='submit' and contains(text(), 'Save')]"),
    "cancel_button": ("xpath", "//a[@class='cancel-btn']"),
    
    # Verification
    "success_message": ("xpath", "//div[contains(@class, 'successMessage')]"),
    "error_message": ("xpath", "//div[contains(@class, 'errorMessage')]"),
}

# ============== Display Configuration ==============
print(f"\n✓ Configuration loaded successfully")
print(f"  - Logs directory: {LOGS_DIR}")
print(f"  - Screenshots directory: {SCREENSHOTS_DIR}")
print(f"  - Headless mode: {HEADLESS_MODE}")
print(f"  - Browser timeout: {BROWSER_TIMEOUT}s\n")
