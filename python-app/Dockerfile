FROM python:3.8.0-slim
COPY . /app
RUN pip install aiohttp aiopg
ENTRYPOINT python app/main.py