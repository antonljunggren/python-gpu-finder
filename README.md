# Python GPU Finder
##### By Anton Ljunggren

## Requirements
* Python 3
* pip
* email account with securiy turned of

## Instructions
* First create an enviroment
  * `python3 -m venv env`
  * `source env/bin/activate`
* Then install all the packages listed in `dependencies.txt` (you may get some errors and need to install some packages separatley)
* To create the settings file run `python3 create-settings.py`
* Then edit the values in the settings file to correct emails and password
* To run the script run `python3 web-scraper.py`
  * Available arguments:
    1. `--debug [boolean]` (false is default)
    2. `--seconds [number]` (60 is default)
  * Example 1: `python3 web-scraper.py --seconds 30 --debug true`
  * Example 2: `nohup python3 web-scraper.py --seconds 30 --debug false &` To run in background
    * To kill the process run `jobs -l`to list the jobs and look for the process id (PID) then `kill <PID>` to kill the process with given PID
* Then to look at the logs run for example `nano yyyy-MM-dd.log`
