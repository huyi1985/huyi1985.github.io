---
title: Python明明执行了print，为什么屏幕上空空如也
date: '2026-01-23'
---

# Python明明执行了print，为什么屏幕上空空如也

先来看这样一段 Python 代码，猜猜运行结果

```python
# python3 hello.py
import time

print("Hello World")
time.sleep(10)
```

这段“简单到爆”的代码，大家一定都能猜到结果。但要是这样执行呢？

```bash
$ python3 hello.py | tee
```

`tee` 命令用于**将前一个命令的输出同时写入文件和标准输出**，方便一边在终端查看一边保存结果。如果 `tee` 不带文件名参数，就会把输入原封不动地输出，相当于一个“透明管道”。

执行结果是什么呢？来个投票吧。

> 【投票】
> 这条命令的结果是？
> 屏幕上根本看不到"Hello World"
> 屏幕上立刻出现"Hello World"
> 等了 10 秒钟，才在屏幕上看到"Hello World"

如果我在 `print("Hello World")` 中加个 `end=""` 参数，即 `print("Hello World", end="")`，结果又是什么呢？

这背后，其实是**输出缓冲机制**在作怪。

简单来说，**标准输出（stdout）有两种缓冲模式**：

- **行缓冲（line-buffered）**：只有当输出里出现换行符 `\n`，或者缓冲区满了，内容才会真正“刷”到终端。终端通常默认是行缓冲，所以在屏幕上能立即看到 `"Hello World\n"`；而要等 10 秒后才能看到带 `end=""` 的 `print()` 输出。
- **块缓冲（full-buffered）**：输出会先积累在缓冲区里，等缓冲区满了或者程序结束时才一次性写出。如果 `stdout` 被管道或文件重定向了（比如 `| tee`、`| grep`），Python 就会**自动切换到块缓冲模式**。所以即使 `print("Hello World")` 确实执行完了，也要等缓冲区满（或者 手动 `flush()`）才能看到输出。

可以通过如下代码查看缓冲模式：

![](/assets/neh8n0.png)

```python
import sys
import time

print("Hello World")
time.sleep(10)

# 是否是终端
print("isatty:", sys.stdout.isatty())
# 是否行缓冲模式？
print("line_buffering:", getattr(sys.stdout, 'line_buffering', None))

╔════════════════════════╦════════════════════════════╗
║ # 单独执行              ║ # 使用管道执行               ║
║ # $ python3 hello.py   ║ # $ python3 hello.py | tee ║
║ # Hello World          ║ # (...⏰ 10秒后)            ║
║ # (...⏰ 10秒后)        ║ # Hello World              ║
║ # isatty: True         ║ # isatty: False            ║
║ # line_buffering: True ║ # line_buffering: False    ║
╚════════════════════════╩════════════════════════════╝
```

块缓冲机制的存在本是为了提高效率，但有时候真心让人抓狂。单独执行 `python xxx.py` 能看到预期的内容，但一旦想用 `grep` 过滤输出；或者用 `| tee result.log`，既要实时看到处理结果，又想把结果保存到 `result.log`，就会遇到块缓冲的问题，输出可能迟迟不会刷到屏幕上。这时第一反应往往是脚本出 bug 了吧？！于是开始检查代码，在错误的道路上越走越远。

解决办法倒是很简单：可以在 `print()` 里加上参数 `flush=True`；或者在运行 Python 时加 `-u` 参数，进入`unbuffered` 模式：

```bash
$ python3 -u xxx.py | tee result.log
```

----

突然发现，PHP 程序员好像不用担心“块缓冲模式”这个问题，`echo` 能立刻输出。

用你熟悉的语言写“Hello World”程序，把输出用管道接上 `tee`，屏幕上会不会也迟迟看不到内容呢？

----

```
fileno(0x7fee31adb780)                                                                                             = 1
fileno(0x562873c194e0)                                                                                             = 3

write(1, "Hello World", 11Hello World)                                                                                        = 11
fflush(0x7fee31adb780)                                                                                             = 0
write(1, "\n", 1
)                                                                                                  = 1
fflush(0x7fee31adb780)                                                                                             = 0
sleep(10)                                                                                                          = 0
fclose(0x562873c194e0)
```