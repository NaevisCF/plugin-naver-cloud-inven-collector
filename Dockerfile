FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1
ENV SPACEONE_PORT 50051
ENV SERVER_TYPE grpc
ENV PKG_DIR /tmp/pkg
ENV SRC_DIR /tmp/src

RUN apt update && apt upgrade -y

COPY pkg/*.txt ${PKG_DIR}/
RUN pip install --upgrade pip && \
    pip install --upgrade -r ${PKG_DIR}/pip_requirements.txt

COPY src ${SRC_DIR}
ARG CACHEBUST=1
WORKDIR ${SRC_DIR}
RUN rm -rf /tmp/*

RUN python3 setup.py install

EXPOSE ${SPACEONE_PORT}

ENTRYPOINT ["spaceone"]
CMD ["run", "plugin-server", "inventory"]

