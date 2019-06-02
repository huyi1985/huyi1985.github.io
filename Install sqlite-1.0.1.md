# Install sqlite-1.0.1 3.0.2

https://www.sqlite.org/src/info/26a559b65835d3da

https://ja.stackoverflow.com/questions/54622/%EF%BC%91%EF%BC%99%E5%B9%B4%E5%89%8D%E3%81%AB%E3%83%AA%E3%83%AA%E3%83%BC%E3%82%B9%E3%81%95%E3%82%8C%E3%81%9Fsqlite-1-0-1%E3%81%AF%E3%81%A9%E3%81%AE%E3%82%88%E3%81%86%E3%81%AB%E3%81%97%E3%81%A6%E3%82%B3%E3%83%B3%E3%83%91%E3%82%A4%E3%83%AB%E3%81%97%E3%81%BE%E3%81%99%E3%81%8B/54623#54623

`patch -F 3 < 7902e477.patch`

https://www.sqlite.org/src/raw/tool/lemon.c?name=14fedcde9cf70aa6040b89de164cf8f56f92a4b9


```
wget "https://www.sqlite.org/src/tarball/e8521fc1/SQLite-e8521fc1.tar.gz"
tar xzvf SQLite-e8521fc1.tar.gz
mkdir bld && cd bld
../SQLite-e8521fc1/configure --prefix=/opt/sqlite-1.0.1 --with-tcl=no

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
make CFLAGS=-g
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


Change lemon to use <stdarg.h> instead of <varargs.h> because GCC no longer supports varargs.h. Tickets #288 and #280. Ironically, lemon originally used varargs.h because stdarg.h was not supported by the compiler I was using in 1989 (which was gcc if I recall correctly.) (CVS 905)