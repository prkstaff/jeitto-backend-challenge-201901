FROM python:3.6-alpine3.7

ENV PROJECT_ROOT /proj

RUN mkdir -p ${PROJECT_ROOT}

WORKDIR ${PROJECT_ROOT}

ADD ./ .

RUN apk --no-cache add --virtual .build-dependencies build-base gcc \
    openssl-dev libffi-dev \
    && pip install -r requirements.dev.txt \
    && rm -rf .cache/pip \
    && apk del .build-dependencies

ENTRYPOINT ["./start.sh"]

