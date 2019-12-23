## 502

1. upstream connection timeout (ip:port不存在、没启动php-fpm)

2. PHPFPM request_terminate_timeout 超时，worker进程被KILL

   （ -> Broken pipe ）  https://www.cnblogs.com/metoy/p/6565486.html  

3. 从connect PHP-FPM到发送Fastcgi Request超过5s

```
// PHP FPM strace log
accept(0, {sa_family=AF_INET, sin_port=htons(57960), sin_addr=inet_addr("127.0.0.1")}, [16]) = 3
times({tms_utime=1, tms_stime=1, tms_cutime=0, tms_cstime=0}) = 1721486416
poll([{fd=3, events=POLLIN}], 1, 5000)  = 0 (Timeout)
close(3)                                = 0
accept(0, 
```

Nginx worker_process_cycle

```
ngx_worker_process_cycle
    `- ngx_epoll_process_events
    
1. read event ready  -> ngx_event_accept()
2. read event ready  -> ngx_http_wait_request_handler()
                              `-- // connect PHP FPM
3. write event ready -> ngx_http_request_handler()
4. write event ready -> ngx_http_upstream_handler()
                              `-- ngx_http_upstream_send_request()
5. read event ready  -> ngx_http_upstream_handler()

ngx_http_upstream
n = c->recv(c, u->buffer.last, u->buffer.end - u->buffer.last)
```

当从2到4超过5s，`c->recv`就会返回0，导致502

![1573017425545](C:\Users\DYZ\GitHub\huyi1985.github.io\ngx_50x_1573017425545.png)



```c
// ./fpm/fastcgi.c +855 PHP 5.5.9

int fcgi_accept_request(fcgi_request *req)
{
	while (1) {
        // ...
        while (1) {
             fpm_request_reading_headers();

             fds.fd = req->fd;
             fds.events = POLLIN;
             fds.revents = 0;
             do {
                 errno = 0;
                 ret = poll(&fds, 1, 5000);
             } while (ret < 0 && errno == EINTR);
             if (ret > 0 && (fds.revents & POLLIN)) {
                 break;
             }
             fcgi_close(req, 1, 0);
```



## 504

fastcgi_read_timeout

```c
// https://github.com/nginx/nginx/blob/master/src/http/ngx_http_upstream.c#L2284
ngx_http_upstream_process_header(ngx_http_request_t *r, ngx_http_upstream_t *u)
{
    ssize_t            n;
    ngx_int_t          rc;
    ngx_connection_t  *c;

    c = u->peer.connection;

    ngx_log_debug0(NGX_LOG_DEBUG_HTTP, c->log, 0,
                   "http upstream process header");

    c->log->action = "reading response header from upstream";

    if (c->read->timedout) {
        // 读超时会引起504
        ngx_http_upstream_next(r, u, NGX_HTTP_UPSTREAM_FT_TIMEOUT);
        return;
    }
    
// https://github.com/nginx/nginx/blob/master/src/http/ngx_http_upstream.c#L4191
    switch (ft_type) {

    case NGX_HTTP_UPSTREAM_FT_TIMEOUT:
    case NGX_HTTP_UPSTREAM_FT_HTTP_504:
        status = NGX_HTTP_GATEWAY_TIME_OUT;
        break;
```

