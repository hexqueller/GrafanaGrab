FROM python:3.12

WORKDIR /app

COPY Python/* /app

RUN pip install --no-cache-dir requests

CMD ["python", "server.py"]


# docker run --net=host grafanagrab