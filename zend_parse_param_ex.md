# ZEND_PARSE_PARAM

```
#define ZEND_PARSE_PARAMETERS_START_EX(flags, min_num_args, max_num_args) do { \
    const int _flags = (flags); \
    int _min_num_args = (min_num_args); \
    int _max_num_args = (max_num_args); \
    int _num_args = EX_NUM_ARGS(); \
    int _i; \
    zval *_real_arg, *_arg = NULL; \
    zend_expected_type _expected_type = Z_EXPECTED_LONG; \
    char *_error = NULL; \
    zend_bool _dummy; \
    zend_bool _optional = 0; \
    int error_code = ZPP_ERROR_OK; \
    ((void)_i); \
    ((void)_real_arg); \
    ((void)_arg); \
    ((void)_expected_type); \
    ((void)_error); \
    ((void)_dummy); \
    ((void)_optional); \
    \
    do { \
        if (UNEXPECTED(_num_args < _min_num_args) || \
        (UNEXPECTED(_num_args > _max_num_args) && \
         EXPECTED(_max_num_args >= 0))) { \
        if (!(_flags & ZEND_PARSE_PARAMS_QUIET)) { \
            zend_wrong_paramers_count_error(_num_args, _min_num_args, _max_num_args); \
        } \
        error_code = ZPP_ERROR_FAILURE; \
        break; \
        } \
        _i = 0; \
        _real_arg = ZEND_CALL_ARG(execute_data, 0);


#define ZEND_PARSE_PARAMETERS_END_EX(failure) \
    } while (0); \
    if (UNEXPECTED(error_code != ZPP_ERROR_OK)) { \
        if (!(_flags & ZEND_PARSE_PARAMS_QUIET)) { \
        if (error_code == ZPP_ERROR_WRONG_CALLBACK) { \
            zend_wrong_callback_error(E_WARNING, _i, _error); \
        } else if (error_code == ZPP_ERROR_WRONG_CLASS) { \
            zend_wrong_paramer_class_error(_i, _error, _arg); \
        } else if (error_code == ZPP_ERROR_WRONG_ARG) { \
            zend_wrong_paramer_type_error(_i, _expected_type, _arg); \
        } \
        } \
        failure; \
    } \
    } while (0)
```
