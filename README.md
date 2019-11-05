# block-exporter
  Blockchain prometheus exporter, currently support geth information export

## Get Started
### Installation
```
# git clone this project
~$ git clone git@github.com:charles-hsiao/block-exporter.git
~$ cd block-exporter

# (Optional but recommend)
# Use virtual env for local development
~$ pip install virtualenv
~$ virtualenv venv

# Install packages
~$ pip install -r requirements.txt
```

### Usage
```
# (Option 1) Simply run with python command
~$ python block-exporter.py

# (Option 2) Running with nohup (Background execution)
~$ nohup python block-exporter.py >> ${LOG_PATH} 2>&1 &

# (Option 3) Running with init config
# create config file path
~$ sudo mkdir -p /etc/init.d

# move init config
~$ sudo cp etc/init.d/block_exporter /etc/init.d/block_exporter

# update init config permission
~$ sudo chmod 755 /etc/init.d/block_exporter

# start with init config
~$ bash /etc/init.d/block_exporter start

# (Option 4) Running with init + monit
# Set-up option 3 first but don't start with init config (skip last step)
# install monit first
# Ref: https://mmonit.com/monit/

# move monit config
~$ sudo cp block-exporter/etc/monit/conf.d/block_exporter /etc/monit/conf.d/block_exporter

# reload monit config
~$ sudo monit reload

# start with monit
~$ sudo monit start block_exporter
```

### Validation
```
~$ curl http://localhost:8000
# You should see prometheus metrics below
```
