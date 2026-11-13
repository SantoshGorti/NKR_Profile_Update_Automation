# Naukri Profile Headline Automation

A Python-based Selenium automation tool that periodically updates your Naukri.com profile headline to improve visibility to recruiters. The automation intelligently rotates through five professional headline variations every hour, avoiding consecutive repeats.

---

## Features

✅ **Automated Authentication** - Secure login with session reuse  
✅ **Hourly Scheduling** - Runs automatically every hour without manual intervention  
✅ **Intelligent Rotation** - Randomly selects from 5 professional headlines, avoiding repeats  
✅ **Session Management** - Reuses authenticated session between updates  
✅ **Comprehensive Logging** - Structured logs with timestamps and execution status  
✅ **Error Recovery** - Automatic retry logic and recovery mechanisms  
✅ **Screenshot Capture** - Takes screenshots on failure for debugging  
✅ **Execution Tracking** - JSON-based execution history for analysis  
✅ **Configurable Elements** - Easy-to-update CSS/XPath selectors for page changes  

---

## Project Structure

```
naukri-automation/
├── main.py                 # Main orchestrator script
├── auth.py                 # Authentication & session management
├── profile.py              # Profile navigation & updates
├── scheduler.py            # Hourly scheduling & headline rotation
├── logger.py               # Logging & execution tracking
├── config.py               # Configuration & settings
├── headlines.json          # Resume headline variations
├── .env.example            # Environment variables template
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── logs/                  # Execution logs (auto-created)
├── screenshots/           # Failure screenshots (auto-created)
└── config/                # Config directory (for future use)
```

---

## Installation

### Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)
- **Google Chrome** (for ChromeDriver)
- **macOS/Linux/Windows**

### Step 1: Clone or Create the Project

```bash
cd /Users/santoshgorti/Documents/NKR
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- **selenium** (4.15.0+) - Browser automation
- **schedule** (1.2.0+) - Scheduling library
- **python-dotenv** (1.0.0+) - Environment variable management

Selenium 4.6+ includes **Selenium Manager** which automatically handles ChromeDriver downloads.

### Step 3: Configure Credentials

Copy the environment template and add your Naukri credentials:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```
NAUKRI_EMAIL=your_email@example.com
NAUKRI_PASSWORD=your_secure_password

HEADLESS_MODE=False
BROWSER_TIMEOUT=15
LOG_LEVEL=INFO
```

> **Security Note**: Never commit `.env` to version control. The `.env` file is sensitive and contains credentials.

### Step 4: Verify Headline Variations

The five professional headline variations are pre-configured in `headlines.json`. Review and customize them if needed:

```json
{
  "variations": [
    {
      "id": 1,
      "headline": "AWS & GCP Cloud Infrastructure Engineer | Terraform | Kubernetes | Docker | CI/CD Automation with Jenkins & ArgoCD"
    },
    {
      "id": 2,
      "headline": "DevOps Engineer specializing in Cloud Automation | AWS | GCP | Terraform | Kubernetes | Docker | Linux | CI/CD Pipeline Expert"
    },
    ...
  ]
}
```

Each variation preserves the core technical skills: AWS, GCP, Terraform, Kubernetes, Docker, Jenkins, ArgoCD, and Linux administration.

---

## Configuration

### Environment Variables (.env)

| Variable | Default | Description |
|----------|---------|-------------|
| `NAUKRI_EMAIL` | - | Your Naukri login email |
| `NAUKRI_PASSWORD` | - | Your Naukri password |
| `HEADLESS_MODE` | False | Run browser in headless mode (no UI) |
| `BROWSER_TIMEOUT` | 15 | Page load timeout in seconds |
| `LOG_LEVEL` | INFO | Logging level (DEBUG, INFO, WARNING, ERROR) |

### Customizing Page Element Locators

If Naukri updates their page structure, update the `LOCATORS` dictionary in `config.py`:

```python
LOCATORS = {
    "login_email_field": ("id", "usernameField"),
    "login_password_field": ("id", "passwordField"),
    "resume_headline_field": ("xpath", "//input[@placeholder='Resume headline']"),
    ...
}
```

Supported locator types: `id`, `name`, `xpath`, `css selector`, `class name`, etc.

### Headline Variations

Edit `headlines.json` to customize the five headline options:

```bash
# View current headlines
cat headlines.json | jq '.variations[].headline'

