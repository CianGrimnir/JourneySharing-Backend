[![Django CI](https://github.com/CianGrimnir/JourneySharing-Backend/actions/workflows/django.yml/badge.svg)](https://github.com/CianGrimnir/JourneySharing-Backend/actions/workflows/django.yml)

# JourneySharing-Backend

## What is it?

Backend service written in Django and other services for finding and sharing journeys with other users.  
For Frontend see: https://github.com/ConorChurch/ase-journey-sharing

## Getting Started

### Install dependencies - 
```
pip install -r requirements.txt
```

### How to start the server locally - 
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

### How to execute test cases for the backend service -
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

### (OPTIONAL) Steps for enabling https
```
install mkcert following below link - 
https://github.com/FiloSottile/mkcert/
mkdir cert && cd cert
mkcert -install
mkcert -cert-file cert.pem -key-file key.pem localhost 127.0.0.1
cd ../
# run backend service in ssl mode
python3.9 .\manage.py runsslserver --certificate .\cert\cert.pem --key .\cert\key.pem
```