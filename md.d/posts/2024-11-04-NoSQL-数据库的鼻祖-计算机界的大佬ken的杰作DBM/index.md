---
title: NoSQL 数据库的鼻祖——计算机界的大佬ken的杰作DBM
date: '2024-11-04'
---

# NoSQL 数据库的鼻祖——计算机界的大佬ken的杰作DBM

进入互联网和大数据时代后，数据的快速增长和多样化使得传统关系型数据库（MySQL、SQL Server 等）面临诸多挑战。在这一背景下，诞生了 Redis、MemCache 等键值存储型 NoSQL 数据库。

> NoSQL 其实没有严格的定义，它可以是 **N**ot **O**nly **SQL**，强调这类数据库是传统 SQL 数据库的升级版，可以适用于更多场景；也可以是 **NO**t **SQL**，表示这些数据库有别于传统数据库，不依赖 SQL 查询语言和关系模型，能够更加灵活地处理大量非结构化或半结构化数据。

本文将要介绍的 **DBM 可谓是键值存储型 NoSQL 数据库的鼻祖**。

DBM（**D**ata**B**ase **M**anager的缩写）是来自 Unix 世界的键值数据库。1970 年代，随着 Unix 操作系统的发展，越来越多的应用程序需要高效地存储和检索数据。为了解决这个问题，计算机界的大佬 Ken Thompson（肯·汤普逊）亲自编写了一个以键值对方式存储数据的小型数据库系统 DBM。DBM 的目标是实现一个轻量级、快速的数据存储系统，以适用于 Unix 环境中常见的数据管理任务，如用户信息、系统配置等。

![[dbm.c.png]]

DBM 只是一个简单的**数据库引擎**，仅以代码库（library）的形式向用户（程序员）提供一系列API，并不支持 SQL 语句（所以说它是 NoSQL 的一种）。我们可以将 DBM 的数据库看作是存储在硬盘上的哈希表。

> **数据库引擎（database engine）**
> 
> 也称为存储引擎，是支持数据库管理系统 （DBMS）对数据库（文件）进行 CRUD 的底层组件。大多数数据库管理系统都包含特定的 API，允许用户通过 API 直接与其底层的存储引擎交互。

Ken Thompson 可是计算机科学领域的一位传奇人物，黑客文化圈通常称他为 ***ken***。
他不但是 Unix 操作系统的共同创始人之一，也是C语言的前身——B语言与C语言的现代化演进——Go 语言的开发者。此外，他还参与过正则表达式和 UTF-8 编码的设计。

![](img1.png)

没想到大佬在数据库系统方面还有作品啊。

DBM 现在也泛指一系列由 Ken 的原始 DBM 派生而来的数据库，如 ndbm、gdbm、lmdb 等，有时也指用于操作这些数据库的代码库（library）或例程（routine）。

关于 ndbm 这个派生版本还有个冷笑话，

> NDBM 虽然叫 **New** DBM，但也颇有历史了。就好像那不勒斯(Neapolis)这座城市，虽然已有 2700 余年的历史，字面上却是**新**城（New Town）的意思。

DBM 作为最早的键值数据库之一，影响了后来的许多数据库系统。特别是可谓部署范围最广、安装次数最多（据说安装量排名世界第二）的数据库引擎 SQLite。SQLite 的第 1 版只不过是在 DBM 的衍生版本 gdbm 上套了个壳。SQLite 第 1 版的 README 文件中这样写道：

> SQLite: An SQL Database Built Upon GDBM

----


> Although NDBM is now old - like the city named New Town ('Neapolis') by the Greeks in about 600BC and still called Naples today - it remains the baseline DBM.
>
> —— Kew, Nick (2007). *The Apache Modules Book: Application Development with Apache*. Prentice Hall Professional. ISBN 9780132704502. p.80


下面我们使用“世界上最好的语言”PHP来体验一下 DBM。之所以使用PHP，是因为PHP内置了一个叫做DBA（[https://www.php.net/manual/en/book.dba.php](https://www.php.net/manual/en/book.dba.php)）的扩展，只是估计很少有人用过这个扩展吧。

```bash
$ php -r "var_dump(dba_handlers());" 
array(5) {
  [0]=>
  string(4) "ndbm"
  [1]=>
  string(3) "cdb"
  [2]=>
  string(8) "cdb_make"
  [3]=>
  string(7) "inifile"
  [4]=>
  string(8) "flatfile"
}
```

首先通过`dba_handlers()`函数来看一看系统支持的DBM，这里的 ndbm 和 cdb 都派生自 DBM。接下来我们再通过一小段代码，看看如何对DBM（ndbm）进行增删改查。

```php
<?php
$id = dba_open("/tmp/test.db", "n", "ndbm"); // mode `n` for create, truncate and read/write access
if (!$id) {
    echo "dba_open failed\n";
    exit;
}

dba_replace("key", "This is an example!", $id);
if (dba_exists("key", $id)) {
    echo dba_fetch("key", $id), PHP_EOL;
    dba_delete("key", $id);
}
var_dump(dba_fetch("key", $id));

dba_close($id);
```

`dba_open()`的第3个参数是“DBM系”数据库的名字（在PHP DBA扩展中叫做handler）。从设计模式的角度看，DBA相当于接口，handler相当于实现类。从MySQL架构的角度看，DBA相当于MySQL Server，handler相当于Pluggable Storage Engine。

在本例中，我们使用`ndbm`这个handler。执行结果如下所示。

```bash
/tmp $ php dbm.php
This is an example!
bool(false)
```

我们还可以通过`strings`命令查看存储在DBM数据库中的数据。

```php
// $id resource returned from `dba_open`
dba_replace("key", "This is an example!", $id);
dba_replace("foo", "bar", $id);
dba_sync($id);
```

```bash
$ strings test.db.db
barfoo
This is an example!key
```

关于ndbm这个名字还有个冷笑话，

> Although NDBM is now old - like the city named New Town ('Neapolis') by the Greeks in about 600BC and still called Naples today - it remains the baseline DBM.
>
> —— Kew, Nick (2007). *The Apache Modules Book: Application Development with Apache*. Prentice Hall Professional. ISBN 9780132704502. p.80

NDBM虽然叫**New** DBM，但也颇有历史了。就好像那不勒斯这座城市，虽然已有2700余年的历史，字面上却是**新**城的意思。



