FROM python:3.8.10

ENV PYTHONBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ARG PROJ_DIR=/numbers_test

RUN mkdir -p ${PROJ_DIR}
COPY ./numbers_test ${PROJ_DIR}

WORKDIR ${PROJ_DIR}

RUN pip install -U pip \
    pip install -r requirements.txt

COPY ./compose/django/entry.sh /entry.sh
RUN chmod +x /entry.sh
ENTRYPOINT [ "/entry.sh" ]