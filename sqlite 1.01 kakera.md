# sqlite 1.01 kakera

## Token table换Table

```
Token *pTableName
->
Table *pTab;
```


```
void sqliteDeleteFrom(
  Parse *pParse,         /* The parser context */
  Token *pTableName,     /* The table from which we should delete things */
  Expr *pWhere           /* The WHERE clause.  May be null */
)

	Table *pTab;
	pTab = sqliteFindTable(pParse->db, pTabList->a[i].zName);
```

```
void sqliteInsert(
  Parse *pParse,        /* Parser context */
  Token *pTableName,    /* Name of table into which we are inserting */
  ExprList *pList,      /* List of values to be inserted */
  Select *pSelect,      /* A SELECT statement to use as the data source */
  IdList *pColumn       /* Column names corresponding to IDLIST. */
)

	char *zTab;           /* Name of the table into which we are inserting */
	
	zTab = sqliteTableNameFromToken(pTableName);
	pTab = sqliteFindTable(pParse->db, zTab);
```

```
void sqliteUpdate(
  Parse *pParse,         /* The parser context */
  Token *pTableName,     /* The table in which we should change things */
  ExprList *pChanges,    /* Things to be changed */
  Expr *pWhere           /* The WHERE clause.  May be null */
){

	Table *pTab;
	pTab = sqliteFindTable(pParse->db, pTabList->a[i].zName);
```

