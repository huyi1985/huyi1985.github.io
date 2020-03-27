# Why does MySQL use B-tree

Version 1.0.1 https://www.sqlite.org/src/info/e8521fc10dcfa02f

```
SQLite: An SQL Database Built Upon GDBM
```

```c
/*
** Fetch a single record from an open cursor.  Return 1 on success
** and 0 on failure.
*/
int sqliteDbbeFetch(DbbeCursor *pCursr, int nKey, char *pKey){
  datum key;
  key.dsize = nKey;
  key.dptr = pKey;
  datumClear(&pCursr->key);
  datumClear(&pCursr->data);
  if( pCursr->pFile && pCursr->pFile->dbf ){
    pCursr->data = gdbm_fetch(pCursr->pFile->dbf, key);
  }
  return pCursr->data.dptr!=0;
}

...
  
/*
** Write an entry into the table.  Overwrite any prior entry with the
** same key.
*/
int sqliteDbbePut(DbbeCursor *pCursr, int nKey,char *pKey,int nData,char *pData){
  datum data, key;
  int rc;
  if( pCursr->pFile==0 || pCursr->pFile->dbf==0 ) return SQLITE_ERROR;
  data.dsize = nData;
  data.dptr = pData;
  key.dsize = nKey;
  key.dptr = pKey;
  rc = gdbm_store(pCursr->pFile->dbf, key, data, GDBM_REPLACE);
  if( rc ) rc = SQLITE_ERROR;
  datumClear(&pCursr->key);
  datumClear(&pCursr->data);
  return rc;
}
```



https://www.sqlite.org/src/info/bdb1c425f577d455

Begin adding BTree code (CVS 213)