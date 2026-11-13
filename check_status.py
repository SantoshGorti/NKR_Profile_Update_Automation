#!/usr/bin/env python3
"""
Quick status checker - displays current automation status without running.
Usage: python3 check_status.py
"""

import sys
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from status import StatusTracker
from logger import ExecutionLogger

if __name__ == "__main__":
    tracker = StatusTracker()
    execution_logger = ExecutionLogger()
    
    print("\n" + "=" * 70)
    print("NAUKRI AUTOMATION STATUS")
    print("=" * 70)
    
    # Print tracker status
    tracker.print_status()
    
    # Print recent executions
    print("\nRECENT EXECUTIONS (Last 5):")
    print("-" * 70)
    try:
        with open(execution_logger.execution_log_file, "r") as f:
            import json
            executions = json.load(f)
            for exec_record in executions[-5:]:
                timestamp = exec_record.get("timestamp", "Unknown")
                status = exec_record.get("status", "Unknown")
                error = exec_record.get("error_message", "")
                error_msg = f" - {error[:50]}" if error else ""
                print(f"  {timestamp}: {status}{error_msg}")
    except Exception as e:
        print(f"  Could not read execution log: {str(e)}")
    
    print("=" * 70 + "\n")
