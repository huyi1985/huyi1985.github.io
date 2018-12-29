# ap bug

## gdb

controller = zend_read_property(ap_request_ce, request, ZEND_STRL(AP_REQUEST_PROPERTY_NAME_CONTROLLER), 1, NULL);

req_uri = zend_string_init(Z_STRVAL_P(zuri) + Z_STRLEN_P(base_uri), Z_STRLEN_P(zuri) - Z_STRLEN_P(base_uri), 0);

```
b zim_ap_application___construct

PHP_METHOD(ap_application, __construct) {
    // ...
    (void)ap_request_instance(&zrequest, AP_G(base_uri));
```

```
ap_request_t *ap_request_instance(ap_request_t *this_ptr, zend_string *request_uri) /* {{{ */ {
    return ap_request_http_instance(this_ptr, NULL, request_uri);
}
```

```
#0  ap_request_http_instance (this_ptr=0x7fffffffadb0, request_uri=0x0, base_uri=0x0) at /home/work/src/php7-extensions/ap/requests/ap_request_http.c:83
#1  ap_request_instance (this_ptr=0x7fffffffadb0, request_uri=0x0) at /home/work/src/php7-extensions/ap/ap_request.c:86
#2  zim_ap_application___construct (execute_data=0x7ffff58141a0, return_value=0x7ffff5814150)

ap_request_t *ap_request_http_instance(ap_request_t *this_ptr, zend_string *request_uri, zend_string *base_uri)
{
    zend_string *settled_uri = NULL;
    
    // ...
    zval *uri;
    do {
        // ...
        // 用$_SERVER['PATH_INFO']填充settled_uri
        uri = ap_request_query_str(AP_GLOBAL_VARS_SERVER, "PATH_INFO", sizeof("PATH_INFO") - 1);
        if (uri) {
            if (EXPECTED(Z_TYPE_P(uri) == IS_STRING)) {
                settled_uri = zend_string_copy(Z_STR_P(uri));
                break;
            }
    } while (0);
    
    if (settled_uri) {
        // ...
        zend_update_property_str(ap_request_http_ce, this_ptr, ZEND_STRL(AP_REQUEST_PROPERTY_NAME_URI), settled_uri);
        ap_request_set_base_uri(this_ptr, base_uri, settled_uri);
        zend_string_release(settled_uri);
    }
    
```

```
#define AP_REQUEST_PROPERTY_NAME_BASE       "_base_uri"

// SCRIPT_NAME > PHP_SELF > ORIG_SCRIPT_NAME
// base_uri --> App(Module) name
// uri      --> Controller/Action

int ap_request_set_base_uri(ap_request_t *request, zend_string *base_uri, zend_string *request_uri) {
    // ...
    zval *script_filename = ap_request_query_str(AP_GLOBAL_VARS_SERVER, "SCRIPT_FILENAME", sizeof("SCRIPT_FILENAME") - 1);
    
    script_name = ap_request_query_str(AP_GLOBAL_VARS_SERVER, "SCRIPT_NAME", sizeof("SCRIPT_NAME") - 1);
    
     if (ZSTR_LEN(dir)) {
         if (strncmp(ZSTR_VAL(request_uri), ZSTR_VAL(dir), ZSTR_LEN(dir)) == 0) {
                 zend_update_property_str(ap_request_ce, request, ZEND_STRL(AP_REQUEST_PROPERTY_NAME_BASE), dir);
                 zend_string_release(dir);
                 zend_string_release(basename);
                 return 1;
         }
 }
    zend_update_property_string(ap_request_ce, request, ZEND_STRL(AP_REQUEST_PROPERTY_NAME_BASE), "");

```

```
#0  ap_dispatcher_instance (this_ptr=0x7fffffffada0) at /home/work/src/php7-extensions/ap/ap_dispatcher.c:110
#1  zim_ap_application___construct (execute_data=0x7ffff58141a0, return_value=0x7ffff5814150)
    at /home/work/src/php7-extensions/ap/ap_application.c:346
    
#define ap_request_t		zval

ap_dispatcher_t *ap_dispatcher_instance(ap_dispatcher_t *this_ptr)
{
```

```
PHP_METHOD(ap_application, run) {
```

```
#define AP_ROUTER_PROPERTY_NAME_ROUTES 		"_routes"
#define AP_ROUTER_PROPERTY_NAME_CURRENT_ROUTE	"_current"

routers = zend_read_property(ap_router_ce, router, ZEND_STRL(AP_ROUTER_PROPERTY_NAME_ROUTES), 1, NULL);

static inline void ap_dispatcher_fix_default(ap_dispatcher_t *dispatcher, ap_request_t *request) {

```