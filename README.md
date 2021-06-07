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
* Then install all the packages listed in `dependencies.txt`
* To run the script run `python3 web-scraper.py`
  * Available arguments:
    1. `--debug [boolean]` (false is default)
    2. `--seconds [number]` (60 is default)
  * Example: `python3 web-scraper.py --seconds 30 --debug true`
