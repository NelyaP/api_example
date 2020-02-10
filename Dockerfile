FROM python:3.6-slim
ENV PYTHONUNBUFFERED 1
COPY . /code
WORKDIR /code
RUN chmod +x entrypoint.sh
RUN pip install -r requirements.txt
ENTRYPOINT ["./entrypoint.sh"]