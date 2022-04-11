[![Django CI](https://github.com/CianGrimnir/JourneySharing-Backend/actions/workflows/django.yml/badge.svg)](https://github.com/CianGrimnir/JourneySharing-Backend/actions/workflows/django.yml)

# JourneySharing-Backend


## Run below command to setup the server - 
```
pip install -r requirements.txt
```

## Start the server locally
* Initialize redis server using below commands
```
cd docker/
docker-compose up -d
```
* Start backend service
```
python manage.py runserver
```

* To change the default port number, update the value of `Django_Port` present in the `settings.ini` file
```
[settings]
Django_Port=8091
```

## Execute test cases for the backend service
```
# set environment variables for module settings -
## NOT REQUIRED ANYMORE

# Powershell command
$env:DJANGO_SETTINGS_MODULE="journeysharing.settings"

# Bash command
export DJANGO_SETTINGS_MODULE="journeysharing.settings"

# run test cases
# BASH
coverage run --source=. -m pytest -v . && coverage report -m

# Powershell
coverage run --source=. -m pytest -v . ; coverage report -m
```