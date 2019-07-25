# PHP script execution in background

https://maslosoft.com/kb/how-to-continue-script-execution-in-background-in-php/

```
PHP_FUNCTION(fastcgi_finish_request) /* {{{ */
{
        fcgi_request *request = (fcgi_request*) SG(server_context);

        if (!fcgi_is_closed(request)) {
                php_output_end_all();
                php_header();

                fcgi_end(request);
                fcgi_close(request, 0, 0);
                RETURN_TRUE;
        }

        RETURN_FALSE;

}
```

```
void fcgi_close(fcgi_request *req, int force, int destroy)
{
    if (destroy && req->has_env) {
            fcgi_hash_clean(&req->env);
            req->has_env = 0;
    }

    if ((force || !req->keep) && req->fd >= 0) {

        if (!force) {
                char buf[8];
                
                shutdown(req->fd, 1);
                /* read any remaining data, it may be omitted */
                while (recv(req->fd, buf, sizeof(buf), 0) > 0) {}
        }
        close(req->fd);

#ifdef TCP_NODELAY
        req->nodelay = 0;
#endif
        req->fd = -1;

        req->hook.on_close();
    }
}
```