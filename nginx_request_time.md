# nignx的request_time在长连接和短连接下分别是怎么（起点终点）计算的

php rt几十ms，ngx rt几百ms，why？

【可能原因1】: phpfpm worker 饱和 saturation 通过phpfpm backlog查看?
 

【可能原因2】: ngx rt的起点和终点
11个阶段

PR
SVR Rewrite
Find Config

RW
POST RW

Pre Access
ACESS 
POST ACESS

TF
CONTENT
LOG

CONTENT在什么条件下转到LOG Phase