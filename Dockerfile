FROM python:3.12-slim

WORKDIR /app

COPY Python/ .

RUN pip3 install --no-cache-dir requests

# ENV URL="http://grafana:3000"
# ENV KEY="your_key"
# ENV SAVE=""
# ENV PORT=8000

CMD ["python3", "server.py"]