# PHP refcount

https://github.com/pangudashu/php7-internal/blob/master/7/var.md

http://www.phpinternalsbook.com/zvals/basic_structure.html


## Macro

Zend/zend_types.h

```
#define Z_REFCOUNTED(zval)                      ((Z_TYPE_FLAGS(zval) & IS_TYPE_REFCOUNTED) != 0)
#define Z_REFCOUNTED_P(zval_p)          Z_REFCOUNTED(*(zval_p))


#define Z_REFCOUNT_P(pz)                        zval_refcount_p(pz)
#define Z_SET_REFCOUNT_P(pz, rc)        zval_set_refcount_p(pz, rc)
#define Z_ADDREF_P(pz)                          zval_addref_p(pz)
#define Z_DELREF_P(pz)                          zval_delref_p(pz)

#define Z_REFCOUNT(z)                           Z_REFCOUNT_P(&(z))
#define Z_SET_REFCOUNT(z, rc)           Z_SET_REFCOUNT_P(&(z), rc)
#define Z_ADDREF(z)                                     Z_ADDREF_P(&(z))
#define Z_DELREF(z)                                     Z_DELREF_P(&(z))

#define Z_TRY_ADDREF_P(pz) do {         \
        if (Z_REFCOUNTED_P((pz))) {             \
                Z_ADDREF_P((pz));                       \
        }                                                               \
} while (0)

#define Z_TRY_DELREF_P(pz) do {         \
        if (Z_REFCOUNTED_P((pz))) {             \
                Z_DELREF_P((pz));                       \
        }                                                               \
} while (0)

#define Z_TRY_ADDREF(z)                         Z_TRY_ADDREF_P(&(z))
#define Z_TRY_DELREF(z)                         Z_TRY_DELREF_P(&(z))

static zend_always_inline uint32_t zval_refcount_p(zval* pz) {
        ZEND_ASSERT(Z_REFCOUNTED_P(pz) || Z_IMMUTABLE_P(pz) || Z_SYMBOLTABLE_P(pz));
        return GC_REFCOUNT(Z_COUNTED_P(pz));
}

static zend_always_inline uint32_t zval_set_refcount_p(zval* pz, uint32_t rc) {
        ZEND_ASSERT(Z_REFCOUNTED_P(pz));
        return GC_REFCOUNT(Z_COUNTED_P(pz)) = rc;
}

static zend_always_inline uint32_t zval_addref_p(zval* pz) {
        ZEND_ASSERT(Z_REFCOUNTED_P(pz));
        return ++GC_REFCOUNT(Z_COUNTED_P(pz));
}

static zend_always_inline uint32_t zval_delref_p(zval* pz) {
        ZEND_ASSERT(Z_REFCOUNTED_P(pz));
        return --GC_REFCOUNT(Z_COUNTED_P(pz));
}
```

## 为什么以及什么时候操作引用计数

7.7.4 https://github.com/pangudashu/php7-internal/blob/master/7/var.md

```
function test($arr){
    return $arr;
}

$a = array(1,2);
$b = test($a);


```

如果把函数test()用内部函数实现，这个函数接受了一个PHP用户空间传入的数组参数，然后又返回并赋值给了PHP用户空间的另外一个变量，这个时候就需要增加传入数组的refcount。

因为这个数组由PHP用户空间分配，函数调用前refcount=1，传到内部函数时相当于赋值给了函数的参数，因此**refcount增加了1变为2，这次增加在函数执行完释放参数时会减掉**，等返回并赋值给$b后此时共有两个变量指向这个数组，所以**内部函数需要增加refcount，增加的引用是给返回值的**。test()翻译成内部函数：

> “refcount增加了1变为2”应该是这个意思吧：开发者需要使refcount增加1

```
PHP_FUNCTION(test)
{   
    zval    *arr;

    if(zend_parse_parameters(ZEND_NUM_ARGS(), "a", &arr) == FAILURE){
        RETURN_FALSE;
    }
    //如果注释掉下面这句将导致core dumped
    Z_TRY_ADDREF_P(arr);
    RETURN_ARR(Z_ARR_P(arr));
} 
```

要明确的一点是引用计数是用来解决多个变量指向同一个value问题的，所以在PHP中来回传递zval的时候就需要考虑下是不是要修改引用计数，下面总结下PHP中常见的会对引用计数进行操作的情况：

(1)变量赋值: 变量赋值是最常见的情况，一个用到引用计数的变量类型在初始赋值时其refcount=1，如果后面把此变量又赋值给了其他变量那么就会相应的增加其引用计数
(2)数组操作： 如果把一个变量插入数组中那么就需要增加这个变量的引用计数，如果要删除一个数组元素则要相应的减少其引用
(3)函数调用： 传参实际可以当做普通的变量赋值，将调用空间的变量赋值给被调函数空间的变量，函数返回时会销毁函数空间的变量，这时又会减掉传参的引用，这两个过程由内核完成，不需要扩展自己处理
(4)成员属性： 当把一个变量赋值给对象的成员属性时需要增加引用计数