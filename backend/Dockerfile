FROM python:3.10.8-slim-buster as build-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10.8-slim-buster
WORKDIR /app
COPY --from=build-stage /tmp/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY . .
ADD https://github.com/afrincon/ms-proyecto-final-ai-despliegue-senales/releases/download/v1.0/modelo.h5 /app/modelo.h5
EXPOSE 8080
CMD ["python", "main.py"]
