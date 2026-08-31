---
title: PHP 8.2 的新功能——用 SensitiveParameter 避免密码暴露在函数调用栈信息中
date: '2024-09-04'
---

我们知道，若 PHP 的程序异常退出，就会输出函数调用栈信息（stack trace）。信息中列出了每一次函数调用，从产生异常的最内层函数开始，到调用这个函数的函数，再到更外层的函数，逐级向外，一直到虚拟的 `main()` 函数为止。其间每一个函数的名字和参数都会被打印出来，以便于调试和排查问题。

![](img1.png)

但你有没有想到这套机制带来的安全隐患？

例如，到了 PHP 8.0 以后，若向 `password_hash()` 函数传递尚未支持的哈希算法名称（如这里的`'MurmurHash'`），该函数就会抛出异常，导致本该保密的密码直接暴露在函数调用栈信息中：

```php
<?php
function loginAction($username, $password) {
    $hash = password_hash($password, 'MurmurHash');
}

loginAction('foobar', '$3cr3t');
```

```
Fatal error: Uncaught ValueError: password_hash(): ↵
  Argument #2 ($algo) must be a valid password hashing algorithm in ...
Stack trace:
#0 /home/user/scripts/code.php(3): password_hash('$3cr3t', 'MurmurHash')
#1 /home/user/scripts/code.php(6): loginAction('foobar', '$3cr3t')
#2 {main}
  thrown in /home/user/scripts/code.php on line 3
```

> 在 PHP 8.0+ 中，是否在函数调用栈中显示参数的信息，其实还受 `zend.exception_ignore_args` 和 `zend.exception_string_param_max_len` 这两个配置项的控制。将前者设置为 `On`，或者后者设置为 `0`，也可以以牺牲便捷为代价，在一定程度上保护敏感数据。

MySQL 等数据库的密码也面临同样的风险：

```php
<?php
$pdo = new PDO("mysql:host=localhost;dbname=world", 'my_user', 'my_password');
$result = $pdo->query("SELECT Name FROM City");
```

```
Fatal error: Uncaught PDOException: SQLSTATE[HY000] [2002]  ↵
  No such file or directory in ...
Stack trace:
#0 /home/user/scripts/code.php(2): PDO->__construct('mysql:host=loca...', 'my_user', 'my_password')
#1 {main}
  thrown in /home/user/scripts/code.php on line 2
```

为了解决这类安全问题，PHP 8.2+ 引入了名为 `SensitiveParameter` 的属性（attribute）来标记此类敏感参数，避免它们直接暴露在函数调用栈信息中。

![](img2.png)

经过这个属性的标记，在函数调用栈信息中就再也看不到密码之类的信息了：

```
Stack trace:
#0 /home/user/scripts/code.php(3): password_hash(Object(SensitiveParameterValue), 'MurmurHash')
#1 /home/user/scripts/code.php(6): loginAction('foobar', '$3cr3t')
#2 {main}
  thrown in /home/user/scripts/code.php on line 3
```

```
Stack trace:
#0 /home/user/scripts/code.php(2): PDO->__construct('mysql:host=loca...', 'my_user', Object(SensitiveParameterValue))
#1 {main}
  thrown in /home/user/scripts/code.php on line 2
```

敏感信息全部被替换成了 `Object(SensitiveParameterValue)`。

这是怎么实现的呢？

原来，在 PHP 8.2+ 中，只要参数被归类为敏感参数，即附带了 `SensitiveParameter` 属性时，`var_dump()`/`logging()` 函数中可用的参数的实际值将被替换为 PHP 8.2 中新添加的 `SensitiveParameterValue` 类的对象。

该类具有诸多限制，如将数据存放在私有属性中，以防止从外部访问；不允许序列化；不输出任何调试信息等。