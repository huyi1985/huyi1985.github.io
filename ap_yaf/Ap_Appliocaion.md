# Ap_Appliocaion

## issue 1 Couldn't find bootstrap file

```
Ap_Application::bootstrap(): Couldn't find bootstrap file <path>

$config = array(
    "application" => array(
        "directory" => realpath(dirname(__FILE__)) . "/application",
    ),
);

$objApplication = new Ap_Application($config);
$objResponse = $objApplication->bootstrap()->run();
```

```
zim_ap_application_bootstrap

/** {{{ proto public Ap_Application::bootstrap(void)
*/
PHP_METHOD(ap_application, bootstrap) {

bootstrap_path = strpprintf(0, "%s%c%s.%s",
	ZSTR_VAL(AP_G(directory)), 
	DEFAULT_SLASH, 				// /
	AP_DEFAULT_BOOTSTRAP, 		// Bootstrap
	ZSTR_VAL(AP_G(ext))			// php
);
gdb > p *bootstrap_path->val@bootstrap_path->len
$6 = "/home/work/duer/skill-pay/application/Bootstrap.php"

AP_G(directory)读取的就是$config['application']['directory']
```

``` 
/main/php.h
#define PHP_METHOD              ZEND_METHOD

/Zend/zend_API.h
#define ZEND_METHOD(classname, name)	ZEND_NAMED_FUNCTION(ZEND_MN(classname##_##name))
#define ZEND_MN(name) zim_##name
#define ZEND_NAMED_FUNCTION(name)		void name(INTERNAL_FUNCTION_PARAMETERS)
```

## issue 2 load ~/odp/conf/app/<appname>/global.conf
```
bd_conf exetension

static void init_global_conf_tree()
{
    /* 获取全局配置树 persist_conf 如果不存在则创建他 */
    if (NULL == g_config) {
        ...
        //global_path = ${ODP_ROOT}/conf/global.conf
        snprintf(g_config->root->global_path, sizeof(g_config->root->global_path), "%s/global.conf", CONF_G(conf_path));
        g_config->root->name[0] = 0;
    }
}
```


