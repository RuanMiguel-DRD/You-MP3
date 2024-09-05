FROM python:3.10

WORKDIR /app

COPY README.md .

COPY pyproject.toml .
COPY poetry.lock .

COPY you_mp3 you_mp3

RUN apt update -y && \
    apt install -y ffmpeg && \
    pip install --upgrade pip && \
    pip install poetry && \
    poetry lock --no-update && \
    poetry install

RUN echo "export SHELL=/bin/bash" >> start.sh && \
    echo "poetry shell" >> start.sh && \
    chmod +x start.sh

ENTRYPOINT ["/bin/bash", "-c", "./start.sh"]
