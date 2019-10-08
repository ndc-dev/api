# NDC API for Developer

## framework
https://fastapi.tiangolo.com/

## development
pipenv install  
pipenv run uvicorn main:app --reload --host 0.0.0.0

## JSON Schema

[jsonschema.json](https://api-4pccg7v5ma-an.a.run.app/schema)  
pipenv run python validate.py

## Docker

docker build . -t calil/ndc.dev  
docker run -it -p 80:80 calil/ndc.dev  
docker push calil/ndc.dev

## Demo

~~[https://ndc-api-beta.arukascloud.io/](https://ndc-api-beta.arukascloud.io/)~~  
[https://api-4pccg7v5ma-an.a.run.app/](https://api-4pccg7v5ma-an.a.run.app/)
