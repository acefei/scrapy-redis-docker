FROM daocloud.io/python:2-onbuild

COPY pip.conf /root/.pip/pip.conf 
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

# set volume in docer-compose to real-time code sychronization
#COPY scrapy_redis_demo/ ./

WORKDIR /usr/src/app
ENTRYPOINT ["scrapy"]
CMD ["crawl", "scrapy_redis_demo"]
