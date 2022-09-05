FROM python:3.10-slim-bullseye

RUN python -m pip install "poetry==1.2.0"

COPY . /app
WORKDIR /app
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-dev --no-root

ENTRYPOINT ["poetry", "run", "gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--access-logfile", "-", "--bind", "0.0.0.0:80", "--timeout", "60", "main:app"]

EXPOSE 80

