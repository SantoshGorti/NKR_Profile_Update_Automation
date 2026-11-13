# Quick Commands Reference

## Running Automation

### Single Execution (Run Once, Then Exit)
```bash
python3 main.py --once
```
- Runs one update cycle
- Logs results
- Exits cleanly
- **Use for:** Testing, manual updates, cron jobs

### Scheduled Execution (Hourly)
```bash
python3 main.py --schedule
```
- Executes immediately
- Repeats every hour
- Continues until interrupted (Ctrl+C)
- **Use for:** Background daemon, continuous operation

### Custom Interval (Every N Hours)
```bash
python3 main.py --schedule --hours 2
python3 main.py --schedule --hours 4
python3 main.py --schedule --hours 6
```
- Executes immediately
- Repeats at specified interval
- **Use for:** Flexible scheduling

## Monitoring & Status

### Check Current Status
```bash
python3 check_status.py
```
- Shows last execution time
- Shows success/failure counts
- Shows recent executions
- Shows last used headline

### View Raw Status JSON
```bash
cat logs/status.json | python3 -m json.tool
```
- Detailed status information
- Machine-readable format
- For scripts/tools

### View Execution History
```bash
cat logs/execution_log.json | python3 -m json.tool
```
- All execution records
- Timestamps and results
- Headlines and errors

### See Recent Logs
```bash
tail -50 logs/naukri_automation.log
```
- Last 50 log lines
- Real-time progress info
- Error details

### Follow Live Logs (Tail)
```bash
tail -f logs/naukri_automation.log
```
- Live log streaming
- Press Ctrl+C to stop
- **Use for:** Watching execution in progress

## Debugging

### Take Full Page Screenshot
The automation automatically takes screenshots on errors. Check:
```bash
ls -lh screenshots/
```

### Run with Debug Logging
```bash
# Edit .env to set LOG_LEVEL=DEBUG, then:
python3 main.py --once
```

### Check Browser Process
```bash
# List Chrome processes
pgrep -a chromedriver
pgrep -a chrome

# Kill lingering processes
pkill -f chromedriver
pkill -f chrome
```

### Test Element Locators
Temporarily add debug code to capture page source:
```python
# In profile.py, add after navigation:
with open("debug_page.html", "w") as f:
    f.write(self.driver.page_source)
```

## File Management

### List All Logs
```bash
ls -lh logs/
```

### List All Screenshots
```bash
ls -lh screenshots/
```

### Clean Old Screenshots
```bash
# Remove screenshots older than 7 days
find screenshots/ -mtime +7 -delete
```

### Rotate Logs
```bash
# Backup current log
cp logs/naukri_automation.log logs/naukri_automation.log.backup

# Clear log (start fresh)
> logs/naukri_automation.log
```

## Configuration

### Edit Credentials
```bash
nano .env
```
Requires:
- `NAUKRI_EMAIL`
- `NAUKRI_PASSWORD`

### Edit Headlines
```bash
nano headlines.json
```
Modify the `variations` array with your own headlines

### Edit Settings
```bash
nano config.py
```
Adjust:
- `HEADLESS_MODE` - Show/hide browser
- `EXPLICIT_WAIT` - Element wait timeout
- `BROWSER_TIMEOUT` - Page load timeout

## System Integration

### Create Cron Job (Hourly)
```bash
# Edit crontab
crontab -e

# Add this line:
0 * * * * cd /path/to/NKR && python3 main.py --once >> logs/cron.log 2>&1
```

### Create Cron Job (Every 6 Hours)
```bash
0 */6 * * * cd /path/to/NKR && python3 main.py --once >> logs/cron.log 2>&1
```

### Create Systemd Service (Optional)
```bash
# Create service file
sudo nano /etc/systemd/system/naukri-automation.service
```

Content:
```ini
[Unit]
Description=Naukri Profile Automation
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/Users/santoshgorti/Documents/NKR
ExecStart=/usr/bin/python3 /Users/santoshgorti/Documents/NKR/main.py --schedule
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable naukri-automation
sudo systemctl start naukri-automation
```

## Troubleshooting Commands

### Verify Python Installation
```bash
python3 --version
python3 -c "import selenium; print(selenium.__version__)"
```

### Verify Dependencies
```bash
pip3 list | grep -E "selenium|python-dotenv"
```

### Check Disk Space
```bash
du -sh logs/
du -sh screenshots/
df -h
```

### Restart After Error
```bash
# Kill any lingering processes
pkill -f "python3 main.py"
pkill -f chromedriver

# Check status
sleep 2
python3 check_status.py

# Try again
python3 main.py --once
```

## Monitoring Scripts

### Monitor Continuously
```bash
# Watch status every 30 seconds
watch -n 30 'python3 check_status.py'
```

### Count Recent Successes
```bash
grep '"status": "SUCCESS"' logs/execution_log.json | wc -l
```

### Find Last Error
```bash
grep '"error_message"' logs/execution_log.json | tail -1
```

### Calculate Success Rate
```bash
python3 << 'EOF'
import json
with open('logs/execution_log.json') as f:
    data = json.load(f)
    total = len(data)
    success = sum(1 for x in data if x['status'] == 'SUCCESS')
    rate = (success/total*100) if total > 0 else 0
    print(f"Success Rate: {success}/{total} ({rate:.1f}%)")
EOF
```

## Emergency Procedures

### Stop Running Automation
```bash
# Graceful shutdown
Ctrl+C

# Force kill if needed
pkill -f "python3 main.py"
```

### Reset Everything
```bash
# Clean logs
rm logs/*.log logs/*.json

# Clean screenshots
rm screenshots/*.png

# Run fresh
python3 main.py --once
```

### Clear Credentials (Security)
```bash
# Replace .env with template
cp .env.example .env

# Edit with real credentials
nano .env
```

## Useful One-Liners

### Show execution timeline
```bash
grep "EXECUTION CYCLE" logs/naukri_automation.log | head -20
```

### Count executions per day
```bash
grep "EXECUTION CYCLE" logs/naukri_automation.log | cut -d' ' -f1 | sort | uniq -c
```

### Show all errors
```bash
grep "ERROR" logs/naukri_automation.log | tail -20
```

### Show success timestamps
```bash
grep "✓ SUCCESS" logs/naukri_automation.log
```

### Monitor real-time with alerts
```bash
while true; do python3 check_status.py; sleep 60; done
```

---

**Tip:** Save this file and refer to it for common commands!
