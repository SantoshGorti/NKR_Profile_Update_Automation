# Quick Start Guide - Naukri Profile Automation

Get up and running in 5 minutes.

## Step 1: Install Dependencies (2 minutes)

```bash
cd /Users/santoshgorti/Documents/NKR

# Install required packages
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed selenium-4.x.x schedule-1.x.x python-dotenv-1.x.x
```

## Step 2: Configure Credentials (1 minute)

```bash
# Copy and edit the environment file
cp .env.example .env

# Edit with your Naukri credentials (use your preferred editor)
# Example with nano:
nano .env
```

**Update these lines:**
```
NAUKRI_EMAIL=your_email@naukri.com
NAUKRI_PASSWORD=your_password_here
```

Save and close the file.

## Step 3: Test Once (2 minutes)

```bash
python main.py --once
```

**What happens:**
1. Browser opens
2. Logs into Naukri
3. Updates your headline with one of 5 variations
4. Saves the change
5. Verifies the update was successful
6. Closes gracefully

**Success output:**
```
====================================================================
EXECUTION CYCLE STARTED - 2026-11-13 10:00:00
====================================================================
✓ Successfully authenticated with Naukri
✓ Headline updated in field
✓ Save button clicked
✓ Headline verified successfully

====================================================================
✓ SUCCESS - Headline updated successfully
  Headline: AWS & GCP Cloud Infrastructure Engineer | Terraform | ...
  Timestamp: 2026-11-13 10:00:30
====================================================================
```

## Step 4: Run on Schedule (Continuous)

```bash
# Start automatic hourly updates
python main.py --schedule
```

**To run every 2 hours instead:**
```bash
python main.py --schedule --hours 2
```

**To run in background (macOS/Linux):**
```bash
nohup python main.py --schedule > logs/automation.log 2>&1 &

# View logs
tail -f logs/automation.log

# Stop when needed
pkill -f "python main.py"
```

---

## 5 Headline Variations (Pre-configured)

The automation will rotate through these every hour (avoiding repeats):

1. **AWS & GCP Cloud Infrastructure Engineer** | Terraform | Kubernetes | Docker | CI/CD Automation with Jenkins & ArgoCD

2. **DevOps Engineer specializing in Cloud Automation** | AWS | GCP | Terraform | Kubernetes | Docker | Linux | CI/CD Pipeline Expert

3. **Cloud Infrastructure Automation Specialist** | AWS, GCP, Kubernetes, Docker, Terraform | Linux Administration & Deployment Reliability

4. **Infrastructure as Code & Container Orchestration Expert** | AWS, GCP, Terraform, Kubernetes, Docker, Jenkins, ArgoCD, Linux

5. **Senior DevOps Professional** | Cloud Platforms (AWS/GCP), Kubernetes, Docker, Terraform, CI/CD, Jenkins, ArgoCD, Monitoring & Linux Administration

---

## View Execution History

```bash
# See all executions (pretty-printed)
jq . logs/execution_log.json

# See last 5 executions
jq '.[-5:]' logs/execution_log.json

# Count successes
jq '[.[] | select(.status=="SUCCESS")] | length' logs/execution_log.json

# Real-time log watching
tail -f logs/naukri_automation.log
```

---

## Troubleshooting (First Run Issues)

| Issue | Solution |
|-------|----------|
| "NAUKRI_EMAIL and NAUKRI_PASSWORD must be set" | Edit `.env` file - make sure credentials are there |
| Browser doesn't open | Change `HEADLESS_MODE=True` to `HEADLESS_MODE=False` in `.env` |
| "Timeout waiting for login elements" | Increase `BROWSER_TIMEOUT=30` in `.env` |
| CAPTCHA appears | This is normal on first login. Solve it manually, then the session will be reused |
| "Resume Headline field not found" | Naukri changed their page - update `LOCATORS` in `config.py` |

---

## What Gets Logged?

Two types of logs are created:

1. **naukri_automation.log** - Detailed execution log
   ```bash
   cat logs/naukri_automation.log
   ```

2. **execution_log.json** - Structured execution history
   ```bash
   cat logs/execution_log.json
   ```

On failure, a screenshot is saved to `screenshots/` for debugging.

---

## Next Steps

- **Read full docs**: `cat README.md` for complete documentation
- **Customize headlines**: Edit `headlines.json` to add your own variations
- **Monitor logs**: Watch `logs/naukri_automation.log` while running
- **Schedule for background**: Use the instructions in README.md for tmux or systemd

---

## Common Questions

**Q: How do I stop the automation?**
- Press `Ctrl+C` if running in foreground
- Use `pkill -f "python main.py"` if running in background

**Q: Will this harm my account?**
- No, respectful hourly updates are normal profile management
- The automation follows Naukri's ToS

**Q: Can I change how often it updates?**
- Yes: `python main.py --schedule --hours 2` for 2-hour intervals

**Q: What if Naukri changes their website?**
- Update the CSS/XPath selectors in `config.py`
- Instructions in README.md's Troubleshooting section

---

That's it! You're ready to go. The automation will now update your Naukri profile headline every hour. 🚀
