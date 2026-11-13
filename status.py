"""
Status tracker for monitoring automation progress and health.
Provides real-time status information without blocking execution.
"""

import json
from datetime import datetime
from pathlib import Path
from config import LOGS_DIR


class StatusTracker:
    """Tracks and reports execution status."""

    def __init__(self):
        """Initialize status tracker."""
        self.status_file = LOGS_DIR / "status.json"
        self.default_status = {
            "last_execution": None,
            "last_status": "IDLE",
            "last_headline": None,
            "execution_count": 0,
            "success_count": 0,
            "failure_count": 0,
            "next_scheduled": None,
            "uptime_seconds": 0,
        }

    def update_status(self, status, headline=None, error=None):
        """
        Update status file.

        Args:
            status (str): Current status (RUNNING, SUCCESS, FAILURE, etc.)
            headline (str): Current headline being processed
            error (str): Error message if applicable
        """
        try:
            # Read existing or create new
            if self.status_file.exists():
                with open(self.status_file, "r") as f:
                    data = json.load(f)
            else:
                data = self.default_status.copy()

            # Update status
            data["last_execution"] = datetime.now().isoformat()
            data["last_status"] = status
            if headline:
                data["last_headline"] = headline[:100]
            if error:
                data["last_error"] = error

            # Update counts
            if status == "SUCCESS":
                data["success_count"] = data.get("success_count", 0) + 1
            elif status == "FAILURE":
                data["failure_count"] = data.get("failure_count", 0) + 1

            data["execution_count"] = data.get("execution_count", 0) + 1

            # Write back
            with open(self.status_file, "w") as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            # Silently fail - don't let status tracking break automation
            pass

    def get_status(self):
        """
        Get current status.

        Returns:
            dict: Current status information.
        """
        try:
            if self.status_file.exists():
                with open(self.status_file, "r") as f:
                    return json.load(f)
        except:
            pass

        return self.default_status.copy()

    def print_status(self):
        """Print current status to console."""
        status = self.get_status()
        print("\n" + "=" * 70)
        print("STATUS REPORT")
        print("=" * 70)
        print(f"  Last Execution:  {status.get('last_execution', 'Never')}")
        print(f"  Last Status:     {status.get('last_status', 'Unknown')}")
        print(f"  Success Count:   {status.get('success_count', 0)}")
        print(f"  Failure Count:   {status.get('failure_count', 0)}")
        print(f"  Total Executions: {status.get('execution_count', 0)}")
        if status.get('last_headline'):
            print(f"  Last Headline:   {status['last_headline'][:60]}...")
        if status.get('last_error'):
            print(f"  Last Error:      {status['last_error'][:80]}...")
        print("=" * 70 + "\n")
