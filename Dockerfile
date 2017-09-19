FROM daocloud.io/python:2-onbuild


COPY pip.conf /root/.pip/pip.conf 
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

WORKDIR /usr/src/app

COPY scrapy_redis_demo/ ./

ENTRYPOINT ["scrapy"]
CMD ["crawl", "scrapy_redis_demo"]
