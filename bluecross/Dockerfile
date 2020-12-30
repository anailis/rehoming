FROM python:3.8.7-buster

WORKDIR /usr/src/app

RUN apt-get update \
 && apt-get install -y gnupg2 \
 && apt-get install -y curl \
 && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
 && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17
RUN apt-get install -y unixodbc-dev

#RUN apt-get update \
# && apt-get install unixodbc -y \
# && apt-get install unixodbc-dev -y \
# && apt-get install freetds-dev -y \
# && apt-get install freetds-bin -y \
# && apt-get install tdsodbc -y \
# && apt-get install --reinstall build-essential -y

#RUN echo "[FreeTDS]\n\
#Description = FreeTDS unixODBC Driver\n\
#Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so\n\
#Setup = /usr/lib/x86_64-linux-gnu/odbc/libtdsS.so" >> /etc/odbcinst.ini

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pyodbc 

COPY . .

CMD ["scrapy", "crawl", "bluecross"]