# Builds an image for qed celery worker

#FROM python:3
FROM quanted/qed_py3

# Install requirements for cts_celery
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt

# Copy the project code
COPY . /src/
WORKDIR /src
