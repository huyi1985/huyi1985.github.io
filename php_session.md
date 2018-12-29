# php_seesion

php string interval
smart_str_appends

PS: 可能是**P**hp **S**ession Gloabls的意思
```c
./session/php_session.h:187:#define PS(v) (ps_globals.v)

typedef struct _php_ps_globals {
}
```

```c
../Zend/zend_globals_macros.h:47:# define EG(v) (executor_globals.v)

../Zend/zend_compile.c:105:ZEND_API zend_executor_globals executor_globals;
```

```c
// Strategy Pattern
type ps_module

// ps_file extends ps_module, mod_files.c
// ps_file has metadata:
struct {
    int fd;
    char *lastkey;
    char *basedir;
    size_t basedir_len;
    size_t dirdepth;
    size_t st_size;
    int filemode;
}

#define PS_GET_MOD_DATA() *mod_data
#define PS_SET_MOD_DATA(a) *mod_data = (a)
```

```c
./main/SAPI.h:141:# define SG(v) TSRMG(sapi_globals_id, sapi_globals_struct *, v)
./main/SAPI.h:144:# define SG(v) (sapi_globals.v)

./main/php_globals.h:29:# define PG(v) TSRMG(core_globals_id, php_core_globals *, v)
./main/php_globals.h:32:# define PG(v) (core_globals.v)
```

close seesion tmp file
```c
static PHP_RSHUTDOWN_FUNCTION(session)
{
	int i;

	php_session_flush(TSRMLS_C);
	php_rshutdown_session_globals(TSRMLS_C);

	/* this should NOT be done in php_rshutdown_session_globals() */
	for (i = 0; i < 6; i++) {
		if (PS(mod_user_names).names[i] != NULL) {
			zval_ptr_dtor(&PS(mod_user_names).names[i]);
			PS(mod_user_names).names[i] = NULL;
		}
	}

	return SUCCESS;
}
```
