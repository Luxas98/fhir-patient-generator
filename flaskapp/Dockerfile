FROM python:3.6-stretch
RUN apt-get update

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app

COPY flaskapp flaskapp
COPY gcloudlogging gcloudlogging
COPY patientgenerator patientgenerator
COPY fhir_fastavro fhir_fastavro
COPY fhir_fastavro/schema schema

COPY wsgi.py wsgi.py
COPY manage.py manage.py
COPY entrypoint.sh entrypoint.sh
COPY gunicorn.conf gunicorn.conf

RUN mkdir -p /etc/secrets
COPY deployments/terraform/credentials.json /etc/secrets/gcs-secret.json

RUN chmod +x entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
