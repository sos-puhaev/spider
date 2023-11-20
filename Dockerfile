FROM python:3.8-slim
RUN apt-get update && apt-get install -y libpq-dev
RUN pip3 install scrapy psycopg2-binary pymongo
WORKDIR /bls_scrapy/
COPY . /bls_scrapy
CMD [ "scrapy", "crawl", "thepirate_bay" ]