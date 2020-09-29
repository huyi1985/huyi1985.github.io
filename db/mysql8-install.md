

https://dev.mysql.com/doc/refman/8.0/en/source-installation-prerequisites.html

MySQL Source-Configuration Options

https://dev.mysql.com/doc/refman/8.0/en/source-configuration-options.html

https://dev.mysql.com/doc/refman/8.0/en/compilation-problems.html

```
shell> make clean
shell> rm CMakeCache.txt
```

交换区
```
fallocate -l 2G /swapfile
chmod 0600 /swapfile
mkswap /swapfile
swapon /swapfile
```

Disk
https://www.vagrantup.com/docs/disks/usage	Resizing your primary disk 
https://qiita.com/yut_h1979/items/c84c490053877beee5c1	Vagrantfileに一行書くだけでVMのディスク容量を増やす方法

```
apt install -y cmake g++ libssl-dev libncurses5-dev pkg-config gdb

shell> cd mysql-VERSION
shell> mkdir bld
shell> cd bld
shell> cmake -DCMAKE_INSTALL_PREFIX=/opt/mysql-8.0.20 -DWITH_DEBUG=1 -DWITH_BOOST=../boost -DMYSQL_DATADIR=/opt/mysql-8.0.20/data .. 
shell> make
shell> make install
```

`cmake -DCMAKE_INSTALL_PREFIX=/opt/mysql-8.0.12 -DWITH_DEBUG=1 -DWITH_BOOST=../boost -DMYSQL_DATADIR=/opt/mysql-8.0.12/data ..`


```
# Postinstallation setup
shell> cd /usr/local/mysql
shell> mkdir mysql-files
shell> chown mysql:mysql mysql-files
shell> chmod 750 mysql-files

shell> bin/mysqld --initialize --user=mysql
shell> bin/mysql_ssl_rsa_setup
shell> bin/mysqld_safe --user=mysql &

[Note] [MY-010454] [Server] A temporary password is generated for root@localhost: TkwL_dKkt0(P
```

```mysql
alter user root@localhost identified by '123456';
```