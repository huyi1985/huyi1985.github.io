```c
#include "ext/standard/base64.h"
```

```c

static EVP_PKEY * php_openssl_evp_from_zval(zval * val, int public_key, char * passphrase, int makeresource, zend_resource **resourceval);

/* {{{ proto int openssl_pkey_get_private(string key [, string passphrase])
   Gets private keys */
PHP_FUNCTION(openssl_pkey_get_private)
{
    zval *cert;
    EVP_PKEY *pkey;
    char * passphrase = "";
    size_t passphrase_len = sizeof("")-1;
    zend_resource *res;

    if (zend_parse_parameters(ZEND_NUM_ARGS(), "z|s", &cert, &passphrase, &passphrase_len) == FAILURE) {
        return;
    }
    pkey = php_openssl_evp_from_zval(cert, 0, passphrase, 1, &res);

    if (pkey == NULL) {
        RETURN_FALSE;
    }
    ZVAL_RES(return_value, res);
    Z_ADDREF_P(return_value);
}
```

```php
<?php
$privateKey =
'-----BEGIN PRIVATE KEY-----
MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAKzcQZsMsF01wiAU
43F0jo6wCTpQyU74N9EpLfGvY/fvEtuhcjJzfC1uRYiaxpRAeyo24qRBtAIIYj7v
ftD8rRVTwDltAIBJ0PrWWOIohiBGHb4NLkmR7eAa/wQl5W/IM6UWemlg+Iv+fmVX
cR2+1WfBNibc5UKhL1+RmB+ORv33AgMBAAECgYA26CuKpYgrw1SrPhdUxXI2zqHP
vTOEewG31X27hDub2HvD+c89SUOLZrh9gLRNCQJWUWLCTABymNkkJozAs1ICq4LC
Q+/JuXKQkhCFBBrGBVP9l+YPuy+rTSrJPV6SUa9jfB7j5iw0E1fQLW1EaK6Cw+Xs
ecpaF1FJqUDH1Q8x8QJBANoPQbO2nyllwNMzfoME7UHyfMLFPhM49vpu87xtbT6h
wvWycWBChWfyWS7J0lhxz/YeC/HIlAVJbKvq8yaUVokCQQDK77/4U11z8N1nP2wf
y4ZRuuR4LJHU0nfbCwkXzW7jhLXf98tGhgM/qmREuTn8tD9nuILP+SfX21xeDXmp
K5B/AkEAnUUxqs8E3hOgTfMuxIoyIEUmzEb77VtBbf/F1NnLV8fNV+1aLgXsN7sn
rUIsblOvnJ+xF7IFaAa71QaAVgvYmQJBAMELC6wncTCHIbXDiRE9w8ofZJJEo3y1
sTn253FzBFb9uR0SVJYDiTeY2MTfBiAzPlVmGVnJA3O8wcLeQqsAO/UCQC9Ir0y1
bK2tpewYjtpywlP3EZ2RL89StIfipidX0GCDZID1BEieXP+HzDPdv/ung+A+MvHo
9YEAD/lNdCML/XQ=
-----END PRIVATE KEY-----';

$algo = OPENSSL_ALGO_SHA1;
$content = 'hello';

$pKey = openssl_pkey_get_private($privateKey);
openssl_sign($content, $sign, $pKey, $algo);
echo base64_encode($sign), PHP_EOL;
```

http://www.phpinternalsbook.com/php7/internal_types/strings/zend_strings.html