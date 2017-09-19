本文创建了一个Scrapy-Redis+Docker模板

### 从Scrapy到Scrapy-Redis，需要哪些文件做了更改
查看一下文件的注释     
scrapy_redis_demo/scrapy_redis_demo/settings.py    
scrapy_redis_demo/scrapy_redis_demo/spiders/toscrape-xpath.py 

### 启动
```
docker-compose up -d
```
执行docker-compose logs，可以看到spider正在等待喂食
```
2017-09-19 18:10:46 [scrapy.core.engine] INFO: Spider opened
2017-09-19 18:10:46 [scrapy.extensions.logstats] INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)
2017-09-19 18:10:46 [scrapy.extensions.telnet] DEBUG: Telnet console listening on 127.0.0.1:6023
```

### 喂食
```
# 找到redis container id
$ docker ps
CONTAINER ID        IMAGE                       COMMAND                  CREATED             STATUS                         PORTS                                              NAMES
81182b061b7d        scrapyredisdocker_scraper   "scrapy crawl scra..."   55 seconds ago      Restarting (1) 6 seconds ago                                                      scrapyredisdocker_scraper_1
6617e72e3048        redis                       "docker-entrypoint..."   56 seconds ago      Up 55 seconds                  0.0.0.0:6379->6379/tcp                             scrapyredisdocker_redis_1

# 进入redis container，执行redis-cli lpush
$ docker exec -it 6617e72e3048 /bin/bash
root@6617e72e3048:/data# redis-cli lpush scrapy_redis_demo:start_urls http://quotes.toscrape.com
(integer) 1
```
