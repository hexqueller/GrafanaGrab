# docker build -t grafanagrab .
# docker run \
    # --name grafanagrab
    # --net=host \
    # -v ${PWD}:/data\
    # -d \
    # --rm \
    # grafanagrab


FROM alpine:latest

RUN apk update && apk add --no-cache py-pip python3-dev

USER root

WORKDIR /app

COPY Python/* /app

RUN python3 -m venv /app/venv

ENV PATH="/app/venv/bin:$PATH"

RUN pip3 install --no-cache-dir requests

CMD ["python3", "server.py"]
# result: SIZE: 169MB <3


# FROM python:3.12

# WORKDIR /app

# COPY Python/* /app

# RUN pip install --no-cache-dir requests

# CMD ["python", "server.py"]
# result: SIZE: 1.03GB 0_o