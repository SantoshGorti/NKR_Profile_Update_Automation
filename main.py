"""
Main automation script for Naukri profile headline updates.
Orchestrates the complete workflow: login, navigate, update, save, verify.
"""

import sys
import time
from datetime import datetime

from auth import NaukriAuthenticator
from profile import NaukriProfileManager
from scheduler import ExecutionScheduler
from logger import get_logger, ExecutionLogger, take_screenshot
from status import StatusTracker

logger = get_logger(__name__)
execution_logger = ExecutionLogger()


class NaukriAutomation:
    """Main automation orchestrator."""

    def __init__(self):
        """Initialize the automation."""
        self.authenticator = NaukriAuthenticator()
        self.profile_manager = None
        self.scheduler = ExecutionScheduler()
        self.status_tracker = StatusTracker()

    def execute_update_cycle(self):
        """
        Execute a single profile update cycle with improved error recovery.

        This is the function that gets called by the scheduler repeatedly.
        """
        logger.info("\n" + "=" * 70)
        logger.info(f"EXECUTION CYCLE STARTED - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 70)

        selected_headline = None
        try:
            # Step 1: Initialize and authenticate
            logger.info("\n[STEP 1/5] Initializing and authenticating...")
            if not self.authenticator.is_authenticated:
                logger.info("  Attempting login...")
                if not self.authenticator.login():
                    raise Exception("Login failed - check credentials and network")
                logger.info("  ✓ Login successful")
            else:
                logger.info("  Using existing session")

            # Verify session is still active
            if not self.authenticator.verify_session_active():
                logger.warning("  Session expired, attempting re-login...")
                self.authenticator.driver = None
                self.authenticator.is_authenticated = False
                if not self.authenticator.login():
                    raise Exception("Re-login failed after session expiry")
                logger.info("  ✓ Re-login successful")
            else:
                logger.info("  ✓ Session verified")

            # Step 2: Get WebDriver and initialize profile manager
            logger.info("\n[STEP 2/5] Preparing profile manager...")
            driver = self.authenticator.get_driver()
            self.profile_manager = NaukriProfileManager(driver)
            logger.info("  ✓ Profile manager ready")

            # Step 3: Select next headline
            logger.info("\n[STEP 3/5] Selecting next headline...")
            selected_headline = self.scheduler.get_next_headline()
            if not selected_headline:
                raise Exception("Failed to select headline")
            logger.info(f"  ✓ Selected: {selected_headline[:60]}...")

            # Step 4: Update and save profile
            logger.info("\n[STEP 4/5] Updating profile...")
            success, verified = self.profile_manager.update_and_verify_headline(
                selected_headline
            )

            if not success:
                raise Exception("Profile update failed")
            
            logger.info(f"  ✓ Profile updated (verified: {verified})")

            # Step 5: Log and report results
            logger.info("\n[STEP 5/5] Logging results...")
            status = "SUCCESS" if verified else "PARTIAL_SUCCESS"
            message = f"{status} - Headline updated"
            if not verified:
                message += " but verification failed"

            # Log to execution log
            execution_logger.log_execution(
                status=status,
                headline=selected_headline,
                verification_result=verified,
                error_message=None,
                screenshot_path=None,
            )

            # Update status tracker
            self.status_tracker.update_status(status, selected_headline)

            # Console output
            logger.info("\n" + "=" * 70)
            logger.info(f"✓ {message}")
            logger.info(f"  Headline: {selected_headline[:70]}...")
            logger.info(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info("=" * 70 + "\n")

            return True

        except Exception as e:
            logger.error("\n" + "=" * 70)
            logger.error(f"✗ EXECUTION FAILED")
            logger.error(f"  Error: {str(e)}")
            logger.error(f"  Headline: {selected_headline[:70] if selected_headline else 'N/A'}...")
            logger.error(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            logger.error("=" * 70 + "\n")

            # Take screenshot for debugging
            screenshot_path = None
            try:
                if self.authenticator.driver:
                    screenshot_path = take_screenshot(
                        self.authenticator.driver, "execution_failure"
                    )
            except Exception as screenshot_error:
                logger.debug(f"Failed to take screenshot: {str(screenshot_error)}")

            # Log to execution log
            execution_logger.log_execution(
                status="FAILURE",
                headline=selected_headline,
                verification_result=False,
                error_message=str(e),
                screenshot_path=screenshot_path,
            )

            # Update status tracker
            self.status_tracker.update_status("FAILURE", selected_headline, str(e))

            # Attempt graceful recovery on certain errors
            if "Session expired" in str(e) or "Login failed" in str(e):
                logger.info("Attempting session recovery for next cycle...")
                try:
                    self.authenticator.close_driver()
                except:
                    pass

            return False

    def run_once(self):
        """Execute the automation once."""
        logger.info("Running single execution mode...")
        return self.execute_update_cycle()

    def run_scheduled(self, interval_hours=1):
        """
        Run the automation on a schedule.

        Args:
            interval_hours (int): Hours between executions (default: 1)
        """
        logger.info(f"Running scheduled mode - interval: {interval_hours} hour(s)")

        # Execute first cycle immediately
        logger.info("\nExecuting initial cycle...")
        self.execute_update_cycle()

        # Schedule subsequent cycles
        self.scheduler.run_scheduler(
            job_function=self.execute_update_cycle,
            check_interval_seconds=60,
        )

    def cleanup(self):
        """Clean up resources."""
        logger.info("\nCleaning up resources...")
        self.authenticator.close_driver()
        logger.info("✓ Cleanup complete")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Naukri Profile Headline Automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --once              # Run once and exit
  python main.py --schedule          # Run continuously every hour
  python main.py --schedule --hours 2 # Run every 2 hours
        """,
    )

    parser.add_argument(
        "--once",
        action="store_true",
        help="Execute once and exit (no scheduling)",
    )
    parser.add_argument(
        "--schedule",
        action="store_true",
        help="Run on schedule (executes immediately, then repeats)",
    )
    parser.add_argument(
        "--hours",
        type=int,
        default=1,
        help="Interval in hours for scheduled execution (default: 1)",
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.once and not args.schedule:
        parser.print_help()
        logger.error("\nError: Please specify either --once or --schedule")
        sys.exit(1)

    try:
        # Create automation instance
        automation = NaukriAutomation()

        # Run based on mode
        if args.once:
            logger.info("\n" + "=" * 70)
            logger.info("NAUKRI PROFILE AUTOMATION - SINGLE EXECUTION MODE")
            logger.info("=" * 70)
            success = automation.run_once()
            automation.cleanup()
            sys.exit(0 if success else 1)

        elif args.schedule:
            logger.info("\n" + "=" * 70)
            logger.info("NAUKRI PROFILE AUTOMATION - SCHEDULED MODE")
            logger.info(f"Interval: Every {args.hours} hour(s)")
            logger.info("=" * 70)
            automation.run_scheduled(interval_hours=args.hours)

    except KeyboardInterrupt:
        logger.info("\n\nInterrupt received. Shutting down gracefully...")
        try:
            automation.cleanup()
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
        sys.exit(0)

    except Exception as e:
        logger.error(f"\nFatal error: {str(e)}", exc_info=True)
        try:
            automation.cleanup()
        except:
            pass
        sys.exit(1)


if __name__ == "__main__":
    main()
