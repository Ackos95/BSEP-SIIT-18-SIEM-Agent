# BSEP-SIIT-18/SIEM-Agent

Python application for `SIEM` agent which should run on monitored machines.

App starts watching folders which are configured to be watched through config file pulled from siem-core file
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

Also you need to set up certificates for current agent. Inside `config/certs` folder, you should copy
appropriate `trusted_ca.crt` (from `siem-core`), and add one (`.p12`) certificate file for your agent.
Make sure that `trusted_ca.crt` contains server as a trusted source, and to match `config.cert` configurations
with actual data in `config/cert` folder (name of the file must match and password for unlocking `.p12` file). 

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
Update configuration to watch `./test-logs` folder (already set up in example config). After that start the app,
and in other terminal tab run and run `python ./test-scripts/simulate-logs.py LOGGER_NAME`, and watch it update.