# Add new variations (maintain the JSON structure)
```

---

## Usage

### Single Execution (Test Mode)

Run the automation once to test everything is working:

```bash
python main.py --once
```

**Output:**
```
[2026-11-13 10:00:00] ✓ Configuration loaded successfully
[2026-11-13 10:00:01] Initializing new Chrome WebDriver...
[2026-11-13 10:00:05] ✓ Successfully authenticated with Naukri
[2026-11-13 10:00:10] ✓ Headline updated successfully
[2026-11-13 10:00:10] Execution Status: SUCCESS
```

### Scheduled Mode (Hourly)

Run the automation continuously with 1-hour intervals:

```bash
python main.py --schedule
```

Run with custom interval (e.g., every 2 hours):

```bash
python main.py --schedule --hours 2
```

**Output:**
```
====================================================================
NAUKRI PROFILE AUTOMATION - SCHEDULED MODE
Interval: Every 1 hour(s)
====================================================================
Scheduler started - Press Ctrl+C to stop

[EXECUTION 1 - 2026-11-13 10:00:00] SUCCESS
[EXECUTION 2 - 2026-11-13 11:00:00] SUCCESS
[EXECUTION 3 - 2026-11-13 12:00:00] SUCCESS
...
```

### Running in the Background

#### macOS / Linux

```bash
# Run in background, log output to file
nohup python main.py --schedule > logs/background.log 2>&1 &

# Check if running
ps aux | grep main.py

# Stop the process
pkill -f "python main.py"
```

#### Using tmux (Recommended)

```bash
# Create a new tmux session
tmux new-session -d -s naukri-automation "cd /Users/santoshgorti/Documents/NKR && python main.py --schedule"

# View logs in real-time
tmux capture-pane -p -t naukri-automation -S -100

# Stop the session
tmux kill-session -t naukri-automation
```

#### Using systemd (Linux)

Create `/etc/systemd/user/naukri-automation.service`:

```ini
[Unit]
Description=Naukri Profile Headline Automation
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/Users/santoshgorti/Documents/NKR
ExecStart=/usr/bin/python3 main.py --schedule
Restart=on-failure
RestartSec=60

[Install]
WantedBy=default.target
```

```bash
systemctl --user enable naukri-automation
systemctl --user start naukri-automation
systemctl --user status naukri-automation
```

---

## Logging and Monitoring

### Console Logs

Real-time logs are displayed on the console showing:
- Execution timestamp
- Step-by-step progress
- Selected headline
- Success/failure status
- Error details

### Log Files

All logs are saved to `logs/`:

- **naukri_automation.log** - Main execution log with all details
- **execution_log.json** - Structured JSON log with execution history

**View execution history:**

```bash
# Pretty-print execution log
cat logs/execution_log.json | jq .

# Show last 10 executions
tail -c 10000 logs/execution_log.json | jq '.[-10:]'

# Count successes vs failures
jq '[.[] | .status] | group_by(.) | map({status: .[0], count: length})' logs/execution_log.json
```

### Screenshots

On failure, screenshots are automatically saved to `screenshots/` for debugging:

```bash
# List all failure screenshots
ls -lh screenshots/

# Open last failure screenshot
open $(ls -t screenshots/ | head -1)
```

---

## Troubleshooting

### Problem: "NAUKRI_EMAIL and NAUKRI_PASSWORD must be set"

**Solution**: Ensure your `.env` file is properly configured:
```bash
cp .env.example .env
# Edit .env with your credentials
cat .env  # Verify it's set correctly
```

### Problem: "Resume Headline field not found"

**Solution**: Naukri may have changed their page structure:

1. Open Naukri in your browser
2. Right-click on the Headline input field → Inspect
3. Find the element's `id`, `name`, `placeholder`, or `xpath`
4. Update `LOCATORS` in `config.py` with the new selectors
5. Test with `python main.py --once`

Example updated locator:
```python
LOCATORS = {
    "resume_headline_field": ("xpath", "//input[@data-id='headline-input']"),
    ...
}
```

### Problem: "Timeout waiting for login elements"

**Solutions**:
- Verify Naukri URL is correct (currently: https://www.naukri.com/naukri/user/login)
- Increase `BROWSER_TIMEOUT` in `.env` to 20-30 seconds
- Check internet connection
- Naukri may require CAPTCHA for new IPs (see next section)

### Problem: CAPTCHA or MFA Required

If Naukri requires CAPTCHA or multi-factor authentication:

1. **Do not bypass security measures** - This violates Naukri's ToS
2. **Manual intervention required**: Run in non-headless mode with manual CAPTCHA solving
3. **First login**: Log in manually first from your IP, approve any MFA
4. **Session reuse**: Subsequent automated runs will reuse the session

To handle manual CAPTCHA:

1. Set `HEADLESS_MODE=False` in `.env`
2. Run: `python main.py --once`
3. When CAPTCHA appears, solve it manually in the browser
4. Wait for automation to continue
5. Subsequent runs may not require CAPTCHA if session is maintained

### Problem: "Session expired - redirected to login page"

**Solution**: The automation automatically detects session expiry and re-authenticates:

```bash
# Check logs for re-authentication attempts
grep -i "session expired" logs/naukri_automation.log

