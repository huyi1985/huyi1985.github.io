# Install sqlite-1.0.1 3.0.2

https://www.sqlite.org/src/info/26a559b65835d3da

https://ja.stackoverflow.com/questions/54622/%EF%BC%91%EF%BC%99%E5%B9%B4%E5%89%8D%E3%81%AB%E3%83%AA%E3%83%AA%E3%83%BC%E3%82%B9%E3%81%95%E3%82%8C%E3%81%9Fsqlite-1-0-1%E3%81%AF%E3%81%A9%E3%81%AE%E3%82%88%E3%81%86%E3%81%AB%E3%81%97%E3%81%A6%E3%82%B3%E3%83%B3%E3%83%91%E3%82%A4%E3%83%AB%E3%81%97%E3%81%BE%E3%81%99%E3%81%8B/54623#54623

`patch -F 3 < 7902e477.patch`

https://www.sqlite.org/src/raw/tool/lemon.c?name=14fedcde9cf70aa6040b89de164cf8f56f92a4b9


```bash
wget "https://www.sqlite.org/src/tarball/e8521fc1/SQLite-e8521fc1.tar.gz"
tar xzvf SQLite-e8521fc1.tar.gz
# mkdir bld && cd bld
mkdir sqlite-1.0.1 && cd sqlite-1.0.1 
../SQLite-e8521fc1/configure --prefix=/opt/sqlite-1.0.1 --with-tcl=no
```

```
gcc -std=c89

/usr/lib/gcc/i386-redhat-linux/3.4.2/include/varargs.h:4:2: #error "GCC no longer implements <varargs.h>."
/usr/lib/gcc/i386-redhat-linux/3.4.2/include/varargs.h:5:2: #error "Revise your code to use <stdarg.h>."
```

```
wget https://www.sqlite.org/src/raw/tool/lemon.c?name=14fedcde9cf70aa6040b89de164cf8f56f92a4b9 -Olemon.c.patch
```

```
configure: error:
**************************************************************************
** This program may not be compiled in the same directory that contains **
** the configure script or any subdirectory of that directory.   Rerun  **
** the configure script from a directory that is separate from the      **
** source tree.                                                         **
**                                                                      **
** See the README file for additional information.                      **
**************************************************************************
```

```
mkdir bld && cd bld
tar xzf sqlite.tar.gz    ;#  Unpack the source tree into "sqlite"
mkdir bld                ;#  Build will occur in a sibling directory
cd bld                   ;#  Change to the build directory
../sqlite/configure      ;#  Run the configure script
make                     ;#  Run the makefile.
```

```
../sqlite/configure --prefix=/opt/sqlite-1.0.1 --with-tcl=no
../SQLite-e8521fc1/configure --prefix=/opt/sqlite-1.0.1 --with-tcl=no
make CFLAGS=-g -O0
```



> Now, we compile the program using the GNU C compiler, GCC. We pass the `-gdwarf-2` *and* `-g3` flags to ensure the compiler includes information about preprocessor macros in the debugging information.

https://sourceware.org/gdb/onlinedocs/gdb/Macros.html



## 数据结构

表示SQL语句中的 部分

Token

Expr: WHERE clause, HAVING clause

ExprList: ORDER BY clause, GROUP BY clause, SELECT后面的字段列表 

IdList: FROM table_list,

Table

Index



## RedHat 8

OK!



RedHat 6.2

http://archive.download.redhat.com/pub/redhat/linux/

https://soft.lafibre.info/

Networking Config

```ini
[root@redhat62 /tmp]# tail -n +1 /etc/sysconfig/network-scripts/ifcfg-*
==> /etc/sysconfig/network-scripts/ifcfg-eth0 <==
DEVICE=eth0
ONBOOT=yes
BOOTPROTO=dhcp
NAME=eth0

==> /etc/sysconfig/network-scripts/ifcfg-eth1 <==
DEVICE=eth1
IPADDR=192.168.56.100
NETMASK=255.255.255.0
NETWORK=192.168.56.0
BROADCAST=192.168.56.255
ONBOOT=yes
BOOTPROTO=dhcp
NAME=eth1

==> /etc/sysconfig/network-scripts/ifcfg-lo <==
DEVICE=lo
IPADDR=127.0.0.1
NETMASK=255.0.0.0
NETWORK=127.0.0.0
# If you're having problems with gated making 127.0.0.0/8 a martian,
# you can change this to something else (255.255.255.255, for example)
BROADCAST=127.255.255.255
ONBOOT=yes
```



rpm：http://rpm.pbone.net/index.php3



## Lexer & Parser

| nth-Byte  | 0-5    | 6    | 7    | 8    | 9-12 | 13   | 14-15 |
| --------- | ------ | ---- | ---- | ---- | ---- | ---- | ----- |
|           | SELECT |      | 1    |      | FROM |      | t1    |
| TokenType | 61     | 65   | 40   | 65   | 28   | 65   | 35    |



