# fastapi-test
https://fastapi.tiangolo.com/

# development
pipenv install  
pipenv run uvicorn main:app --reload --host 0.0.0.0

## Docker

docker build . -t calil/fastapi-test  
docker run -it -p 80:80 calil/fastapi-test  
docker push calil/fastapi-test
