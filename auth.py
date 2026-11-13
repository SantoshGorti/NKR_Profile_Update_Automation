"""
Authentication module for Naukri profile automation.
Handles login, session management, and session reuse.
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException,
)

from config import (
    NAUKRI_LOGIN_PAGE_URL,
    NAUKRI_HOME_URL,
    NAUKRI_EMAIL,
    NAUKRI_PASSWORD,
    HEADLESS_MODE,
    BROWSER_TIMEOUT,
    EXPLICIT_WAIT,
    LOCATORS,
    MAX_RETRIES,
    RETRY_DELAY_SECONDS,
)
from logger import get_logger

logger = get_logger(__name__)


class NaukriAuthenticator:
    """Handles Naukri authentication and session management."""

    def __init__(self):
        """Initialize the authenticator."""
        self.driver = None
        self.is_authenticated = False
        self._last_activity_time = None
        self._session_start_time = None

    def initialize_driver(self):
        """
        Initialize the Chrome WebDriver with appropriate options.
        Reuses existing driver if available.
        Launches in Incognito mode to avoid "Save Password" popups.
        """
        if self.driver is not None:
            logger.info("Reusing existing browser session")
            return self.driver

        logger.info("Initializing new Chrome WebDriver in Incognito mode...")

        options = webdriver.ChromeOptions()

        # Incognito mode - prevents "Save Password" popup and other browser features
        options.add_argument("--incognito")

        # Set headless mode based on configuration
        if HEADLESS_MODE:
            options.add_argument("--headless=new")

        # Additional options for stability
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument(f"--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)")

        # Disable password manager popup
        options.add_argument("--disable-password-manager-reauthentication")
        prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
        options.add_experimental_option("prefs", prefs)

        try:
            # Use Selenium Manager if available (Selenium 4.6+)
            self.driver = webdriver.Chrome(options=options)
            self.driver.set_page_load_timeout(BROWSER_TIMEOUT)
            self.driver.implicitly_wait(10)
            logger.info("✓ WebDriver initialized successfully in Incognito mode")
            return self.driver
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {str(e)}")
            raise

    def login(self, retry_count=0):
        """
        Authenticate with Naukri using provided credentials.
        
        Flow: Homepage -> Click Login button -> Login page -> Enter credentials -> Submit

        Args:
            retry_count (int): Current retry attempt number.

        Returns:
            bool: True if login successful, False otherwise.
        """
        if self.is_authenticated:
            logger.info("Already authenticated. Skipping login.")
            return True

        try:
            logger.info(f"Logging in to Naukri (attempt {retry_count + 1}/{MAX_RETRIES})...")

            # Initialize driver if not already done
            if self.driver is None:
                self.initialize_driver()

            # Step 1: Navigate to homepage
            logger.info("Navigating to Naukri homepage...")
            self.driver.get(NAUKRI_HOME_URL)
            time.sleep(2)
            logger.info("✓ Navigated to Naukri homepage")

            # Step 2: Click login button on homepage
            logger.info("Looking for login button on homepage...")
            try:
                login_button_homepage = WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                    EC.element_to_be_clickable(LOCATORS["login_button_homepage"])
                )
                logger.info("✓ Login button found on homepage")
                login_button_homepage.click()
                logger.info("✓ Clicked login button, redirecting to login page...")
                time.sleep(3)
            except TimeoutException:
                logger.warning("Homepage login button not found, trying direct login page access...")
                self.driver.get(NAUKRI_LOGIN_PAGE_URL)
                time.sleep(2)

            # Step 3: Wait for email field on login page
            logger.info("Waiting for login form...")
            email_field = WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                EC.presence_of_element_located(LOCATORS["login_email_field"])
            )
            logger.info("✓ Email field located")

            # Step 4: Enter email
            email_field.clear()
            email_field.send_keys(NAUKRI_EMAIL)
            logger.info("✓ Email entered")
            time.sleep(1)

            # Step 5: Enter password
            password_field = WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                EC.presence_of_element_located(LOCATORS["login_password_field"])
            )
            password_field.clear()
            password_field.send_keys(NAUKRI_PASSWORD)
            logger.info("✓ Password entered")
            time.sleep(1)

            # Step 6: Click login button on login page
            login_button = WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                EC.element_to_be_clickable(LOCATORS["login_button"])
            )
            login_button.click()
            logger.info("✓ Login button clicked")

            # Step 7: Wait for navigation to complete (check if we're redirected from login page)
            time.sleep(3)
            WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                lambda driver: "login" not in driver.current_url.lower() or driver.current_url == NAUKRI_HOME_URL
            )

            self.is_authenticated = True
            self._session_start_time = time.time()
            self._last_activity_time = time.time()
            logger.info("✓ Successfully authenticated with Naukri")
            logger.info(f"  Current URL: {self.driver.current_url}")
            return True

        except TimeoutException:
            logger.error("Timeout waiting for login elements. Page may be slow or layout changed.")
            logger.error(f"Current URL: {self.driver.current_url}")
            if retry_count < MAX_RETRIES:
                logger.info(f"Retrying login (attempt {retry_count + 2}/{MAX_RETRIES})...")
                time.sleep(RETRY_DELAY_SECONDS)
                try:
                    self.driver.quit()
                except:
                    pass
                self.driver = None
                return self.login(retry_count + 1)
            return False

        except NoSuchElementException as e:
            logger.error(f"Required element not found: {str(e)}")
            logger.error("Page structure may have changed. Please verify element locators in config.py")
            logger.error(f"Current URL: {self.driver.current_url}")
            return False

        except WebDriverException as e:
            logger.error(f"WebDriver error during login: {str(e)}")
            if retry_count < MAX_RETRIES:
                logger.info(f"Retrying login...")
                time.sleep(RETRY_DELAY_SECONDS)
                try:
                    self.driver.quit()
                except:
                    pass
                self.driver = None
                return self.login(retry_count + 1)
            return False

        except Exception as e:
            logger.error(f"Unexpected error during login: {str(e)}")
            logger.error(f"Current URL: {self.driver.current_url}")
            return False

    def verify_session_active(self):
        """
        Verify if the current session is still active.

        Returns:
            bool: True if session is active, False otherwise.
        """
        try:
            if self.driver is None:
                return False

            # Check if we can access profile page (simple verification)
            self.driver.get("https://www.naukri.com/myr/profile")
            time.sleep(2)

            # If redirected to login, session expired
            if "login" in self.driver.current_url.lower():
                logger.warning("Session expired - redirected to login page")
                self.is_authenticated = False
                return False

            logger.info("✓ Session is still active")
            return True

        except Exception as e:
            logger.warning(f"Error verifying session: {str(e)}")
            self.is_authenticated = False
            return False

    def close_driver(self):
        """Close the WebDriver and cleanup resources gracefully."""
        try:
            if self.driver is not None:
                # Attempt graceful close
                try:
                    self.driver.quit()
                    logger.info("✓ WebDriver closed gracefully")
                except Exception as e:
                    logger.warning(f"Graceful close failed, forcing close: {str(e)}")
                    # Force close
                    try:
                        self.driver.close()
                    except:
                        pass
        except Exception as e:
            logger.error(f"Error closing WebDriver: {str(e)}")
        finally:
            self.driver = None
            self.is_authenticated = False
            self._last_activity_time = None
            self._session_start_time = None

    def get_driver(self):
        """
        Get the current WebDriver instance. Initialize if needed.

        Returns:
            WebDriver: The Selenium WebDriver instance.
        """
        if self.driver is None:
            self.initialize_driver()
        return self.driver
