# Nginx $remote_addr

```
static ngx_int_t
ngx_http_variable_remote_addr(ngx_http_request_t *r,
    ngx_http_variable_value_t *v, uintptr_t data)
{
    v->len = r->connection->addr_text.len;
    v->valid = 1;
    v->no_cacheable = 0;
    v->not_found = 0;
    v->data = r->connection->addr_text.data;

    return NGX_OK;
}
```

```
#0  ngx_http_variable_remote_addr (r=0x14b5fe0, v=0x14b6a38, data=0) at src/http/ngx_http_variables.c:1177
#1  0x000000000043dea1 in ngx_http_get_indexed_variable (r=0x14b5fe0, index=<optimized out>) at src/http/ngx_http_variables.c:509
#2  0x000000000043a75e in ngx_http_log_variable_getlen (r=<optimized out>, data=<optimized out>) at src/http/modules/ngx_http_log_module.c:936
#3  0x000000000043a35d in ngx_http_log_handler (r=0x14b5fe0) at src/http/modules/ngx_http_log_module.c:292
#4  0x000000000042fb00 in ngx_http_log_request (r=r@entry=0x14b5fe0) at src/http/ngx_http_request.c:3524
#5  0x0000000000430c84 in ngx_http_free_request (r=r@entry=0x14b5fe0, rc=rc@entry=0) at src/http/ngx_http_request.c:3471
#6  0x0000000000431e19 in ngx_http_set_keepalive (r=0x14b5fe0) at src/http/ngx_http_request.c:2909
#7  ngx_http_finalize_connection (r=r@entry=0x14b5fe0) at src/http/ngx_http_request.c:2546
#8  0x0000000000432b8d in ngx_http_finalize_request (r=r@entry=0x14b5fe0, rc=<optimized out>) at src/http/ngx_http_request.c:2442
#9  0x00000000004328c8 in ngx_http_finalize_request (r=r@entry=0x14b5fe0, rc=404) at src/http/ngx_http_request.c:2329
#10 0x000000000042d80e in ngx_http_core_content_phase (r=0x14b5fe0, ph=0x14a7bc0) at src/http/ngx_http_core_module.c:1406
#11 0x0000000000428683 in ngx_http_core_run_phases (r=r@entry=0x14b5fe0) at src/http/ngx_http_core_module.c:873
#12 0x000000000042879c in ngx_http_handler (r=r@entry=0x14b5fe0) at src/http/ngx_http_core_module.c:856
#13 0x0000000000430a52 in ngx_http_process_request (r=r@entry=0x14b5fe0) at src/http/ngx_http_request.c:1910
#14 0x0000000000433683 in ngx_http_process_request_headers (rev=rev@entry=0x14e99f0) at src/http/ngx_http_request.c:1341
#15 0x00000000004339ac in ngx_http_process_request_line (rev=rev@entry=0x14e99f0) at src/http/ngx_http_request.c:1021
```