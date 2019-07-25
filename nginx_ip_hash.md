# Nginx ip_hash

## 在哪里初始化的ngx_http_request_t *r
```c
void
ngx_event_accept(ngx_event_t *ev)
{
    ...
    ngx_connection_t  *c, *lc;
    
    ...
    lc = ev->data;
    
    ...
    s = accept(lc->fd, &sa.sockaddr, &socklen);  // accept4

    ...
    c->sockaddr = ngx_palloc(c->pool, socklen);
    ngx_memcpy(c->sockaddr, &sa, socklen);

    ...
    if (ls->addr_ntop) {
        c->addr_text.data = ngx_pnalloc(c->pool, ls->addr_text_max_len);
        c->addr_text.len = ngx_sock_ntop(c->sockaddr, c->socklen,
                                         c->addr_text.data,
                                         ls->addr_text_max_len, 0);
    ...
```

```c
ngx_http_request_t *
ngx_http_create_request(ngx_connection_t *c)
{
    ...
    r->connection = c;
    ...
```

## 在哪里初始化的ngx_http_upstream_ip_hash_peer_data_t  *iphp;
```c
static ngx_int_t
ngx_http_upstream_init_ip_hash_peer(ngx_http_request_t *r,
    ngx_http_upstream_srv_conf_t *us)
{
    ...
    ngx_http_upstream_ip_hash_peer_data_t  *iphp;

    iphp = ngx_palloc(r->pool, sizeof(ngx_http_upstream_ip_hash_peer_data_t));
    // {rrp = {peers = 0x0, current = 0, tried = 0x0, data = 0}, hash = 0, addrlen = 0 '\000', addr = 0x0, tries = 0 '\000', get_rr_peer = 0x0}

    // init `rrp` field
    r->upstream->peer.data = &iphp->rrp;
    if (ngx_http_upstream_init_round_robin_peer(r, us) != NGX_OK) {
    ...

    switch (r->connection->sockaddr->sa_family) {
        case AF_INET:
            sin = (struct sockaddr_in *) r->connection->sockaddr;
            iphp->addr = (u_char *) &sin->sin_addr.s_addr;
            iphp->addrlen = 3;  // The first three octets of the client IPv4 address, or the entire IPv6 address, are used as a hashing key.
```

## hard code 素数
```c
ngx_http_upstream_get_ip_hash_peer(ngx_peer_connection_t *pc, void *data)
{
    ngx_http_upstream_ip_hash_peer_data_t  *iphp = data;
    ... 
    hash = iphp->hash; // = 89                                                                                                                                                                 
    ...
    for ( ;; ) {
        // The first three octets of the client IPv4 address, 
	// or the entire IPv6 address, are used as a hashing key.
	for (i = 0; i < (ngx_uint_t) iphp->addrlen; i++) {                                                                                                                             
		hash = (hash * 113 + iphp->addr[i]) % 6271;                                                                                                                                
	}
        ...
```

```
#0  ngx_http_upstream_get_ip_hash_peer (pc=0x1e86910, data=0x1e86f30) at src/http/modules/ngx_http_upstream_ip_hash_module.c:150
#1  0x000000000041d4e8 in ngx_event_connect_peer (pc=pc@entry=0x1e86910) at src/event/ngx_event_connect.c:25
#2  0x0000000000446b17 in ngx_http_upstream_connect (r=r@entry=0x1e1ec70, u=u@entry=0x1e86900) at src/http/ngx_http_upstream.c:1331
#3  0x0000000000447b16 in ngx_http_upstream_init_request (r=r@entry=0x1e1ec70) at src/http/ngx_http_upstream.c:736
#4  0x00000000004482b1 in ngx_http_upstream_init (r=r@entry=0x1e1ec70) at src/http/ngx_http_upstream.c:497
#5  0x000000000043bbb4 in ngx_http_read_client_request_body (r=r@entry=0x1e1ec70, post_handler=0x4481ce <ngx_http_upstream_init>) at src/http/ngx_http_request_body.c:89
```

```
#0  ngx_http_upstream_init_round_robin_peer (r=r@entry=0x1e1ec70, us=us@entry=0x1e16700) at src/http/ngx_http_upstream_round_robin.c:223
#1  0x0000000000472dbc in ngx_http_upstream_init_ip_hash_peer (r=0x1e1ec70, us=0x1e16700) at src/http/modules/ngx_http_upstream_ip_hash_module.c:113
```

```
#0  ngx_http_upstream_init_ip_hash_peer (r=0x1e1ec70, us=0x1e16700) at src/http/modules/ngx_http_upstream_ip_hash_module.c:99
#1  0x0000000000447ac9 in ngx_http_upstream_init_request (r=r@entry=0x1e1ec70) at src/http/ngx_http_upstream.c:722
#2  0x00000000004482b1 in ngx_http_upstream_init (r=r@entry=0x1e1ec70) at src/http/ngx_http_upstream.c:497
#3  0x000000000043bbb4 in ngx_http_read_client_request_body (r=r@entry=0x1e1ec70, post_handler=0x4481ce <ngx_http_upstream_init>) at src/http/ngx_http_request_body.c:89
#4  0x00000000004664ff in ngx_http_proxy_handler (r=0x1e1ec70) at src/http/modules/ngx_http_proxy_module.c:906
#5  0x000000000042d7ae in ngx_http_core_content_phase (r=0x1e1ec70, ph=<optimized out>) at src/http/ngx_http_core_module.c:1396
#6  0x0000000000428683 in ngx_http_core_run_phases (r=r@entry=0x1e1ec70) at src/http/ngx_http_core_module.c:873
#7  0x000000000042879c in ngx_http_handler (r=r@entry=0x1e1ec70) at src/http/ngx_http_core_module.c:856
#8  0x0000000000430a52 in ngx_http_process_request (r=r@entry=0x1e1ec70) at src/http/ngx_http_request.c:1910
#9  0x0000000000433683 in ngx_http_process_request_headers (rev=rev@entry=0x1e52990) at src/http/ngx_http_request.c:1341
#10 0x00000000004339ac in ngx_http_process_request_line (rev=rev@entry=0x1e52990) at src/http/ngx_http_request.c:1021
#11 0x00000000004343e7 in ngx_http_wait_request_handler (rev=0x1e52990) at src/http/ngx_http_request.c:499
#12 0x0000000000425405 in ngx_epoll_process_events (cycle=0x1deda90, timer=<optimized out>, flags=<optimized out>) at src/event/modules/ngx_epoll_module.c:822
```