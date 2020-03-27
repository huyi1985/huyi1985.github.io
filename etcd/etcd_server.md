# etcd_server

```go
type EtcdServer struct {
	cfg *ServerConfig

	r raftNode

	w          wait.Wait
	stop       chan struct{}
	done       chan struct{}
	errorc     chan error
	id         types.ID
	attributes Attributes

	Cluster *Cluster

	store store.Store

	stats  *stats.ServerStats
	lstats *stats.LeaderStats

	SyncTicker <-chan time.Time

	reqIDGen *idutil.Generator
}
```

## request id gen



```bash
curl -L http://127.0.0.1:4001/v2/keys/mykey
{"action":"get","node":{"key":"/mykey","value":"this is awesome","modifiedIndex":3,"createdIndex":3}}
```



client/keys.go

```go
func (k *httpKeysAPI) Get(ctx context.Context, key string) (*Response, error) {
```

