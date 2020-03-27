# Install from Source

https://dev.mysql.com/doc/mysql-sourcebuild-excerpt/5.5/en/installing-source-distribution.html#installing-source-distribution-install-distribution

https://dev.mysql.com/doc/refman/5.6/en/installing-source-distribution.html 

cmake options

```
s -D MYSQL_MAINTAINER_MODE=0

# using-g3-or-ggdb3-or-gdwarf-4

make CFLAGS='-Wno-error' CXXFLAGS="-Wno-error"


cd /opt/mysql-5.6.43/scripts
./mysql_install_db --basedir=/opt/mysql-5.6.43 --user=root

cat /opt/mysql-5.6.43/start_mysql.sh
#!/bin/bash
/opt/mysql-5.6.43/bin/mysqld --user=root
```

不关闭`MYSQL_MAINTAINER_MODE` cmake会在FLAGS后加上`-Werror`

