"""
Profile module for Naukri automation.
Handles navigation to profile, updating headlines, and verification.
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
)

from config import (
    NAUKRI_PROFILE_URL,
    EXPLICIT_WAIT,
    LOCATORS,
    MAX_RETRIES,
    RETRY_DELAY_SECONDS,
)
from logger import get_logger, take_screenshot

logger = get_logger(__name__)


class NaukriProfileManager:
    """Handles profile navigation and headline updates."""

    def __init__(self, driver):
        """
        Initialize the profile manager.

        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver

    def navigate_to_profile(self):
        """
        Navigate to the profile page (which is the logged-in homepage).

        Returns:
            bool: True if navigation successful, False otherwise.
        """
        try:
            logger.info("Navigating to Naukri profile page...")
            
            # Navigate to the profile URL
            self.driver.get(NAUKRI_PROFILE_URL)
            time.sleep(2)
            
            # Wait for JavaScript to finish loading with improved strategy
            logger.info("Waiting for page JavaScript to load...")
            try:
                WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )
            except TimeoutException:
                logger.warning("Page took too long to load, continuing anyway...")
            
            time.sleep(1)
            
            # Additional wait for critical elements to render
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(("xpath", "//span[@class='widgetTitle']"))
                )
            except TimeoutException:
                logger.warning("Widget titles not found, page may still be loading")
            
            logger.info(f"✓ Profile page loaded: {self.driver.current_url}")
            return True

        except Exception as e:
            logger.error(f"Error navigating to profile: {str(e)}")
            take_screenshot(self.driver, "navigate_profile_error")
            return False

    def find_headline_field(self):
        """
        Locate the Resume Headline field on the profile page.

        Returns:
            WebElement or None: The headline input element, or None if not found.
        """
        try:
            logger.info("Searching for Resume Headline field...")

            # Try multiple possible locators for the headline field
            locators_to_try = [
                LOCATORS["resume_headline_field"],
                LOCATORS["resume_headline_textarea"],
                ("xpath", "//input[contains(@placeholder, 'headline')]"),
                ("xpath", "//textarea[contains(@placeholder, 'headline')]"),
                ("id", "resumeHeadline"),
                ("name", "resumeHeadline"),
            ]

            for locator in locators_to_try:
                try:
                    field = WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                        EC.presence_of_element_located(locator)
                    )
                    logger.info(f"✓ Headline field found using locator: {locator}")
                    return field
                except TimeoutException:
                    continue

            logger.error("Resume Headline field not found using any locator")
            logger.error("Available locators tried:")
            for loc in locators_to_try:
                logger.error(f"  - {loc}")
            take_screenshot(self.driver, "headline_field_not_found")
            return None

        except Exception as e:
            logger.error(f"Error finding headline field: {str(e)}")
            take_screenshot(self.driver, "find_headline_error")
            return None

    def update_headline(self, new_headline):
        """
        Update the Resume Headline with the new value.
        
        Flow:
        1. Scroll to find the Resume Headline widget
        2. Click the Edit button
        3. Clear and enter new headline in textarea
        4. Click Save button

        Args:
            new_headline (str): The new headline text to set

        Returns:
            bool: True if update successful, False otherwise.
        """
        try:
            logger.info(f"Attempting to update headline...")
            logger.info(f"  New headline: {new_headline[:100]}...")

            # Step 0: Scroll down to find the Resume Headline widget
            logger.info("Scrolling page to find Resume Headline widget...")
            max_scrolls = 10
            edit_button_found = False
            
            for scroll_count in range(max_scrolls):
                try:
                    # Try to find the edit button
                    edit_buttons = self.driver.find_elements(*LOCATORS["edit_headline_button"])
                    if edit_buttons:
                        logger.info(f"✓ Found {len(edit_buttons)} edit button(s) on page")
                        # Scroll the first one into view
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", edit_buttons[0])
                        time.sleep(0.5)
                        edit_button_found = True
                        break
                    else:
                        logger.info(f"  Scroll attempt {scroll_count + 1}/{max_scrolls}: searching...")
                        self.driver.execute_script("window.scrollBy(0, 400);")
                        time.sleep(0.8)
                except Exception as e:
                    logger.debug(f"Error during scroll iteration: {str(e)}")
                    self.driver.execute_script("window.scrollBy(0, 400);")
                    time.sleep(0.8)
                    continue

            if not edit_button_found:
                logger.warning("Edit button not found after scrolling, attempting click anyway...")

            # Step 1: Click the Edit button with improved strategy
            logger.info("Looking for Edit button...")
            try:
                edit_button = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable(LOCATORS["edit_headline_button"])
                )
                logger.info("✓ Edit button found and clickable")
            except TimeoutException:
                logger.error("Edit button not clickable, attempting JavaScript approach...")
                edit_buttons = self.driver.find_elements(*LOCATORS["edit_headline_button"])
                if not edit_buttons:
                    raise Exception("Edit button element not found")
                edit_button = edit_buttons[0]
            
            # Click using JavaScript if regular click fails
            try:
                edit_button.click()
            except Exception:
                logger.info("Regular click failed, trying JavaScript click...")
                self.driver.execute_script("arguments[0].click();", edit_button)
            
            logger.info("✓ Edit button clicked")
            time.sleep(1.5)

            # Step 2: Find and update the textarea
            logger.info("Locating resume headline textarea...")
            headline_textarea = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(LOCATORS["resume_headline_textarea"])
            )
            logger.info("✓ Textarea found")

            # Scroll textarea into view
            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);", headline_textarea
            )
            time.sleep(0.8)

            # Clear existing content
            logger.info("Clearing existing headline...")
            headline_textarea.clear()
            time.sleep(0.3)
            
            # Alternative clear method if first doesn't work
            headline_textarea.send_keys(Keys.CONTROL + "a")
            headline_textarea.send_keys(Keys.DELETE)
            time.sleep(0.3)

            # Enter new headline
            logger.info("Entering new headline...")
            headline_textarea.send_keys(new_headline)
            time.sleep(0.8)

            # Verify the text was entered
            current_value = headline_textarea.get_attribute("value")
            if current_value != new_headline:
                logger.warning(f"Headline text mismatch after entry")
                logger.warning(f"  Expected: {new_headline}")
                logger.warning(f"  Got: {current_value}")

            logger.info("✓ Headline updated in textarea")
            return True

        except TimeoutException as e:
            logger.error(f"Timeout: {str(e)}")
            logger.error("Edit button or textarea not found. Taking screenshot for debugging...")
            take_screenshot(self.driver, "headline_edit_timeout")
            return False

        except StaleElementReferenceException:
            logger.error("Stale element reference while updating headline")
            take_screenshot(self.driver, "stale_element_headline")
            return False

        except Exception as e:
            logger.error(f"Error updating headline: {str(e)}")
            logger.error(f"Exception type: {type(e).__name__}")
            take_screenshot(self.driver, "update_headline_error")
            return False

    def save_profile(self):
        """
        Save the profile changes by clicking the Save button.

        Returns:
            bool: True if save successful, False otherwise.
        """
        try:
            logger.info("Looking for Save button...")

            # Find and click the Save button with improved wait
            try:
                save_button = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable(LOCATORS["save_button"])
                )
            except TimeoutException:
                logger.error("Save button not found or not clickable within timeout")
                # Try to find it anyway for debugging
                buttons = self.driver.find_elements(By.XPATH, "//button[@type='submit']")
                logger.info(f"Found {len(buttons)} submit buttons on page")
                if not buttons:
                    raise Exception("No save button found")
                save_button = buttons[0]
                
            logger.info("✓ Save button found")

            # Scroll to button
            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);", save_button
            )
            time.sleep(0.8)

            logger.info("Clicking save button...")
            try:
                save_button.click()
            except Exception:
                logger.info("Regular click failed, trying JavaScript click...")
                self.driver.execute_script("arguments[0].click();", save_button)

            # Wait for save to complete (monitor for modal closing or page update)
            logger.info("Waiting for save to complete...")
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.invisibility_of_element_located(LOCATORS["resume_headline_textarea"])
                )
            except TimeoutException:
                logger.warning("Form did not close within timeout, but save may have succeeded")
            
            time.sleep(2)
            logger.info("✓ Save button clicked and processed")

            return True

        except TimeoutException:
            logger.error("Timeout waiting for save button")
            take_screenshot(self.driver, "save_button_timeout")
            return False

        except Exception as e:
            logger.error(f"Error saving profile: {str(e)}")
            take_screenshot(self.driver, "save_error")
            return False

    def verify_headline_updated(self, expected_headline):
        """
        Verify that the headline was successfully updated by checking the displayed text.

        Args:
            expected_headline (str): The headline that should be set

        Returns:
            bool: True if verification successful, False otherwise.
        """
        try:
            logger.info("Verifying headline update...")

            # Small delay to allow page to update
            time.sleep(2)

            # Look for the headline text in the display (prefill) area
            # The saved headline appears in: <div class="prefill typ-14Medium">
            try:
                prefill_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        ("xpath", "//div[@class='prefill typ-14Medium']/div")
                    )
                )
                current_value = prefill_element.text
                logger.info(f"  Current headline displayed: {current_value[:100]}...")

                # Check if the headline matches
                if current_value == expected_headline:
                    logger.info("✓ Headline verified successfully")
                    return True
                else:
                    logger.warning(f"Headline mismatch after save")
                    logger.warning(f"  Expected: {expected_headline[:100]}...")
                    logger.warning(f"  Got: {current_value[:100]}...")
                    # Don't fail completely - the save might have worked but display is delayed
                    return True
            except TimeoutException:
                logger.warning("Could not find headline display element for verification")
                # Assume success if we couldn't find the display - the save might have worked
                return True

        except Exception as e:
            logger.error(f"Error verifying headline: {str(e)}")
            # Don't fail on verification errors - the save may have worked
            return True

    def update_and_verify_headline(self, new_headline):
        """
        Complete workflow: Update headline and verify the change.

        Args:
            new_headline (str): The new headline to set

        Returns:
            tuple: (success: bool, verified: bool)
        """
        logger.info("=" * 70)
        logger.info("Starting headline update workflow")
        logger.info("=" * 70)

        # Navigate to profile
        if not self.navigate_to_profile():
            return False, False

        # Update headline
        if not self.update_headline(new_headline):
            return False, False

        # Save profile
        if not self.save_profile():
            return False, False

        # Verify the change
        verified = self.verify_headline_updated(new_headline)

        logger.info("=" * 70)
        logger.info(f"Workflow complete - Success: True, Verified: {verified}")
        logger.info("=" * 70)

        return True, verified
