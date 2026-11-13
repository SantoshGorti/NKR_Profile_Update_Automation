# Command Reference - Naukri Profile Automation

## Installation & Setup

```bash
# Navigate to project
cd /Users/santoshgorti/Documents/NKR

# Install dependencies
pip install -r requirements.txt

# Copy and configure credentials
cp .env.example .env
nano .env  # Edit with your credentials
```

## Running the Automation

### Test Mode (Single Execution)
```bash
python main.py --once
```

### Scheduled Mode (Hourly)
```bash
python main.py --schedule
```

### Custom Interval (Every 2 hours)
```bash
python main.py --schedule --hours 2
```

### Help
```bash
python main.py --help
```

## Background Execution

### Using nohup (Simple)
```bash
# Start in background
nohup python main.py --schedule > logs/background.log 2>&1 &

# View logs
tail -f logs/background.log

# Stop
pkill -f "python main.py"
```

### Using tmux (Recommended)
```bash
# Create session
tmux new-session -d -s naukri-automation "cd /Users/santoshgorti/Documents/NKR && python main.py --schedule"

# View logs
tmux capture-pane -p -t naukri-automation -S -100

# Attach to session
tmux attach-session -t naukri-automation

# Detach
Ctrl+B then D

# Stop session
tmux kill-session -t naukri-automation
```

### Using systemd (Linux)
```bash
# Edit service file
sudo nano /etc/systemd/user/naukri-automation.service

# Enable
systemctl --user enable naukri-automation

# Start
systemctl --user start naukri-automation

# Status
systemctl --user status naukri-automation

# Logs
journalctl --user -u naukri-automation -f
```

## Monitoring & Logging

### View Execution Log (JSON)
```bash
# All executions
jq . logs/execution_log.json

# Last 5 executions
jq '.[-5:]' logs/execution_log.json

# Last execution
jq '.[-1]' logs/execution_log.json

# Pretty print in terminal
cat logs/execution_log.json | python3 -m json.tool
```

### View Console Logs
```bash
# All logs
cat logs/naukri_automation.log

# Last 50 lines
tail -n 50 logs/naukri_automation.log

# Follow in real-time
tail -f logs/naukri_automation.log

# Search for errors
grep ERROR logs/naukri_automation.log

# Search for specific date
grep "2026-11-13" logs/naukri_automation.log
```

### View Screenshots
```bash
# List screenshots
ls -lh screenshots/

# View latest screenshot
open $(ls -t screenshots/ | head -1)

# Count screenshots
ls screenshots/ | wc -l
```

## Execution Analysis

### Count Successes
```bash
jq '[.[] | select(.status=="SUCCESS")] | length' logs/execution_log.json
```

### Count Failures
```bash
jq '[.[] | select(.status=="FAILURE")] | length' logs/execution_log.json
```

### Get All Used Headlines
```bash
jq -r '[.[] | select(.headline!=null) | .headline] | unique[]' logs/execution_log.json
```

### Summary Report
```bash
cat << 'REPORT' > analyze.py
import json
from datetime import datetime
from collections import Counter

with open('logs/execution_log.json') as f:
    logs = json.load(f)

statuses = Counter(log['status'] for log in logs)
print(f"\nExecution Summary")
print(f"================")
print(f"Total executions: {len(logs)}")
print(f"Successful: {statuses.get('SUCCESS', 0)}")
print(f"Failed: {statuses.get('FAILURE', 0)}")
print(f"Success rate: {statuses.get('SUCCESS', 0) / len(logs) * 100:.1f}%")

headlines = [log['headline'] for log in logs if log.get('headline')]
if headlines:
    headline_usage = Counter(headlines)
    print(f"\nHeadline Usage")
    print(f"==============")
    for headline, count in headline_usage.most_common():
        print(f"{count}x: {headline[:50]}...")

REPORT

python3 analyze.py
```

## Configuration Updates

### Update Headlines
```bash
nano headlines.json
# Edit the variations array with your custom headlines
```

### Update Locators (If Naukri Changes Page)
```bash
nano config.py

# Find LOCATORS dictionary and update:
LOCATORS = {
    "resume_headline_field": ("xpath", "//new-selector"),
    ...
}
```

