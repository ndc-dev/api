# FROM python:3.7.2-alpine3.9
FROM python:3.7.3-stretch

COPY . /app/
WORKDIR /app/

# Install production dependencies.
RUN pip install pipenv
RUN pipenv lock -r > requirements.txt
RUN pip install -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 2 --threads 8 -k uvicorn.workers.UvicornWorker main:app
# CMD ["pipenv", "run", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]
# EXPOSE 80