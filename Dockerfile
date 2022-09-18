FROM python:3.10-slim-bullseye as requirements-stage

WORKDIR /tmp
RUN python -m pip install "poetry==1.2.0"
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10-slim-bullseye

WORKDIR /app
COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY . /app
ENV PYTHONPATH=/app

ENTRYPOINT ["gunicorn", "--access-logfile", "-", "--bind", "0.0.0.0:80", "--timeout", "60", "app:app"]

EXPOSE 80

