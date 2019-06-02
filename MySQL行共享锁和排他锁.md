# MySQL/sqlite 行共享锁和排他锁

https://blog.csdn.net/she_lock/article/details/82022431

## MySQL

https://dev.mysql.com/doc/mysql-sourcebuild-excerpt/5.5/en/installing-source-distribution.html#installing-source-distribution-install-distribution

cmake options

```
-DCMAKE_C_FLAGS="-g -O0" -DCMAKE_CXX_FLAGS="-g -O0" -DCMAKE_INSTALL_PREFIX="/opt/mysql-5.6.43" -DWITH_DEBUG=1 -D MYSQL_MAINTAINER_MODE=0

make CFLAGS='-Wno-error' CXXFLAGS="-Wno-error"


cd /opt/mysql-5.6.43/scripts
./mysql_install_db --basedi=/opt/mysql-5.6.43 --user=root
```

不关闭`MYSQL_MAINTAINER_MODE` cmake会在FLAGS后加上`-Werror`

from MySQL Glossary
> locking read
> A SELECT statement that also performs a locking operation on an InnoDB table. Either SELECT ... FOR UPDATE or SELECT ... LOCK IN SHARE MODE. It has the potential to produce a deadlock, depending on the isolation level of the transaction. The opposite of a non-locking read. Not allowed for global tables in a read-only transaction.
> 
> See Section 15.7.2.4, “Locking Reads”.


https://blog.csdn.net/she_lock/article/details/82022431
> InnoDB引擎默认的修改数据语句，update,delete,insert 都会自动给涉及到的数据加上排他锁，select 语句默认不会加任何锁类型。

### INSERT

### UPDATE

```
(gdb) b mysql_execute_command
(gdb) b mysql_update
(gdb) b mysql_prepare_update
```

// lock_tables

```
#0  lock_tables (thd=0x55be2fd13ee0, tables=0x7f62940057b0, count=1, flags=0) at /opt/mysql-5.6.43-src/sql/sql_base.cc:5951

#1  0x000055be2d663802 in mysql_update (thd=0x55be2fd13ee0, table_list=0x7f62940057b0, fields=..., values=..., conds=0x0, order_num=0, order=0x0, limit=1,
    handle_duplicates=DUP_ERROR, ignore=false, found_return=0x7f62b75de740, updated_return=0x7f62b75de7d0) at /opt/mysql-5.6.43-src/sql/sql_update.cc:361

#2  0x000055be2d5cb570 in mysql_execute_command (thd=0x55be2fd13ee0) at /opt/mysql-5.6.43-src/sql/sql_parse.cc:3375

#3  0x000055be2d5d3bde in mysql_parse (thd=0x55be2fd13ee0, rawbuf=0x7f62940056c0 "update t1 set i_f1 = 2 limit 1", length=30, parser_state=0x7f62b75df6a0)
    at /opt/mysql-5.6.43-src/sql/sql_parse.cc:6422
```

// lock_rec_lock 3(LOCK_X)

```
#0  lock_rec_lock (impl=0, mode=3, block=0x7f62bd30d780, heap_no=2, index=0x7f62940199b8, thr=0x7f62940460c0)
    at /opt/mysql-5.6.43-src/storage/innobase/lock/lock0lock.cc:2296
#1 lock_clust_rec_read_check_and_lock
#2 sel_set_rec_lock
#3 row_search_for_mysql
#4 ha_innobase::index_read
#5 ha_innobase::index_first
#6 ha_innobase::rnd_next
#7 handler::ha_rnd_next
#8 rr_sequential
#9  0x000055be2d664c52 in mysql_update (thd=0x55be2fd13ee0, table_list=0x7f62940057b0, fields=..., values=..., conds=0x0, order_num=0, order=0x0, limit=1,
    handle_duplicates=DUP_ERROR, ignore=false, found_return=0x7f62b75de740, updated_return=0x7f62b75de7d0) at /opt/mysql-5.6.43-src/sql/sql_update.cc:744
```

