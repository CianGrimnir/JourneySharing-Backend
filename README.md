# JourneySharing-Backend


## Run below command to setup the server - 
```
pip3.9 install -r requirements.txt
```

## Start the server locally
* Initialize redis server using below commands
```
cd docker/
docker-compose up -d
```
* Start backend service
```
python3.9 manage.py runserver
```

## Execute test cases for the backend service
```
# set environment variables for module settings -

# Powershell command
$env:DJANGO_SETTINGS_MODULE="journeysharing.settings"

# Bash
export DJANGO_SETTINGS_MODULE="journeysharing.settings"

coverage run --source=. -m pytest -v . && coverage report -m
```