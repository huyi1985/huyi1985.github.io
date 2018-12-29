# Framework

* Set up upstream init function
* Set up peer init function
* Set up peer get/free/tries function

## Flexible Array

```
struct ngx_http_upstream_rr_peers_s {
    ngx_uint_t                   number;
    ngx_uint_t                   total_weight;
    unsigned int single :        1;
    unsigned int weighted :      1;
    ngx_str_t                    *name;
    ngx_http_upstream_rr_peers_t *next;
    ngx_http_upstream_rr_peer_t  peer[1];
}

peers = ngx_pcalloc(cf->pool, sizeof(ngx_http_upstream_rr_peers_t)
                      + sizeof(ngx_http_upstream_rr_peer_t) * (n - 1));
```

```
ptype rrp->peers
type = struct ngx_http_upstream_rr_peers_s {
    ngx_uint_t number;
    ngx_uint_t total_weight;
    unsigned int single : 1;
    unsigned int weighted : 1;
    ngx_str_t *name;
    ngx_http_upstream_rr_peers_t *next;
    ngx_http_upstream_rr_peer_t peer[1];
} *

p rrp->peers->peer
p rrp->peers->peer[1]

```

## get peer function

```
#0  ngx_http_upstream_get_peer (rrp=0x701b58) at src/http/ngx_http_upstream_round_robin.c:490
#1  ngx_http_upstream_get_round_robin_peer (pc=0x701510, data=0x701b58) at src/http/ngx_http_upstream_round_robin.c:422
#2  ngx_event_connect_peer (pc=0x701510) at src/event/ngx_event_connect.c:25
#3  ngx_http_upstream_connect (r=0x700520, u=0x701500) at src/http/ngx_http_upstream.c:1331
#4  ngx_http_upstream_init_request (r=0x700520) at src/http/ngx_http_upstream.c:736
#5  ngx_http_upstream_init (r=0x700520) at src/http/ngx_http_upstream.c:497
```

## Round-Robin core

```
// Round-Robin core
// ngx_http_upstream_rr_peer_data_t *rrp
best = NULL;
total = 0;

for (i = 0; i < rrp->peers->number; i++) {
    peer = &rrp->peers->peer[i];
    
    // ...
    peer->current_weight += peer->effective_weight;
    total += peer->effective_weight;

    ...

    if (best == NULL || peer->current_weight > best->current_weight) {
        best = peer;
}

...
best->current_weight -= total;

return best;
```