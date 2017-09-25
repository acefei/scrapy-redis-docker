


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
redis是定义在docker-compose.yaml的container name
```
docker exec -it redis redis-cli lpush scrapy_redis_demo:start_urls http://quotes.toscrape.com
```


### 参考
[使用 Docker Compose 配置开发环境](https://coyee.com/article/compare/11003-setting-up-your-development-environment-with-docker-compose)

[Python分布式爬虫打造搜索引擎Scrapy精讲—将bloomfilter(布隆过滤器)集成到scrapy-redis中](http://www.cnblogs.com/adc8868/p/7442306.html)

[how to filter duplicate requests based on url in scrapy](https://stackoverflow.com/questions/12553117/how-to-filter-duplicate-requests-based-on-url-in-scrapy?answertab=votes#tab-top)
