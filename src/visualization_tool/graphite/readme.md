### Graphite
```
1.安装：https://graphite.readthedocs.io/en/latest/install.html#docker
docker run -d\
--name graphite\
--restart=always\
-p 8080:80\
-p 2003-2004:2003-2004\
-p 2023-2024:2023-2024\
-p 8125:8125/udp\
-p 8126:8126\
graphiteapp/graphite-statsd
其中 -p p1:p2 选项表示将本机的p1端口映射到docker容器的p2端口。由于本机的80端口有nginx，所以讲2003端口映射到docker的80端口。

2.配置 https://segmentfault.com/a/1190000002573509
3.查看数据有没有进来
/opt/graphite/storage/whisper
```
- [代码编写](monitor.py)