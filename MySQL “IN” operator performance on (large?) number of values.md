# MySQL “IN” operator performance on (large?) number of values

Optimizing large MySQL SELECT WHERE IN clauses

> adaptive hash index
> 
> An optimization for InnoDB tables that can speed up lookups using `=` and `IN` operators, by constructing a hash index in memory. MySQL monitors index searches for InnoDB tables, and if queries could benefit from a hash index, **it builds one automatically for index pages that are frequently accessed**. In a sense, the adaptive hash index configures MySQL at runtime to take advantage of **ample main memory**, coming closer to the architecture of main-memory databases. This feature is controlled by the `innodb_adaptive_hash_index` configuration option. Because this feature benefits some workloads and not others, and **the memory used for the hash index is reserved in the buffer pool**, typically you should benchmark with this feature both enabled and disabled.
> 
> The hash index is always built based on an existing B-tree index on the table. MySQL can build a hash index on a prefix of any length of the key defined for the B-tree, depending on the pattern of searches against the index. A hash index can be partial; the whole B-tree index does not need to be cached in the buffer pool.
> 
> In MySQL 5.6 and higher, another way to take advantage of fast single-value lookups with InnoDB tables is to use the InnoDB memcached plugin. See Section 15.19, “InnoDB memcached Plugin” for details.


## Limits
Oracle 1000 items

MySQL：`max_allowed_packet`

php: `post_max_size`

ngx: `client_max_body`

* 单位：ms
* disable the query cache (via NOW())
* 使用覆盖索引

```
+----------------------+-------+-------+-------+-------+--------+--------+
| WHERE IN 中元素数    | 100   | 500   | 1000  | 2000  | 5000   | 10000  |
+----------------------+-------+-------+-------+-------+--------+--------+
| IN中元素无序         | 17.16 | 39.22 | 56.98 | 87.83 | 174.87 | 301.87 |
+----------------------+-------+-------+-------+-------+--------+--------+
| IN中元素有序（升序） | 13.65 | 32.85 | 53.71 | 81.52 | 164.65 | 295.75 |
+----------------------+-------+-------+-------+-------+--------+--------+
| IN中元素有序（降序） | 13.63 | 31.76 | 54.01 | 84.37 | 157.61 | 290.58 |
+----------------------+-------+-------+-------+-------+--------+--------+
```

* 使用Hash索引

> An optimization for InnoDB tables that can speed up lookups using `=` and `IN` operators, by constructing a hash index in memory.

```
+----------------------+-------+-------+-------+-------+--------+--------+
| WHERE IN 中元素数    | 100   | 500   | 1000  | 2000  | 5000   | 10000  |
+----------------------+-------+-------+-------+-------+--------+--------+
| IN中元素无序         | 12.69 | 29.65 | 48.86 | 76.95 | 155.61 | 283.99 |
+----------------------+-------+-------+-------+-------+--------+--------+
| IN中元素有序（升序） | 13.16 | 31.49 | 51.31 | 81.27 | 163.36 | 283.69 |
+----------------------+-------+-------+-------+-------+--------+--------+
| IN中元素有序（降序） | 13.65 | 31.94 | 54.11 | 80.57 | 152.51 | 293.32 |
+----------------------+-------+-------+-------+-------+--------+--------+
```