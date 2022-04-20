FROM python:3.9.5-slim-buster

ENV GOOGLE_APPLICATION_CREDENTIALS 'local/gsa/test-mdp-de-gsa.json'
ENV PIP_DEFAULT_TIMEOUT 100
ENV PIP_DISABLE_PIP_VERSION_CHECK 'on'
ENV PIP_NO_CACHE_DIR 'on'
ENV PYTHON_ENV 'local'
ENV PYTHONDONTWRITEBYTECODE 1

RUN ln -sf /usr/share/zoneinfo/America/Lima /etc/localtime

WORKDIR /app
COPY requirements.txt .
RUN \
	pip install pip==20.1.1 && \
	pip install -r requirements.txt

CMD \
	cp -R local/gcsql /tmp/ && \
	chmod -R 0700 /tmp/gcsql && \
	python main.py