### Change Timeout
```bash
# Edit .env
BROWSER_TIMEOUT=20  # Increase for slow connections
```

### Enable Debug Logging
```bash
# Edit .env
LOG_LEVEL=DEBUG

# Then run
python main.py --once
```

### Disable Headless Mode (See Browser)
```bash
# Edit .env
HEADLESS_MODE=False

# Then run
python main.py --once
```

## Troubleshooting Commands

### Check if Process is Running
```bash
ps aux | grep main.py
```

### Check for CAPTCHA Issues
```bash
grep -i captcha logs/naukri_automation.log
```

### Check for Login Errors
```bash
grep -i "login" logs/naukri_automation.log
```

### Check for Element Not Found
```bash
grep -i "not found" logs/naukri_automation.log
```

### Get Last Error
```bash
jq '.[] | select(.status=="FAILURE") | .error_message' logs/execution_log.json | tail -1
```

### Get Screenshot Path of Last Failure
```bash
jq '.[] | select(.status=="FAILURE") | .screenshot_path' logs/execution_log.json | tail -1
```

### Validate JSON Configuration
```bash
python3 -m json.tool headlines.json > /dev/null && echo "✓ Valid JSON"
```

### Validate Python Syntax
```bash
python3 -m py_compile *.py && echo "✓ All files valid"
```

## Cleanup

### Clear Logs
```bash
rm logs/*.log
```

### Clear Execution History
```bash
echo "[]" > logs/execution_log.json
```

### Clear Screenshots
```bash
rm screenshots/*.png
```

### Backup Everything
```bash
tar -czf backup_$(date +%Y%m%d).tar.gz logs/ screenshots/ headlines.json logs/execution_log.json
```

## Useful One-Liners

```bash
# Monitor real-time execution
watch -n 5 'tail logs/execution_log.json | jq ".[-1]"'

# Count lines executed per day
jq 'group_by(.timestamp[:10]) | map({date: .[0].timestamp[:10], count: length})' logs/execution_log.json

# Find all errors from last 24 hours
jq '.[] | select(.timestamp > "'$(date -d '1 day ago' '+%Y-%m-%d')'") | select(.status=="FAILURE")' logs/execution_log.json

# Generate simple report
echo "Total runs: $(jq length logs/execution_log.json)" && echo "Success rate: $(jq '[.[] | select(.status=="SUCCESS")] | length' logs/execution_log.json)/$(jq length logs/execution_log.json)"

# Email if failures exist (requires mail command)
[ $(jq '[.[] | select(.status=="FAILURE")] | length' logs/execution_log.json) -gt 0 ] && echo "Failures detected" | mail -s "Naukri Automation Alert" your@email.com
```

## Common Issues & Fixes

### Issue: Browser doesn't open
```bash
# Edit .env
HEADLESS_MODE=False

# Run
python main.py --once
```

### Issue: Timeout errors
```bash
# Edit .env - increase timeout
BROWSER_TIMEOUT=30

# Run
python main.py --once
```

### Issue: Can't find headline field
```bash
# Inspect the page manually
# Update LOCATORS in config.py with new selector
# Test with
python main.py --once
```

### Issue: Session expired repeatedly
```bash
# Check network connection
ping www.naukri.com

# Try re-login
python main.py --once

# If still fails, clear browser data
rm -rf ~/.cache/selenium  # Or relevant browser cache
```

### Issue: Still failing?
```bash
# Enable debug logging
echo "LOG_LEVEL=DEBUG" >> .env

# Run with screenshot
python main.py --once

# Check latest screenshot
open $(ls -t screenshots/ | head -1)

# Review full log
tail -100 logs/naukri_automation.log
```

## System Requirements Check

```bash
# Python version
python3 --version  # Should be 3.8+

# Check packages installed
pip list | grep -E "selenium|schedule|python-dotenv"

# Check Chrome
which google-chrome  # or /Applications/Google\ Chrome.app

# Check disk space
df -h /Users/santoshgorti/Documents/

# Check system resources while running
top -p $(pgrep -f "python main.py")
```

---

**For comprehensive documentation, see README.md**
**For quick setup, see QUICKSTART.md**
