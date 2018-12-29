# $a;



// Zend/zend_language_scanner.l

<ST_IN_SCRIPTING,ST_DOUBLE_QUOTES,ST_HEREDOC,ST_BACKQUOTE,ST_VAR_OFFSET>"$"{LABEL} {
        zend_copy_value(zendlval, (yytext+1), (yyleng-1));
        RETURN_TOKEN(T_VARIABLE);
}
```

```c
// Zend/zend_language_scanner.l

// TODO: avoid reallocation ???
# define zend_copy_value(zendlval, yytext, yyleng) \
        if (SCNG(output_filter)) { \
                size_t sz = 0; \
                char *s = NULL; \
                SCNG(output_filter)((unsigned char **)&s, &sz, (unsigned char *)yytext, (size_t)yyleng); \
                ZVAL_STRINGL(zendlval, s, sz); \
                efree(s); \
        } else { \
                ZVAL_STRINGL(zendlval, yytext, yyleng); \
        }
