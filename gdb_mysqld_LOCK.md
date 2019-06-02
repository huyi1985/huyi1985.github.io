# gdb mysqld LOCK 5.6

## VM config
src
192.168.57.3
/usr/local/mysql/start_mysql.sh
/usr/local/mysql/my.cnf

 ps -ef | fgrep mysql

```
# /usr/local/mysql/start_mysql.sh
gdb --tui -q -p $(pgrep --pid '/usr/local/mysql/data/ubuntu.pid')
gdb --tui -q -p $(pidof mysqld)

```

## breakpoints
* `mysql_execute_select`
* `row_search_for_mysql`
* `sel_set_rec_lock`
* Alternatively, you can set breakpoints on locking related functions: lock_table(), lock_rec_lock(),
row_lock_table_autoinc_for_mysql() etc:



```
lock_rec_lock()

https://github.com/mysql/mysql-server/blob/5.6/storage/innobase/lock/lock0lock.cc#L2281

lock_rec_lock_fast
```

```
p *trx_sys
set $trx_locklist = trx_sys->rw_trx_list->start->lock->trx_locks
set $rowlock = $trx_locklist.start->trx_locks->next
p lock_get_mode($rowlock)
x /4b $rowlock + 1

p trx_sys->rw_trx_list->start->lock->trx_locks->start->un_member->tab_lock->table->name

```

> `x/<n/f/u> <addr>`
> 
> n是一个正整数，表示需要显示的内存单元的个数，也就是说从当前地址向后显示几个内存单元的内容，一个内存单元的大小由后面的u定义。
> 
> u 表示从当前地址往后请求的字节数，如果不指定的话，GDB默认是4个bytes。u参数可以用下面的字符来代替，b表示单字节，h表示双字节，w表示四字 节，g表示八字节。当我们指定了字节长度后，GDB会从指内存定的内存地址开始，读写指定字节，并把其当作一个值取出来。

## Types
`trx_t`: transaction within InnoDB

`trx_lock_t`: all locks associated to a given transaction

`struct lock_t`: a table lock or a row lock

`struct dict_table_t`: table descriptor

## Globals

`lock_sys_t lock_sys`: global object in InnoDB LOCK subsystem

```
lock_sys_t::rec_hash	key => value
key: hash(page_address) = hash(space_id, page_no)
value: lock_t[] of the given page
```

`struct trx_sys_t trx_sys`: global object in InnoDB TRANSACTION subsystem


```
id		user_id		name
--		-------		----
11		1				zhangsan
12		10				li si

UNIQUE KEY `idx_userId` (`user_id`)

SELECT * FROM t1 WHERE user_id = ? FOR UPDATE;

+--------------------+-------+----------------------------------------+
| WHERE user_id = ?  | locks | lock_info                              |
+--------------------+-------+----------------------------------------+
| WHERE user_id = 1  | 2     | mode=1027, heap_no=2, index=idx_userId |
|                    |       | mode=1027, heap_no=2, index=PRIMARY    |
+--------------------+-------+----------------------------------------+
| WHERE user_id = 5  | 1     | mode=515, heap_no=3, index=idx_userId  |
+--------------------+-------+----------------------------------------+
| WHERE user_id = 20 | 1     | mode=3, heap_no=1, index=idx_userId    |
+--------------------+-------+----------------------------------------+

mode
1027 = 1024(LOCK_REC_NOT_GAP) + 3(LOCK_X)
515  = 512(LOCK_GAP) + 3(LOCK_X)
3    = 3(LOCK_X)
```



```
SELECT * FROM t1 WHERE user_id = 1 FOR UPDATE;

lock_table (flags=0, table=0x7efbec037908, mode=LOCK_IX, thr=0x7efbd403c6b8) at /home/huyi/mysql-5.6.42/storage/innobase/lock/lock0lock.cc:4391
(gdb) p table->name
$2 = 0x7efbec036210 "mydb/t1"

lock_rec_lock (impl=0, mode=1027, block=0x7efbfd6c2ec0, heap_no=2, index=0x7efbec0399e8, thr=0x7efbd403c6b8)
(gdb) p index->name
$7 = 0x7efbec039b60 "idx_userId"

lock_rec_lock (impl=0, mode=1027, block=0x7efbfd6c23c0, heap_no=2, index=0x7efbec039048, thr=0x7efbd403c6b8)
(gdb) p index->name
$8 = 0x7efbec0391c0 "PRIMARY"
```

```
SELECT * FROM t1 WHERE user_id = 5 FOR UPDATE;

lock_table (flags=0, table=0x7efbec037908, mode=LOCK_IX, thr=0x7efbd403c6b8)
(gdb) p table->name

lock_rec_lock (impl=0, mode=515, block=0x7efbfd6c2ec0, heap_no=3, index=0x7efbec0399e8, thr=0x7efbd403c6b8)
(gdb) p index->name
$10 = 0x7efbec039b60 "idx_userId"

```
```

SELECT * FROM t1 WHERE user_id = 20 FOR UPDATE;
lock_table (flags=0, table=0x7efbec037908, mode=LOCK_IX, thr=0x7efbd403c6b8)

lock_rec_lock (impl=0, mode=3, block=0x7efbfd6c2ec0, heap_no=1, index=0x7efbec0399e8, thr=0x7efbd403c6b8)
(gdb) p index->name
$14 = 0x7efbec039b60 "idx_userId"
```