```
Breakpoint 9, sqliteParser (yyp=0x806ede8, yymajor=61, yyminor={z = 0xbffffab7 "SELECT 1 FROM t1", n = 6}, pParse=0xbffff410) at parse.c:4685
(gdb) c
Breakpoint 9, sqliteParser (yyp=0x806ede8, yymajor=40, yyminor={z = 0xbffffabe "1 FROM t1", n = 1}, pParse=0xbffff410) at parse.c:4685
(gdb) c
Breakpoint 9, sqliteParser (yyp=0x806ede8, yymajor=28, yyminor={z = 0xbffffac0 "FROM t1", n = 4}, pParse=0xbffff410) at parse.c:4685
(gdb) c
Breakpoint 9, sqliteParser (yyp=0x806ede8, yymajor=35, yyminor={z = 0xbffffac5 "t1", n = 2}, pParse=0xbffff410) at parse.c:4685
(gdb) c

Breakpoint 9, sqliteParser (yyp=0x806ede8, yymajor=0, yyminor={z = 0xbffffac5 "t1", n = 2}, pParse=0xbffff410) at parse.c:4685
```



## GDB

```
b sqlite3_exec
```

```
sqlite3_exec
	|- sqlite3_prepare // init pStmt
		|- sqlite3RunParser
	|- sqlite3_step
		|- sqlite3VdbeExec
```


### pStmt life
```
int sqlite3_exec(
	sqlite *db,                 /* The database on which the SQL executes */
	const char *zSql,           /* The SQL to be executed */
	sqlite_callback xCallback,  /* Invoke this callback routine */
	void *pArg,                 /* First argument to xCallback() */
	char **pzErrMsg             /* Write error messages here */
){
	sqlite3_stmt *pStmt = 0;
	
	rc = sqlite3_prepare(db, zSql, -1, &pStmt, &zLeftover);
	
	
	if ( rc==SQLITE_OK ) {
		*ppStmt = (sqlite3_stmt*)sParse.pVdbe;                                                                                                                      
	} else if( sParse.pVdbe ) {
		sqlite3_finalize((sqlite3_stmt*)sParse.pVdbe);                                                                                                              
	}
	
```

```
sqlite3_prepare() {
	sqlite3RunParser(&sParse, zSql, &zErrMsg);

```

### Open Master db
```
case OP_Transaction:
	 int i = pOp->p1;
	 Btree *pBt;
	 
	 pBt = db->aDb[i].pBt;
	 
	 int sqlite3BtreeBeginTrans(Btree *pBt, int wrflag){
```

```
int sqlite3BtreeCursor(
```


* sqlite3SafetyOn


## SELECT语句是如何执行的
命令式、声明式


https://cdimage.debian.org/mirror/cdimage/archive/

ssh -oKexAlgorithms=+diffie-hellman-group1-sha1 -oCiphers=+aes128-cbc huyi@192.168.58.3

> Change lemon to use <stdarg.h> instead of <varargs.h> because GCC no longer supports varargs.h. Tickets #288 and #280. Ironically, lemon originally used varargs.h because stdarg.h was not supported by the compiler I was using in 1989 (which was gcc if I recall correctly.) (CVS 905)

### 最简单的SELECT语句

`SELECT * FROM t1`





## INSERT语句是如何执行的

### 最简单的INSERT语句

`INSERT INTO t1 VALUES (10)`

no idList



```c
// INSERT INTO <table> <IdList> VALUES <ExprList>
// 省略1、各种检查逻辑（以注释形式给出）；2、索引逻辑

void sqliteInsert(
  Parse *pParse,        /* Parser context */
  Token *pTableName,    /* Name of table into which we are inserting */
  ExprList *pList,      /* List of values to be inserted */
  Select *pSelect,      /* A SELECT statement to use as the data source */
  IdList *pColumn       /* Column names corresponding to IDLIST. */
){
  Table *pTab;          /* The table to insert into */
  char *zTab;           /* Name of the table into which we are inserting */
  int i;                /* Loop counters */
  Vdbe *v;              /* Generate code into this virtual machine */
  int nColumn;          /* Number of columns in the data */
  int base;             /* First available cursor */

  /* Locate the table into which we will be inserting new information. */
  zTab = sqliteTableNameFromToken(pTableName);
  pTab = sqliteFindTable(pParse->db, zTab);
  sqliteFree(zTab);
    
  /* Allocate a VDBE */
  v = sqliteGetVdbe(pParse);

  nColumn = pList->nExpr;
  
  /* Make sure the number of columns in the source data matches the number
  ** of columns to be inserted into the table.
  */
  if( pColumn==0 && nColumn!=pTab->nCol ) {
      // error_string = "table <table_name> has <Num1> columns but <Num2> values were supplied"
    pParse->nErr++;
    goto insert_cleanup;
  }

  base = pParse->nTab;
  sqliteVdbeAddOp(v, OP_Open, base, 1, pTab->zName, 0);
    
  /* Create a new entry in the table and fill it with data. */
  sqliteVdbeAddOp(v, OP_New, 0, 0, 0, 0);
    
  for(i=0; i<pTab->nCol; i++) {
    sqliteExprCode(pParse, pList->a[i].pExpr);
  }
    
  sqliteVdbeAddOp(v, OP_MakeRecord, pTab->nCol, 0, 0, 0);
  sqliteVdbeAddOp(v, OP_Put, base, 0, 0, 0);
    
insert_cleanup:
  if( pList ) sqliteExprListDelete(pList);
  if( pSelect ) sqliteSelectDelete(pSelect);
  sqliteIdListDelete(pColumn);

```

