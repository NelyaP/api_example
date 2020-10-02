FROM python:3.8.5-slim
ENV PYTHONUNBUFFERED 1
COPY . /code
WORKDIR /code
RUN ls -la
RUN chmod +x entrypoint.sh
#RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT ["/code/entrypoint.sh"]