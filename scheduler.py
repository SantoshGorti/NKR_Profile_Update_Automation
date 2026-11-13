"""
Scheduler module for Naukri profile automation.
Manages hourly scheduling with headline rotation and duplicate prevention.
"""

import json
import random
from pathlib import Path

from config import PROJECT_ROOT
from logger import get_logger, ExecutionLogger

logger = get_logger(__name__)


class HeadlineRotator:
    """Manages headline rotation with duplicate prevention."""

    def __init__(self, headlines_file="headlines.json"):
        """
        Initialize the headline rotator.

        Args:
            headlines_file (str): Path to the headlines JSON file
        """
        self.headlines_file = PROJECT_ROOT / headlines_file
        self.execution_logger = ExecutionLogger()
        self.headlines = []
        self._load_headlines()

    def _load_headlines(self):
        """Load headlines from JSON file."""
        try:
            with open(self.headlines_file, "r") as f:
                data = json.load(f)
                self.headlines = [h["headline"] for h in data.get("variations", [])]
                logger.info(f"✓ Loaded {len(self.headlines)} headline variations")
        except Exception as e:
            logger.error(f"Error loading headlines: {str(e)}")
            self.headlines = []

    def get_next_headline(self):
        """
        Get the next headline to use, avoiding consecutive repeats.

        Returns:
            str: The selected headline, or None if no headlines available
        """
        if not self.headlines:
            logger.error("No headlines available for rotation")
            return None

        # Get the last used headline
        last_headline = self.execution_logger.get_last_used_headline()

        if last_headline is None:
            # First execution, pick any random headline
            selected = random.choice(self.headlines)
            logger.info(f"First execution - selected random headline")
        else:
            # Get headlines excluding the last used one
            available_headlines = [h for h in self.headlines if h != last_headline]

            if not available_headlines:
                # Only one headline available, must use it
                logger.warning("Only one headline available, using it despite consecutive repeat")
                selected = self.headlines[0]
            else:
                # Select from available headlines
                selected = random.choice(available_headlines)
                logger.info(f"Avoiding last used headline, selected different one")

        logger.info(f"Selected headline #{self.headlines.index(selected) + 1}:")
        logger.info(f"  {selected[:80]}...")
        return selected

    def get_all_headlines(self):
        """
        Get all available headlines.

        Returns:
            list: List of all headline variations
        """
        return self.headlines.copy()

    def reload_headlines(self):
        """Reload headlines from file (useful if config is updated)."""
        logger.info("Reloading headlines from file...")
        self._load_headlines()


class ExecutionScheduler:
    """Manages the execution schedule and timing."""

    def __init__(self):
        """Initialize the scheduler."""
        self.headliner_rotator = HeadlineRotator()
        self.is_running = False

    def get_next_headline(self):
        """
        Get the next headline to use.

        Returns:
            str: The selected headline
        """
        return self.headliner_rotator.get_next_headline()

    def schedule_job(self, job_function, interval_hours=1):
        """
        Schedule a job to run at regular intervals.

        Args:
            job_function: The function to execute
            interval_hours (int): Interval in hours (default: 1)

        Returns:
            int: Number of scheduled jobs
        """
        try:
            import schedule

            logger.info(f"Scheduling job to run every {interval_hours} hour(s)...")

            # Schedule the job
            schedule.every(interval_hours).hours.do(job_function)

            # Show scheduled jobs
            jobs = schedule.get_jobs()
            logger.info(f"✓ Job scheduled. Total jobs: {len(jobs)}")

            return len(jobs)

        except ImportError:
            logger.error("schedule library not installed. Install with: pip install schedule")
            return 0

    def run_scheduler(self, job_function, check_interval_seconds=60):
        """
        Run the scheduler in blocking mode.

        Args:
            job_function: The function to execute
            check_interval_seconds (int): How often to check schedule (default: 60)
        """
        try:
            import schedule

            self.is_running = True

            logger.info("=" * 70)
            logger.info("SCHEDULER STARTED - Press Ctrl+C to stop")
            logger.info("=" * 70)

            # Schedule the first job
            self.schedule_job(job_function, interval_hours=1)

            # Run the scheduler
            while self.is_running:
                try:
                    schedule.run_pending()
                    import time
                    time.sleep(check_interval_seconds)
                except KeyboardInterrupt:
                    logger.info("\nScheduler interrupt received")
                    self.is_running = False
                    break
                except Exception as e:
                    logger.error(f"Error in scheduler loop: {str(e)}")
                    import time
                    time.sleep(check_interval_seconds)

        except ImportError:
            logger.error("schedule library not installed")
        except Exception as e:
            logger.error(f"Error running scheduler: {str(e)}")
        finally:
            logger.info("Scheduler stopped")
            self.is_running = False

    def stop_scheduler(self):
        """Stop the scheduler."""
        self.is_running = False
        logger.info("Scheduler stop requested")
