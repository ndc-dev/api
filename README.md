# NDC API for Developer

## framework
https://fastapi.tiangolo.com/

## development
pipenv install  
pipenv run uvicorn main:app --reload --host 0.0.0.0

## Docker

docker build . -t calil/ndc.dev  
docker run -it -p 80:80 calil/ndc.dev  
docker push calil/ndc.dev