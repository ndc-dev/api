# FROM python:3.7.2-alpine3.9
FROM python:3.7.3-stretch

COPY . /app/
WORKDIR /app/
RUN pip install pipenv
RUN pipenv install
CMD ["pipenv", "run", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]
EXPOSE 80