FROM python:3.12

WORKDIR /app

COPY Python/* /app

RUN pip install --no-cache-dir requests

CMD ["python", "server.py"]


# docker build -t grafanagrab .
# docker run --net=host grafanagrab 
# result: SIZE: 1.03GB 0_o