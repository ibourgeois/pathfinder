FROM python:3

COPY / /app

WORKDIR /app

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install xvfb -y

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
