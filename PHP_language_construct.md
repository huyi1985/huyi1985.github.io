PHP Language Construct

## PHP 5.4
```
"./zend_language_parser.y" 1247L

internal_functions_in_yacc:
                T_ISSET '(' isset_variables ')' { $$ = $3; }
        |       T_EMPTY '(' variable ')'        { zend_do_isset_or_isempty(ZEND_ISEMPTY, &$$, &$3 TSRMLS_CC); }
        |       T_INCLUDE expr                  { zend_do_include_or_eval(ZEND_INCLUDE, &$$, &$2 TSRMLS_CC); }
        |       T_INCLUDE_ONCE expr     { zend_do_include_or_eval(ZEND_INCLUDE_ONCE, &$$, &$2 TSRMLS_CC); }
        |       T_EVAL '(' expr ')'     { zend_do_include_or_eval(ZEND_EVAL, &$$, &$3 TSRMLS_CC); }
        |       T_REQUIRE expr                  { zend_do_include_or_eval(ZEND_REQUIRE, &$$, &$2 TSRMLS_CC); }
        |       T_REQUIRE_ONCE expr             { zend_do_include_or_eval(ZEND_REQUIRE_ONCE, &$$, &$2 TSRMLS_CC); }
;
```

## PHP7
```
internal_functions_in_yacc:
		T_ISSET '(' isset_variables possible_comma ')' { $$ = $3; }
	|	T_EMPTY '(' expr ')' { $$ = zend_ast_create(ZEND_AST_EMPTY, $3); }
	|	T_INCLUDE expr
			{ $$ = zend_ast_create_ex(ZEND_AST_INCLUDE_OR_EVAL, ZEND_INCLUDE, $2); }
	|	T_INCLUDE_ONCE expr
			{ $$ = zend_ast_create_ex(ZEND_AST_INCLUDE_OR_EVAL, ZEND_INCLUDE_ONCE, $2); }
	|	T_EVAL '(' expr ')'
			{ $$ = zend_ast_create_ex(ZEND_AST_INCLUDE_OR_EVAL, ZEND_EVAL, $3); }
	|	T_REQUIRE expr
			{ $$ = zend_ast_create_ex(ZEND_AST_INCLUDE_OR_EVAL, ZEND_REQUIRE, $2); }
	|	T_REQUIRE_ONCE expr
			{ $$ = zend_ast_create_ex(ZEND_AST_INCLUDE_OR_EVAL, ZEND_REQUIRE_ONCE, $2); }
;
```