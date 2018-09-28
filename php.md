
# PHP
## $a;


```c
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
```

./zend_compile.h:718:ZEND_API int lex_scan(zval *zendlval);

```
zend_compile.h:715:extern ZEND_API zend_op_array *(*zend_compile_file)(zend_file_handle *file_handle, int type);
implements:
zend.c:763:			zend_compile_file = dtrace_compile_file;
zend.c:767:			zend_compile_file = compile_file;
```

"(1) token值：词法解析器解析到的token值内容就是token值，这些值统一通过 zval 存储，上面的过程中可以看到调用lex_scan参数是是个zval*，在具体的命中规则总会将解析到的token保存到这个值，从而传递给语法解析器使用，比如PHP中的解析变量的规则：$a;，其词法解析规则为：

<ST_IN_SCRIPTING,ST_DOUBLE_QUOTES,ST_HEREDOC,ST_BACKQUOTE,ST_VAR_OFFSET>"$"{LABEL} {
    //将匹配到的token值保存在zval中
    zend_copy_value(zendlval, (yytext+1), (yyleng-1)); //只保存{LABEL}内容，不包括$，所以是yytext+1
    RETURN_TOKEN(T_VARIABLE);
}

zendlval就是我们传入的zval*，yytext指向命中的token值起始位置，yyleng为token值的长度。"

## Parser

```c
#0  zendparse () at /home/huyi/php-7.2.9/Zend/zend_language_parser.c:4059
#1  0x0000555555b2099b in zend_compile (type=2) at Zend/zend_language_scanner.l:585
#2  0x0000555555b20c0f in compile_file (file_handle=0x7fffffffd200, type=8) at Zend/zend_language_scanner.l:635
#3  0x000055555595bb56 in phar_compile_file (file_handle=0x7fffffffd200, type=8) at /home/huyi/php-7.2.9/ext/phar/phar.c:3320
#4  0x0000555555b81429 in zend_execute_scripts (type=8, retval=0x0, file_count=3) at /home/huyi/php-7.2.9/Zend/zend.c:1490
#5  0x0000555555ae52df in php_execute_script (primary_file=0x7fffffffd200) at /home/huyi/php-7.2.9/main/main.c:2590
#6  0x0000555555c7446e in do_cli (argc=2, argv=0x555556662990) at /home/huyi/php-7.2.9/sapi/cli/php_cli.c:1011
#7  0x0000555555c7562c in main (argc=2, argv=0x555556662990) at /home/huyi/php-7.2.9/sapi/cli/php_cli.c:1404
```

```c
#0  zend_compile_var (result=0x7fffffffa7a0, ast=0x7ffff4085060, type=0) at /home/huyi/php-7.2.9/Zend/zend_compile.c:8323
#1  0x0000555555b6000e in zend_compile_expr (result=0x7fffffffa7a0, ast=0x7ffff4085060) at /home/huyi/php-7.2.9/Zend/zend_compile.c:8217
#2  0x0000555555b5fce0 in zend_compile_stmt (ast=0x7ffff4085060) at /home/huyi/php-7.2.9/Zend/zend_compile.c:8186
#3  0x0000555555b5f8ab in zend_compile_top_stmt (ast=0x7ffff4085060) at /home/huyi/php-7.2.9/Zend/zend_compile.c:8072
#4  0x0000555555b5f88d in zend_compile_top_stmt (ast=0x7ffff4085018) at /home/huyi/php-7.2.9/Zend/zend_compile.c:8067
#5  0x0000555555b20a7e in zend_compile (type=2) at Zend/zend_language_scanner.l:601
#6  0x0000555555b20c0f in compile_file (file_handle=0x7fffffffd200, type=8) at Zend/zend_language_scanner.l:635
#7  0x000055555595bb56 in phar_compile_file (file_handle=0x7fffffffd200, type=8) at /home/huyi/php-7.2.9/ext/phar/phar.c:3320
#8  0x0000555555b81429 in zend_execute_scripts (type=8, retval=0x0, file_count=3) at /home/huyi/php-7.2.9/Zend/zend.c:1490
#9  0x0000555555ae52df in php_execute_script (primary_file=0x7fffffffd200) at /home/huyi/php-7.2.9/main/main.c:2590
#10 0x0000555555c7446e in do_cli (argc=2, argv=0x555556662990) at /home/huyi/php-7.2.9/sapi/cli/php_cli.c:1011
#11 0x0000555555c7562c in main (argc=2, argv=0x555556662990) at /home/huyi/php-7.2.9/sapi/cli/php_cli.c:1404
```

# $a = 42;
```c
(gdb) bt
#0  zend_compile_assign (result=0x7fffffffa7a0, ast=0x7ffff4085088) at /home/huyi/php-7.2.9/Zend/zend_compile.c:2972
#1  0x0000555555b60026 in zend_compile_expr (result=0x7fffffffa7a0, ast=0x7ffff4085088) at /home/huyi/php-7.2.9/Zend/zend_compile.c:8220
#2  0x0000555555b5fce0 in zend_compile_stmt (ast=0x7ffff4085088) at /home/huyi/php-7.2.9/Zend/zend_compile.c:8186
#3  0x0000555555b5f8ab in zend_compile_top_stmt (ast=0x7ffff4085088) at /home/huyi/php-7.2.9/Zend/zend_compile.c:8072
#4  0x0000555555b5f88d in zend_compile_top_stmt (ast=0x7ffff4085018) at /home/huyi/php-7.2.9/Zend/zend_compile.c:8067
#5  0x0000555555b20a7e in zend_compile (type=2) at Zend/zend_language_scanner.l:601
#6  0x0000555555b20c0f in compile_file (file_handle=0x7fffffffd200, type=8) at Zend/zend_language_scanner.l:635
#7  0x000055555595bb56 in phar_compile_file (file_handle=0x7fffffffd200, type=8) at /home/huyi/php-7.2.9/ext/phar/phar.c:3320
#8  0x0000555555b81429 in zend_execute_scripts (type=8, retval=0x0, file_count=3) at /home/huyi/php-7.2.9/Zend/zend.c:1490
#9  0x0000555555ae52df in php_execute_script (primary_file=0x7fffffffd200) at /home/huyi/php-7.2.9/main/main.c:2590
#10 0x0000555555c7446e in do_cli (argc=2, argv=0x555556662990) at /home/huyi/php-7.2.9/sapi/cli/php_cli.c:1011
#11 0x0000555555c7562c in main (argc=2, argv=0x555556662990) at /home/huyi/php-7.2.9/sapi/cli/php_cli.c:1404
```

```c
void zend_compile_expr(znode *result, zend_ast *ast) /* {{{ */
{
        /* CG(zend_lineno) = ast->lineno; */
        CG(zend_lineno) = zend_ast_get_lineno(ast);

        switch (ast->kind) {
                case ZEND_AST_ZVAL:
                        ZVAL_COPY(&result->u.constant, zend_ast_get_zval(ast));
                        result->op_type = IS_CONST;
                        return;
```
