# Naukri Profile Automation - Complete Index

## 📍 Project Location
```
/Users/santoshgorti/Documents/NKR
```

---

## 📚 Documentation Files (Read These First)

| File | Purpose | Read Time |
|------|---------|-----------|
| **QUICKSTART.md** | 5-minute setup guide | 5 min |
| **README.md** | Complete reference documentation | 15 min |
| **REFERENCE.md** | Command reference & troubleshooting | 10 min |
| **INDEX.md** | This file - navigation guide | 5 min |

**👉 Start here**: Open `QUICKSTART.md` to get started in 5 minutes

---

## 🔧 Core Python Modules

### 1. **main.py** (233 lines)
- **Purpose**: Main entry point and orchestrator
- **Key Classes**: `NaukriAutomation`
- **Key Methods**: 
  - `execute_update_cycle()` - Complete workflow (login → update → verify)
  - `run_once()` - Single execution
  - `run_scheduled()` - Hourly scheduling
  - `cleanup()` - Resource cleanup
- **Usage**: `python main.py --once` or `python main.py --schedule`

### 2. **auth.py** (222 lines)
- **Purpose**: Authentication and session management
- **Key Classes**: `NaukriAuthenticator`
- **Key Methods**:
  - `initialize_driver()` - Create WebDriver
  - `login()` - Authenticate with Naukri
  - `verify_session_active()` - Check session validity
  - `close_driver()` - Cleanup
- **Features**: Session reuse, retry logic, expiry detection

### 3. **profile.py** (298 lines)
- **Purpose**: Profile navigation and headline updates
- **Key Classes**: `NaukriProfileManager`
- **Key Methods**:
  - `navigate_to_profile()` - Go to profile page
  - `find_headline_field()` - Locate headline input
  - `update_headline()` - Change headline text
  - `save_profile()` - Click save button
  - `verify_headline_updated()` - Verify the change
  - `update_and_verify_headline()` - Complete workflow
- **Features**: Dynamic locator discovery, error screenshots

### 4. **scheduler.py** (184 lines)
- **Purpose**: Scheduling and headline rotation
- **Key Classes**: 
  - `HeadlineRotator` - Intelligent headline selection
  - `ExecutionScheduler` - Job scheduling
- **Key Methods**:
  - `get_next_headline()` - Select headline (avoids repeats)
  - `schedule_job()` - Setup hourly execution
  - `run_scheduler()` - Run indefinitely
- **Features**: Duplicate prevention, configurable intervals

### 5. **logger.py** (170 lines)
- **Purpose**: Logging and execution tracking
- **Key Classes**: `ExecutionLogger`
- **Key Methods**:
  - `setup_logging()` - Configure logging
  - `get_logger()` - Get logger instance
  - `log_execution()` - Record execution details
  - `take_screenshot()` - Capture for debugging
  - `get_last_used_headline()` - Track history
- **Features**: File & console logging, JSON history, screenshots

### 6. **config.py** (87 lines)
- **Purpose**: Configuration management
- **Key Items**:
  - Environment variables loading
  - Directory creation
  - URL definitions
  - Element locators (CSS/XPath selectors)
  - Timeout settings
  - Logging configuration
- **Files**: Reads from `.env` file
- **Validates**: Credentials must be set

---

## ⚙️ Configuration Files

### 1. **.env.example** (Template)
```
NAUKRI_EMAIL=your_email@example.com
NAUKRI_PASSWORD=your_password_here
HEADLESS_MODE=False
BROWSER_TIMEOUT=15
LOG_LEVEL=INFO
```
- **Action Required**: Copy to `.env` and update with your credentials
- **Security**: Never commit `.env` to version control

### 2. **headlines.json** (5 Variations)
```json
{
  "reference_headline": "...",
  "variations": [
    {"id": 1, "headline": "AWS & GCP Cloud Infrastructure Engineer..."},
    {"id": 2, "headline": "DevOps Engineer specializing..."},
    ...
  ]
}
```
- **Purpose**: Stores 5 professional headline variations
- **Auto-Rotated**: Randomly selected each execution
- **Duplicate Prevention**: Avoids consecutive repeats
- **Editable**: Can modify to customize headlines

### 3. **requirements.txt**
```
selenium>=4.15.0
schedule>=1.2.0
python-dotenv>=1.0.0
```
- **Usage**: `pip install -r requirements.txt`
- **All** required dependencies listed

---

## 📁 Directories

### **logs/** (Auto-created)
Contains execution logs and history:
- `naukri_automation.log` - Detailed timestamped logs
- `execution_log.json` - Structured execution history

### **screenshots/** (Auto-created)
Contains failure screenshots for debugging:
- Named with timestamp: `failure_20261113_100000.png`
- Automatically captured on errors

### **config/** (For future use)
Reserved for additional configuration files

---

## 🚀 Quick Commands

### Installation
```bash
cd /Users/santoshgorti/Documents/NKR
pip install -r requirements.txt
cp .env.example .env
nano .env  # Add your credentials
```

### Run Once (Test)
```bash
python main.py --once
```

### Run Hourly (Continuous)
```bash
python main.py --schedule
```

### Run Every 2 Hours
```bash
python main.py --schedule --hours 2
```

### Run in Background
```bash
nohup python main.py --schedule > logs/background.log 2>&1 &
```

### View Logs
```bash
tail -f logs/naukri_automation.log
jq . logs/execution_log.json
```

---

## 📊 Project Statistics

