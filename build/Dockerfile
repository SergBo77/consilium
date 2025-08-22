FROM python:3.12-slim

RUN apt-get update && apt-get -y upgrade \
    && apt-get install -y build-essential cmake

WORKDIR /app

COPY ./src/requirements.txt requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

COPY --chmod=775 build/entrypoint.sh /entrypoint.sh
COPY ./src .
COPY build/.env .env

EXPOSE 8000
CMD ["/entrypoint.sh"]