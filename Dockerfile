FROM python:3.8.5-slim
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app/requirements.txt
WORKDIR /app

RUN pip install -r requirements.txt

COPY api api
COPY geo geo
COPY utils utils
COPY manage.py manage.py

COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh
RUN ls -la

ENTRYPOINT ["/app/entrypoint.sh"]