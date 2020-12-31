FROM python:3.8.7-buster

WORKDIR /usr/src/app

RUN apt-get update \
 && apt-get install -y gnupg2 \
 && apt-get install -y curl \
 && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
 && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
 && apt-get update \
 && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
 && apt-get install -y unixodbc-dev

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pyodbc 

COPY . .

CMD ["scrapy", "crawl", "bluecross"]