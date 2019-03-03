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
```

## breakpoints
* `mysql_execute_select`
* `row_search_for_mysql`
* `sel_set_rec_lock`


```
lock_rec_lock()

https://github.com/mysql/mysql-server/blob/5.6/storage/innobase/lock/lock0lock.cc#L2281
```

```
p *trx_sys


```

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


