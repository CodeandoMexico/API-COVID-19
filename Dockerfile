FROM python:3.6.6  

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt ./  
RUN apt-get update && apt-get -y install ghostscript && apt-get clean 
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt  
COPY . /app  