### DELETE

```
#0  mysql_delete (thd=0x55be2fd13ee0, table_list=0x7f62940057a0, conds=0x0, order_list=0x55be2fd16640, limit=1, options=0) at /opt/mysql-5.6.43-src/sql/sql_delete.cc:49

#1  0x000055be2d5cc0f4 in mysql_execute_command (thd=0x55be2fd13ee0) at /opt/mysql-5.6.43-src/sql/sql_parse.cc:3642

#2  0x000055be2d5d3bde in mysql_parse (thd=0x55be2fd13ee0, rawbuf=0x7f62940056c0 "delete from t1 limit 1", length=22, parser_state=0x7f62b75df6a0)
    at /opt/mysql-5.6.43-src/sql/sql_parse.cc:6422
```

lock_rec_lock mode=3

```
#0  lock_rec_lock (impl=0, mode=3, block=0x7f62bd30d780, heap_no=2, index=0x7f62940199b8, thr=0x7f62940460c0)
    at /opt/mysql-5.6.43-src/storage/innobase/lock/lock0lock.cc:2296

#1 lock_clust_rec_read_check_and_lock
#2 sel_set_rec_lock
#3 row_search_for_mysql
#4 ha_innobase::index_read
#5 ha_innobase::index_first
#6 ha_innobase::rnd_next
#7 handler::ha_rnd_next
#8 rr_sequential
#9  0x000055be2d79b0fa in mysql_delete (thd=0x55be2fd13ee0, table_list=0x7f62940057a0, conds=0x0, order_list=0x55be2fd16640, limit=1, options=0)
    at /opt/mysql-5.6.43-src/sql/sql_delete.cc:362
```

加排他锁可以使用select ...for update 语句；
加共享锁可以使用select ... lock in share mode语句。
加过排他锁的数据行在其他事务种是不能被修改的，也不能通过for update和lock in share mode锁的方式查询数据，但可以直接通过select ...from...查询数据，因为普通查询没有任何锁机制。

## Sqlite

### UPDATE

```
#0  sqlite3VdbeExec (p=0x820a520) at ../SQLite-26a559b6/src/vdbe.c:484
#1  0xf6fed203 in sqlite3_step (pStmt=0x820a520) at ../SQLite-26a559b6/src/vdbeapi.c:159
#2  0xf6ff631c in sqlite3_exec (db=0x81f7008, zSql=0x8209840 "update t1 set i_f1 = 10 where i_f1 = 1;",	xCallback=0x8049628 <callback>,	pArg=0xfef1e690,
    pzErrMsg=0xfef1e638) at ../SQLite-26a559b6/src/legacy.c:79
#3  0x0804bfa3 in process_input	(p=0xfef1e690, in=0x0) at ../SQLite-26a559b6/src/shell.c:1191
#4  0x0804ca32 in main (argc=2,	argv=0xfef1fc44) at ../SQLite-26a559b6/src/shell.c:1472
```

### INSERT

```
#0  sqlite3VdbeExec (p=0x8d374c8) at ../SQLite-26a559b6/src/vdbe.c:484
#1  0xf6fed203 in sqlite3_step (pStmt=0x8d374c8) at ../SQLite-26a559b6/src/vdbeapi.c:159
#2  0xf6ff631c in sqlite3_exec (db=0x8d2c0a8, zSql=0x8d37a50 "insert into t1 values (4);", xCallback=0x8049628 <callback>, pArg=0xfef3fd60, pzErrMsg=0xfef3fd08)
    at ../SQLite-26a559b6/src/legacy.c:79
#3  0x0804bfa3 in process_input	(p=0xfef3fd60, in=0x0) at ../SQLite-26a559b6/src/shell.c:1191
#4  0x0804ca32 in main (argc=2,	argv=0xfef41314) at ../SQLite-26a559b6/src/shell.c:1472
```