```
Total Files: 11
├── Python Modules: 6 (1,194 lines of code)
├── Configuration Files: 3
├── Documentation Files: 4
└── Auto-created Directories: 3

Python Code Distribution:
├── profile.py:      298 lines (25%)
├── main.py:         233 lines (20%)
├── auth.py:         222 lines (19%)
├── scheduler.py:    184 lines (15%)
├── logger.py:       170 lines (14%)
└── config.py:        87 lines (7%)

Documentation:
├── README.md:       591 lines (main reference)
├── QUICKSTART.md:   186 lines (quick setup)
├── REFERENCE.md:    300+ lines (commands & troubleshooting)
└── INDEX.md:        This file

Headline Variations: 5 (pre-configured)
```

---

## 🎯 Architecture Overview

### Execution Flow
```
1. LOGIN & AUTHENTICATE
   ├── Load credentials from .env
   ├── Initialize WebDriver
   └── Login to Naukri

2. NAVIGATE TO PROFILE
   ├── Go to profile page
   ├── Wait for page load
   └── Locate headline field

3. UPDATE HEADLINE
   ├── Select random headline (avoid repeats)
   ├── Clear existing text
   ├── Enter new headline
   └── Click save button

4. VERIFY & SAVE
   ├── Wait for save completion
   ├── Verify headline changed
   └── Log results

5. SCHEDULE & REPEAT
   ├── Log execution (success/failure)
   ├── Save to JSON history
   ├── Take screenshot on error
   └── Wait 1 hour for next execution
```

### Module Dependencies
```
main.py
├── Imports: auth.py, profile.py, scheduler.py, logger.py
├── Orchestrates: Complete workflow
└── Handles: CLI, error handling, reporting

auth.py
├── Imports: Selenium, config.py, logger.py
├── Manages: Login, session, WebDriver
└── Provides: Reusable authenticated driver

profile.py
├── Imports: Selenium, config.py, logger.py
├── Manages: Navigation, updates, verification
└── Uses: WebDriver from auth.py

scheduler.py
├── Imports: headlines.json, logger.py
├── Manages: Scheduling, headline rotation
└── Prevents: Consecutive headline repeats

logger.py
├── Imports: config.py
├── Provides: Logging, history tracking, screenshots
└── Maintains: execution_log.json

config.py
├── Imports: .env file (via python-dotenv)
├── Manages: All configuration & settings
└── Provides: Constants for other modules
```

---

## 🔍 File References

### When You Need To...

| Task | File(s) | Section |
|------|---------|---------|
| **Set up** | QUICKSTART.md | All |
| **Configure credentials** | .env.example, config.py | Setup |
| **Customize headlines** | headlines.json | Edit variations |
| **Change update frequency** | main.py | args.hours parameter |
| **Update page selectors** | config.py | LOCATORS dictionary |
| **View execution status** | logs/execution_log.json | View with `jq` |
| **Debug errors** | logs/naukri_automation.log | tail -f |
| **See failure screenshots** | screenshots/ | ls -t \| head -1 |
| **Get help with commands** | REFERENCE.md | All |
| **Understand architecture** | README.md | Technical section |
| **Fix a problem** | README.md | Troubleshooting |
| **Configure logging** | config.py, .env | LOG_LEVEL |
| **Run in background** | REFERENCE.md | Background Execution |

---

## ⚠️ Important Files (Don't Delete)

- **main.py** - Core orchestrator (without this, nothing runs)
- **auth.py** - Login & session (required for authentication)
- **profile.py** - Updates (required for headline changes)
- **headlines.json** - Variations (automation won't run without this)
- **.env** - Credentials (required for login)

---

## 🛡️ Security Files (Keep Private)

- **.env** - Contains your Naukri password (never share!)
- **logs/** - May contain sensitive execution details
- **screenshots/** - May show your Naukri profile

---

## ✅ Pre-flight Checklist

Before running, verify:

- [ ] Python 3.8+ installed: `python3 --version`
- [ ] Dependencies installed: `pip list | grep selenium`
- [ ] `.env` file created from `.env.example`
- [ ] `.env` has your email and password
- [ ] `headlines.json` exists and is valid
- [ ] Python files compile: `python3 -m py_compile *.py`
- [ ] Directories exist: `logs/`, `screenshots/`, `config/`
- [ ] Internet connection working
- [ ] Chrome browser installed

---

## 📞 Support & Troubleshooting

### Quick Help
1. Check QUICKSTART.md if stuck on setup
2. Check REFERENCE.md for command help
3. Check README.md Troubleshooting section
4. Review logs: `tail logs/naukri_automation.log`
5. Check screenshot: `open screenshots/$(ls -t screenshots | head -1)`

### Common Issues
- **Can't login**: Check .env credentials, verify Naukri URL
- **Can't find elements**: Naukri may have updated selectors
- **Timeout errors**: Increase BROWSER_TIMEOUT in .env
- **Session expired**: Automation will re-authenticate automatically

---

## 🎓 Learning Path

1. **First Time?** → Start with QUICKSTART.md (5 min)
2. **Need Details?** → Read README.md (15 min)
3. **Want to Debug?** → Check REFERENCE.md (10 min)
4. **Ready to Modify?** → Review each Python module

---

## 📈 Next Steps

1. ✅ **Setup**: Follow QUICKSTART.md
2. ✅ **Test**: Run `python main.py --once`
3. ✅ **Deploy**: Use `python main.py --schedule`
4. ✅ **Monitor**: Watch `logs/execution_log.json`
5. ✅ **Maintain**: Review logs weekly

---

## 🎉 You're All Set!

Your Naukri automation tool is complete and ready to use. Start with QUICKSTART.md for a 5-minute setup, then run your first test with:

```bash
cd /Users/santoshgorti/Documents/NKR
python main.py --once
```

**Happy recruiting!** 🚀

---

*Last Updated: 2026-11-13*
*Project Version: 1.0*
*Status: Production Ready*
