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
## NOT REQUIRED ANYMORE

# Powershell command
$env:DJANGO_SETTINGS_MODULE="journeysharing.settings"

# Bash command
export DJANGO_SETTINGS_MODULE="journeysharing.settings"

# run test cases
coverage run --source=. -m pytest -v . && coverage report -m
```

## (OPTIONAL) Steps for enabling https
```
install mkcert following below link - 
https://github.com/FiloSottile/mkcert/

mkdir cert && cd cert
mkcert -install
mkcert -cert-file cert.pem -key-file key.pem localhost 127.0.0.1
cd ../

# run backend service in ssl mode
python3 .\manage.py runsslserver --certificate .\cert\cert.pem --key .\cert\key.pem
```