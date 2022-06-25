FROM python:3.8.10

ENV PYTHONBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ARG PROJ_DIR=/numbers_test/scripts

RUN mkdir -p ${PROJ_DIR}
COPY ./numbers_test/scripts ${PROJ_DIR}

WORKDIR ${PROJ_DIR}

RUN pip install -U pip \
    pip install -r requirements.txt

CMD ["python", "get_google_sheet.py"]