# Nginx Command ngx\_http\_realip

```
ngx_http_core_run_phases()
rc = ph[r->phase_handler].checker(r, &ph[r->phase_handler]);
1. r->phase_handler == 0
2. r->phase_handler == 5

ph[r->phase_handler].checker

    /*
     * generic phase checker,
     * used by the post read and pre-access phases
     */
     
0. <ngx_event_timer_sentinel>     
1. <ngx_http_core_generic_phase>
2. <ngx_http_core_rewrite_phase>
3. <ngx_http_core_find_config_phase>
4. <ngx_http_core_rewrite_phase>
5. <ngx_http_core_post_rewrite_phase>
6. <ngx_http_core_generic_phase>
7. <ngx_http_core_access_phase>
8. <ngx_http_core_post_access_phase>
9. <ngx_http_core_content_phase>

curl http://<host>/ 引起
index_handle发起internal_redirect

void ngx_http_handler(ngx_http_request_t *r)
{
	if (!r->internal) {
		// ...
	} else {
	    cmcf = ngx_http_get_module_main_conf(r, ngx_http_core_module);
	    r->phase_handler = cmcf->phase_engine.server_rewrite_index;
	}
	
	// ...

10. <ngx_http_core_rewrite_phase> **
11. <ngx_http_core_find_config_phase>
12. <ngx_http_core_rewrite_phase>
13. <ngx_http_core_post_rewrite_phase>
14. <ngx_http_core_generic_phase>
15. <ngx_http_core_access_phase>
16. <ngx_http_core_post_access_phase>
17. <ngx_http_core_content_phase>

// http_core_run_phase recursively called
#0  ngx_http_core_run_phases (r=0xe24fe0) at src/http/ngx_http_core_module.c:867
#1  0x000000000043ecd9 in ngx_http_handler (r=0xe24fe0) at src/http/ngx_http_core_module.c:856
#2  0x0000000000442bae in ngx_http_internal_redirect (r=0xe24fe0, uri=0x7ffffe6d7610, args=0xe25338) at src/http/ngx_http_core_module.c:2635
#3  0x00000000004748de in ngx_http_index_handler (r=0xe24fe0) at src/http/modules/ngx_http_index_module.c:277
#4  0x00000000004402a7 in ngx_http_core_content_phase (r=0xe24fe0, ph=0xe38cb0) at src/http/ngx_http_core_module.c:1403
#5  0x000000000043ed6b in ngx_http_core_run_phases (r=0xe24fe0) at src/http/ngx_http_core_module.c:873

```

### 注册module
```
// ./auto/sources
HTTP_REALIP_MODULE=ngx_http_realip_module
HTTP_REALIP_SRCS=src/http/modules/ngx_http_realip_module.c

// https://github.com/nginx/nginx/blob/4bf4650f2f10f7bbacfe7a33da744f18951d416d/src/http/modules/ngx_http_realip_module.c#L101
ngx_module_t  ngx_http_realip_module = {
    NGX_MODULE_V1,
    &ngx_http_realip_module_ctx,           /* module context */
...
    
static ngx_http_module_t  ngx_http_realip_module_ctx = {
    ngx_http_realip_add_variables,         /* preconfiguration */
    ngx_http_realip_init,                  /* postconfiguration */
...
    
```

### init module
Phases:

- NGX\_HTTP\_POST\_READ\_PHASE
- NGX\_HTTP\_PREACCESS\_PHASE

```
static ngx_int_t
ngx_http_realip_init(ngx_conf_t *cf)
{
    h = ngx_array_push(&cmcf->phases[NGX_HTTP_POST_READ_PHASE].handlers);
    *h = ngx_http_realip_handler;
    
    h = ngx_array_push(&cmcf->phases[NGX_HTTP_PREACCESS_PHASE].handlers);
    *h = ngx_http_realip_handler;


// https://github.com/nginx/nginx/blob/4bf4650f2f10f7bbacfe7a33da744f18951d416d/src/http/modules/ngx_http_realip_module.c#L130

ngx_http_realip_handler(ngx_http_request_t *r)
{
```

### 在哪里修改的r->connection中的地址
```
static ngx_int_t
ngx_http_realip_set_addr(ngx_http_request_t *r, ngx_addr_t *addr)
{
    u_char                  text[NGX_SOCKADDR_STRLEN];
    
    len = ngx_sock_ntop(addr->sockaddr, addr->socklen, text,
                        NGX_SOCKADDR_STRLEN, 0);
                        
    ngx_memcpy(p, text, len);
    
    c->sockaddr = addr->sockaddr;
    c->socklen = addr->socklen;
    c->addr_text.len = len;
    c->addr_text.data = p;
                 
```

### 如果没配置'set\_real\_ip\_from'
```
ngx_http_realip_handler(ngx_http_request_t *r)
{
    rlcf = ngx_http_get_module_loc_conf(r, ngx_http_realip_module);

    if (rlcf->from == NULL) {
        return NGX_DECLINED;
    }
```

### 如果配置了‘real\_ip\_header X-Real-IP;’但没有设置对应的头
```
ngx_http_realip_handler(ngx_http_request_t *r)
{
    rlcf = ngx_http_get_module_loc_conf(r, ngx_http_realip_module);

switch (rlcf->type) {

    case NGX_HTTP_REALIP_XREALIP:

        if (r->headers_in.x_real_ip == NULL) {
            return NGX_DECLINED;
        }
```

### r->headers\_in.x\_real\_ip
```
r->headers_in.x_real_ip
type = struct {
    ngx_uint_t hash;
    ngx_str_t key;
    ngx_str_t value;
    u_char *lowcase_key;
} *
```
