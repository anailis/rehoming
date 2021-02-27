# 🐶 Monitoring Rescue Animal Rehoming

This is a long-term project which aims to explore the factors influencing the duration of advertising required before a rescue animal is adopted. The goal is to use this data to make recommendations that may reduce the time between advertisement and adoption.

The data are scraped once daily from the Bluecross and Dogstrust websites using Python's Scrapy framework. The spiders are within a Docker image which is run automatically every 24 hours by an Azure Logic App. Data are stored in an Azure SQL Server database. 

In future, I hope to add spiders for more rescue charities that advertise their animals for adoption online. I use Azure's Container Registry's CI capabilities to immediately integrate any new spiders into the deployed container.