# If re-authentication fails, clear the session:
# (Next execution will force fresh login)
```

### Problem: Execution keeps failing

**Debug Steps**:

1. Check the latest execution status:
   ```bash
   tail logs/naukri_automation.log
   ```

2. View the execution log:
   ```bash
   jq '.[-1]' logs/execution_log.json
   ```

3. Check the failure screenshot:
   ```bash
   ls -t screenshots/ | head -1  # Latest screenshot
   ```

4. Enable debug logging:
   ```bash
   # Edit .env
   LOG_LEVEL=DEBUG
   python main.py --once
   ```

5. Run in non-headless mode to observe the browser:
   ```bash
   HEADLESS_MODE=False python main.py --once
   ```

---

## Security Considerations

### Credentials

- ✅ Credentials stored in `.env` (not in code)
- ✅ Never logged or printed
- ✅ `.env` should be in `.gitignore`

### Browser Automation

- ✅ Uses Selenium with Chrome
- ✅ Respects Naukri's ToS (non-aggressive automation)
- ⚠️ Does not bypass security measures (CAPTCHA, MFA)
- ⚠️ Respects hourly rate limits (check Naukri's policy)

### Best Practices

1. **Never share your `.env` file**
2. **Use strong, unique passwords** (Naukri account)
3. **Review logs regularly** for unauthorized access attempts
4. **Run on trusted machines only**
5. **Keep dependencies updated**: `pip install --upgrade -r requirements.txt`

---

## Advanced Usage

### Custom Scheduling

To run every 2 hours:
```bash
python main.py --schedule --hours 2
```

To run multiple times in an hour (e.g., 30 minutes):
```bash
# Edit scheduler.py and modify interval
# Or implement custom scheduling logic
```

### Headless Mode

For servers without GUI:

```bash
# Edit .env
HEADLESS_MODE=True

# Run normally
python main.py --schedule
```

### Monitoring and Alerts

Create a wrapper script to check execution status:

```bash
#!/bin/bash
# check_status.sh

LAST_LOG=$(jq '.[-1]' logs/execution_log.json)
STATUS=$(echo $LAST_LOG | jq -r '.status')

if [ "$STATUS" != "SUCCESS" ]; then
    echo "Alert: Last execution failed!"
    echo $LAST_LOG | jq .
    # Send email, Slack notification, etc.
fi
```

---

## FAQ

### Q: Why does it avoid consecutive headline repeats?

The automation tracks the last used headline and avoids selecting the same one twice in a row. This ensures more natural-looking profile updates and prevents search algorithms from penalizing repetitive changes.

### Q: Can I run multiple profiles?

Currently, the tool manages one profile per instance. To run multiple profiles:

1. Create separate project folders for each profile
2. Copy all files to each folder
3. Configure unique `.env` files with different emails/passwords
4. Run each instance in separate terminals/sessions

### Q: How often should I update my headline?

This depends on Naukri's algorithm. The default hourly interval is a reasonable balance. Check Naukri's guidelines or experiment with `--hours` flag.

### Q: Will this affect my profile rating?

Regular (non-aggressive) updates should not negatively impact your profile. However:
- Do not update too frequently (more than once per hour)
- Respect Naukri's terms of service
- Monitor if profile rating is affected and adjust frequency

### Q: Can I stop the automation?

Yes, press `Ctrl+C` in the terminal running the automation. It will cleanly shut down and close the browser.

---

## Support and Troubleshooting

### Getting Help

1. **Check logs**:
   ```bash
   tail -f logs/naukri_automation.log  # Watch logs in real-time
   ```

2. **View execution history**:
   ```bash
   jq . logs/execution_log.json
   ```

3. **Inspect failure screenshots**:
   ```bash
   ls -lh screenshots/
   ```

4. **Enable debug mode**:
   ```bash
   LOG_LEVEL=DEBUG python main.py --once
   ```

### Reporting Issues

Document:
- Error message from logs
- Screenshot if available
- Naukri website changes (if page structure changed)
- Steps to reproduce

---

## Updates and Maintenance

### Check for updates

Manually update selectors in `config.py` if Naukri changes their page structure.

### Update dependencies

```bash
pip install --upgrade -r requirements.txt
```

### Backup your data

```bash
# Backup execution history
cp logs/execution_log.json logs/execution_log.backup.json

# Backup logs
tar -czf logs_backup_$(date +%Y%m%d).tar.gz logs/
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-11-13 | Initial release |

---

## License

This project is provided as-is for personal use. Respect Naukri's terms of service when using this automation.

---

## Disclaimer

This tool is designed for personal use only. Users are responsible for:
- Ensuring compliance with Naukri's terms of service
- Maintaining the security of their credentials
- Monitoring and adjusting update frequency based on Naukri's algorithms
- Taking responsibility for any account actions performed by this automation

The developers are not responsible for account suspension, bans, or any other consequences resulting from the use of this tool.

---

**Happy recruiting! 🚀**
