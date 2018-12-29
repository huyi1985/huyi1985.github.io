# 开发机free，大量内存被用于cache

* 没有swap分区
* `sync && echo 3 > /proc/sys/vm/drop_caches` 不起作用