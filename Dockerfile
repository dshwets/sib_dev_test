FROM python:3.7
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code
RUN pip install -r /code/requirements.txt
COPY source /code
EXPOSE 8000