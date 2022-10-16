FROM python:3.7.15-alpine


EXPOSE 5000

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

COPY . /app
WORKDIR /app

#ENV HTTPX_LOG_LEVEL debug
ENV REPO_OWNER 'andrew-pettus'
ENV REPO_TARGET 'forkin'

#ideally these would be pulled from an Azure KeyVault, AWS Secret Manager, Docker Swarm or K8s Secret
ENV FORKME_GHC '86cb9c92aa667f515914'
ENV FORKME_GHS '9ef7511ebb4d4e945d8bdda89d235fbd00d9abc5'


CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]