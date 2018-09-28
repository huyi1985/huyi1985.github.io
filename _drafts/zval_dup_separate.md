> https://unix.stackexchange.com/questions/22926/where-do-executables-look-for-shared-objects-at-runtime

> In a nutshell, when it's looking for a dynamic library (.so file) the linker tries:

> - directories listed in the LD_LIBRARY_PATH environment variable (DYLD_LIBRARY_PATH on OSX);
> - directories listed in the executable's rpath;
> - directories on the system search path, which (on Linux at least) consists of the entries in /etc/ld.so.conf plus /lib and /usr/lib.

> ./embed: error while loading shared libraries: libphp7.so: cannot open shared object file: No such file or directory

## Makefile
```makefile
PREFIX = /home/huyi
CC = gcc
CFLAGS = -I$(PREFIX)/usr/local/include/php/ \
         -I$(PREFIX)/usr/local/include/php/main \
         -I$(PREFIX)/usr/local/include/php/Zend \
         -I$(PREFIX)/usr/local/include/php/TSRM \
         -Wall -g
LDFLAGS = -L$(PREFIX)/usr/local/lib -lphp7

ALL:
        $(CC) -o embed embed.c $(CFLAGS) $(LDFLAGS)
```

```bash
export LD_LIBRARY_PATH=/home/huyi/usr/local/lib:$LD_LIBRARY_PATH
```

## 扩展中函数的返回值
## RETURN_FALSE

```
// Zend/zend_API.h

#define RETURN_FALSE    { RETVAL_FALSE; return; }

#define RETVAL_FALSE    ZVAL_FALSE(return_value)
```

```
// Zend/zend_types.h

#define ZVAL_FALSE(z) do {          \
    Z_TYPE_INFO_P(z) = IS_FALSE;    \
} while (0)
```

// return_value在哪里定义的？

## ZVAL_DUP

```
// Zend/zend_types.h

#define ZVAL_DUP(z, v)                                              \
do {                                                                \
    zval *_z1 = (z);                                                \
    const zval *_z2 = (v);                                          \
    zend_refcounted *_gc = Z_COUNTED_P(_z2);                        \
    uint32_t _t = Z_TYPE_INFO_P(_z2);                               \
    ZVAL_COPY_VALUE_EX(_z1, _z2, _gc, _t);                          \
                
    if ((_t & ((IS_TYPE_REFCOUNTED|IS_TYPE_COPYABLE) << Z_TYPE_FLAGS_SHIFT)) != 0) { \
        if ((_t & (IS_TYPE_COPYABLE << Z_TYPE_FLAGS_SHIFT)) != 0) { \
            _zval_copy_ctor_func(_z1 ZEND_FILE_LINE_CC);            \
        } else {                                                    \
            GC_REFCOUNT(_gc)++;                                     \
        }                                                           \
    }                                                               \
} while (0)
```

## SEPARATE_ZVAL
```
#define SEPARATE_ZVAL(zv) do {                                      \
    zval *_zv = (zv);                                               \
    if (Z_REFCOUNTED_P(_zv) ||                                      \
        Z_COPYABLE_P(_zv)) {                                        \
        if (Z_REFCOUNT_P(_zv) > 1) {                                \
            if (Z_COPYABLE_P(_zv)) {                                \
                if (Z_REFCOUNTED_P(_zv)) {                          \
                    Z_DELREF_P(_zv);                                \
                }                                                   \
                zval_copy_ctor_func(_zv);                           \
            } else if (Z_ISREF_P(_zv)) {                            \
                Z_DELREF_P(_zv);                                    \
                ZVAL_DUP(_zv, Z_REFVAL_P(_zv));                     \
            }                                                       \
        }                                                           \
    }                                                               \
} while (0)
```

## ZVAL_DEREF

## SEPARATE_ZVAL_NOREF



