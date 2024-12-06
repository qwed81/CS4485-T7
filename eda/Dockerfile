FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && apt-get clean

# Install Python packages
RUN pip install --no-cache-dir jupyter fastapi httpx uvicorn

COPY jupyter.py jupyter.py
COPY run.sh run.sh

EXPOSE 8001

CMD ["bash", "./run.sh"]
