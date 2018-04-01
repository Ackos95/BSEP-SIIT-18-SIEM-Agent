# BSEP-SIIT-18/SIEM-Agent

Python application for `SIEM` agent which should run on monitored machines.

App starts watching folders which are configured to be watched through `agent-config.json` file
(inside `watch-directories` array), and each file modification is captured and handled. Log file is
initially filtered through `regex match` with pattern from configuration (`filter` key) and then,
lines which passed check are being pulled through `SysLogParser` to get an valid object representation
of an log entries (or an error). That data is then handled (this is not implemented yet), and
passed to SIEM-Core, through `http` (url specified in config `siem-core-url`).


### Installation

Install required packages
```bash
pipenv install
```

### Configuration

Before app is started, you need to create configuration. In `SIEM-Agent/config` there is an file
`agent-example.json`, copy it into `agent-config.json` and modify data itself before starting app.

### Start app

Start virtual environment (Only once)
```bash
pipenv shell
```

**Note:** *If using `pycharm` (or any advanced IDE) make sure that you've set up virtual environment
(created by `pipenv`) for an execution interpreter. To find out where those executables are, just type
`pipenv --venv`, and then locate `python` executable from that folder and set it as an default for current project.*

Start app
```bash
python main.py
```

### Testing

**This method is only temporary!**
Add some custom `.log` files (format doesn't matter for now) in `SIEM-AGENT/test-logs`, and update configuration to
watch that folder (or just leave example config). After that start the app, and try modifying some of the `.log` files
from that folder, wait for 15-30 seconds for changes to take an effect, and log with request (which would be sent)
should be visible in console.