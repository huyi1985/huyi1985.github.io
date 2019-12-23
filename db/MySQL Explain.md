# MySQL Explain

表user的定义如下：
```sql
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `ext` varchar(2048) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1
```

有如下SQL语句：
```sql
-- 1 --
select name from user where name = 'foobar';

-- 2 --
select * from user where name = 'foobar';
```

为什么语句1可以用上“覆盖索引”（Using index），而语句2不能？

```
$ /opt/mysql-5.6/bin/mysql -e"explain select name from user where name = 'foobar';" --user=root test
+----+-------------+-------+------+---------------+----------+---------+-------+------+--------------------------+
| id | select_type | table | type | possible_keys | key      | key_len | ref   | rows | Extra                    |
+----+-------------+-------+------+---------------+----------+---------+-------+------+--------------------------+
|  1 | SIMPLE      | user  | ref  | idx_name      | idx_name | 35      | const |    1 | Using where; Using index |
+----+-------------+-------+------+---------------+----------+---------+-------+------+--------------------------+

$ /opt/mysql-5.6/bin/mysql -e"explain select * from user where name = 'foobar';" --user=root test
+----+-------------+-------+------+---------------+----------+---------+-------+------+-----------------------+
| id | select_type | table | type | possible_keys | key      | key_len | ref   | rows | Extra                 |
+----+-------------+-------+------+---------------+----------+---------+-------+------+-----------------------+
|  1 | SIMPLE      | user  | ref  | idx_name      | idx_name | 35      | const |    1 | Using index condition |
+----+-------------+-------+------+---------------+----------+---------+-------+------+-----------------------+
```

gdb attach上mysqld，设置断点：

```
(gdb) b Explain_join::explain_extra
(gdb) b Explain_table_base::explain_extra_common
```

注意到如下判断条件

```c
// mysql-server-5.6/sql/opt_explain.cc +1518
                   
// Using index
if (
    ((tab->type == JT_INDEX_SCAN || tab->type == JT_CONST) && table->covering_keys.is_set(tab->index)) 
        ||
    (quick_type == QUICK_SELECT_I::QS_TYPE_ROR_INTERSECT && !((QUICK_ROR_INTERSECT_SELECT*) select->quick)->need_to_fetch_row) 
        ||
    table->key_read) {
    if (quick_type == QUICK_SELECT_I::QS_TYPE_GROUP_MIN_MAX) {
        ...
    } else {
        if (push_extra(ET_USING_INDEX))
            return true;
    }
```

1. tab->type为枚举值：`enum join_type {JT_UNKNOWN, JT_SYSTEM, JT_CONST, JT_EQ_REF, JT_REF, JT_ALL, JT_RANGE, JT_INDEX_SCAN, JT_FT, JT_REF_OR_NULL, JT_UNIQUE_SUBQUERY, JT_INDEX_SUBQUERY, JT_INDEX_MERGE}`
2. tab->index `unsigned int`





```

// Common base class for Explain_join and Explain_table
Explain_table_base(Explain_context_enum context_type_arg,

root@vagrant-ubuntu-trusty-64:~/mysql-server-5.6# /opt/mysql-5.6/bin/mysql -e"explain select name from user;" --user=root test
+----+-------------+-------+-------+---------------+----------+---------+------+------+-------------+
| id | select_type | table | type  | possible_keys | key      | key_len | ref  | rows | Extra       |
+----+-------------+-------+-------+---------------+----------+---------+------+------+-------------+
|  1 | SIMPLE      | user  | index | NULL          | idx_name | 35      | NULL |    2 | Using index |
+----+-------------+-------+-------+---------------+----------+---------+------+------+-------------+
root@vagrant-ubuntu-trusty-64:~/mysql-server-5.6# /opt/mysql-5.6/bin/mysql -e"explain select * from user;" --user=root test
+----+-------------+-------+------+---------------+------+---------+------+------+-------+
| id | select_type | table | type | possible_keys | key  | key_len | ref  | rows | Extra |
+----+-------------+-------+------+---------------+------+---------+------+------+-------+
|  1 | SIMPLE      | user  | ALL  | NULL          | NULL | NULL    | NULL |    2 | NULL  |
+----+-------------+-------+------+---------------+------+---------+------+------+-------+


enum Extra_tag
{
  ET_none,
  ET_USING_TEMPORARY,
  ET_USING_FILESORT,
  ET_USING_INDEX_CONDITION,
  ET_USING,
...

```

## Using index condition

```c++
// ./sql/opt_explain.cc
bool Explain_table_base::explain_extra_common(const SQL_SELECT *select,
                                              const JOIN_TAB *tab,
                                              int quick_type,
                                              uint keyno)
{
  if (((keyno != MAX_KEY &&
        keyno == table->file->pushed_idx_cond_keyno &&
        table->file->pushed_idx_cond) ||
       (tab && tab->cache_idx_cond)))
  {
    StringBuffer<160> buff(cs);
    if (fmt->is_hierarchical())
    {
      if (table->file->pushed_idx_cond)
        table->file->pushed_idx_cond->print(&buff, cond_print_flags);
      else
        tab->cache_idx_cond->print(&buff, cond_print_flags);
    }
    if (push_extra(ET_USING_INDEX_CONDITION, buff))
    return true;
  }

```

