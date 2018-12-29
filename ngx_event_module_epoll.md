# epoll

## ngx\_epoll\_init
```
#0  ngx_epoll_init (cycle=0x6facf0, timer=0) at src/event/modules/ngx_epoll_module.c:319
#1  ngx_event_process_init (cycle=0x6facf0) at src/event/ngx_event.c:626
#2  ngx_single_process_cycle (cycle=0x6facf0) at src/os/unix/ngx_process_cycle.c:298
#3  main (argc=1, argv=0x7fffffffe938) at src/core/nginx.c:416
```

## ngx\_epoll\_process\_events
`epoll_wait` here!

```
#0  ngx_epoll_process_events (cycle=0x6facf0, timer=18446744073709551615, flags=1) at src/event/modules/ngx_epoll_module.c:714
#1 ngx_process_events_and_timers (cycle=0x6facf0) at src/event/ngx_event.c:248
#2 ngx_single_process_cycle (cycle=0x6facf0) at src/os/unix/ngx_process_cycle.c:308
#3 main (argc=1, argv=0x7fffffffe938) at src/core/nginx.c:416
```


## 处理新连接
```
static ngx_int_t
ngx_epoll_process_events(ngx_cycle_t *cycle, ngx_msec_t timer, ngx_uint_t flags)
{
    // ...
    events = epoll_wait(ep, event_list, (int) nevents, timer);

    // check errors ...
    
    for (i = 0; i < events; i++) {
        c = event_list[i].data.ptr;

        instance = (uintptr_t) c & 1;
        c = (ngx_connection_t *) ((uintptr_t) c & (uintptr_t) ~1);

        rev = c->read;	// read event 'struct ngx_event_t'

        revents = event_list[i].events;

        if ((revents & EPOLLIN) && rev->active) {

            rev->ready = 1;

            if (flags & NGX_POST_EVENTS) {
                // ...
            } else {
                rev->handler(rev);	// (ngx_event_handler_pt) 0x42ce3a <ngx_event_accept>
            }
        }
        
        // ...

```

```
#0  ngx_event_accept (ev=0x7218c0) at src/event/ngx_event_accept.c:35
#1  ngx_epoll_process_events (cycle=0x6facf0, timer=18446744073709551615, flags=1) at src/event/modules/ngx_epoll_module.c:822
#2  ngx_process_events_and_timers (cycle=0x6facf0) at src/event/ngx_event.c:248
#3  ngx_single_process_cycle (cycle=0x6facf0) at src/os/unix/ngx_process_cycle.c:308
#4  main (argc=1, argv=0x7fffffffe938) at src/core/nginx.c:416
```

## 处理accept返回的fd

### 1. 调用accept(2)
```
void
ngx_event_accept(ngx_event_t *ev)
{
    do {
        s = accept4(lc->fd, (struct sockaddr *) sa, &socklen, SOCK_NONBLOCK);
    } while (ev->available);
```

### 2. 注册accept返回的fd
```
void
ngx_event_accept(ngx_event_t *ev)
{
    do {
        // use accept4
        c = ngx_get_connection(s, ev->log);
        
        // ...
        ls->handler(c);    // ngx_listening_t * ls 
                           // ls->handler ngx_connection_handler_pt --> 'ngx_http_init_connection()'
    } while(...)
```

```
void
ngx_http_init_connection(ngx_connection_t *c)
{
    rev->handler = ngx_http_wait_request_handler;
    c->write->handler = ngx_http_empty_handler;
    
    // ...
    if (ngx_handle_read_event(rev, 0) != NGX_OK) {
        ngx_http_close_connection(c);
        return;
    }
}
```

```
// src/event/ngx_event.c
ngx_ini_t
ngx_handle_read_event(ngx_event_t *rev, ngx_uint_t flags)
{
    if ( // ... {
        if (!rev->active && !rev->ready) {
            if (ngx_add_event(rev, NGX_READ_EVENT, NGX_CLEAR_EVENT) ...
```

ngx\_add\_event --> ngx\_epoll\_add\_event ??

```
static ngx_int_t
ngx_epoll_add_event(ngx_event_t *ev, ngx_int_t event, ngx_uint_t flags)
{

```

## 1次请求-响应，epoll_wait的3次返回

```
rev->handler(rev)

1. ngx_event_accept
	|- ngx_http_init_connection
		|- ngx_handle_read_event
			|- ngx_epoll_add_event
2. ngx_http_wait_request_handler
	|- ngx_http_process_request_line
		|- ngx_http_read_request_header
		|- ngx_http_parse_request_line
		|- ngx_http_process_request_uri
		|- ngx_http_process_request_headers
			|- ngx_http_read_request_header
			|- ngx_http_parse_header_line
			|- [rc == NGX_OK]hh->handler(r, h, hh->offset) (handler --> ngx_http_process_host, ngx_http_process_user_agent ...)
			
			|- [rc == NGX_HTTP_PARSE_HEADER_DONE] ngx_http_process_request_header
			|- [rc == NGX_HTTP_PARSE_HEADER_DONE] ngx_http_process_request_headers
				|- ngx_http_process_request
					|- ngx_http_handler (r->phase_handler = 0;)
						|- ngx_http_core_run_phases
```


### 1. 连接已建立
```
ngx_epoll_process_events(ngx_cycle_t *cycle, ngx_msec_t timer, ngx_uint_t flags)
{
    ...
    for (i = 0; i < events; i++) {
        ...
        if ((revents & EPOLLIN) && rev->active) {
            rev->handler(rev); // ngx_event_t * rev
                               // rev->handler --> ngx_http_keepalive_handler    
```

```
ngx_epoll_process_events(ngx_cycle_t *cycle, ngx_msec_t timer, ngx_uint_t flags)
{
    ...
    for (i = 0; i < events; i++) {
        ...
        if ((revents & EPOLLIN) && rev->active) {
            rev->handler(rev); // ngx_event_t * rev
                               // rev->handler --> ngx_event_accept    
```

### 2. 读请求
```
ngx_epoll_process_events(ngx_cycle_t *cycle, ngx_msec_t timer, ngx_uint_t flags)
{
    ...
    for (i = 0; i < events; i++) {
        ...
        if ((revents & EPOLLIN) && rev->active) {
            rev->handler(rev); // ngx_event_t * rev
                               // rev->handler --> ngx_http_wait_request_handler    
``` 

```
ngx_http_wait_request_handler(ngx_event_t *rev)
{
    // ...
    n = c->recv(c, b->last, size);
    
    // ...
    rev->handler = ngx_http_process_request_line;
    ngx_http_process_request_line(rev);

}
```

### 3. 写响应
```
```

## 大循环
```
// src/os/unix/ngx_process_cycle.c

ngx_single_process_cycle(ngx_cycle_t *cycle)
{
    for ( ;; ) {
        ngx_process_events_and_timers(cycle);
```

```
// src/event/ngx_event.c
void
ngx_process_events_and_timers(ngx_cycle_t *cycle)
{
    (void) ngx_process_events(cycle, timer, flags);
    
    // ...
```