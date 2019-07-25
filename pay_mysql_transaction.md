# MySQL transaction

```
mysql> select * from trade;
+----+-----------------+--------+
| id | trade_id        | status |
+----+-----------------+--------+
|  1 | 201901171900001 |      0 |
+----+-----------------+--------+
1 row in set (0.00 sec)

mysql> select * from trade_history;
+----+-----------------+--------+---------------------+
| id | trade_id        | status | create_time         |
+----+-----------------+--------+---------------------+
|  1 | 201901171900001 |      0 | 2019-01-17 19:15:43 |
+----+-----------------+--------+---------------------+
1 row in set (0.00 sec)
```

```
To start mysqld at boot time you have to copy
support-files/mysql.server to the right place for your system

PLEASE REMEMBER TO SET A PASSWORD FOR THE MySQL root USER !
To do so, start the server, then issue the following commands:

  /opt/mysql-5.6.42/bin/mysqladmin -u root password 'new-password'
  /opt/mysql-5.6.42/bin/mysqladmin -u root -h B000000134469B password 'new-password'

Alternatively you can run:

  /opt/mysql-5.6.42/bin/mysql_secure_installation

which will also give you the option of removing the test
databases and anonymous user created by default.  This is
strongly recommended for production servers.

See the manual for more instructions.

You can start the MySQL daemon with:

  cd . ; /opt/mysql-5.6.42/bin/mysqld_safe &

You can test the MySQL daemon with mysql-test-run.pl

  cd mysql-test ; perl mysql-test-run.pl

Please report any problems at http://bugs.mysql.com/

The latest information about MySQL is available on the web at

  http://www.mysql.com

Support MySQL by buying support/licenses at http://shop.mysql.com

New default config file was created as /opt/mysql-5.6.42/my.cnf and
will be used by default by the server when you start it.
You may edit this file to change server settings

```

```
show engine innodb status;
```

## Thread 1
```
mysql> START TRANSACTION;
Query OK, 0 rows affected (0.00 sec)

mysql> UPDATE trade SET status = 1 WHERE trade_id = '201901171900001';
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> INSERT INTO trade_history SET trade_id = '201901171900001', status = 1;
Query OK, 1 row affected (0.00 sec)

mysql> SELECT * FROM trade;
+----+-----------------+--------+
| id | trade_id        | status |
+----+-----------------+--------+
|  1 | 201901171900001 |      1 |
+----+-----------------+--------+
1 row in set (0.00 sec)

mysql> SELECT * FROM trade_history;
+----+-----------------+--------+---------------------+
| id | trade_id        | status | create_time         |
+----+-----------------+--------+---------------------+
|  1 | 201901171900001 |      0 | 2019-01-17 19:15:43 |
|  2 | 201901171900001 |      1 | 2019-01-17 19:25:30 |
+----+-----------------+--------+---------------------+
2 rows in set (0.00 sec)
```