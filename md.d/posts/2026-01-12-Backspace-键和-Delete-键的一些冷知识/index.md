---
title: Backspace 键和 Delete 键的一些冷知识
date: '2026-01-12'
tags:
- Unix
- 终端
- man
- 字符
- ASCII
- 计算机
- HTTP
- HTTPS
- IP
- 浏览器
- HTML
- sed
- nc
- Mac
---

https://en.wikipedia.org/wiki/Backspace
https://zh.wikipedia.org/wiki/%E9%80%80%E6%A0%BC%E9%8D%B5
https://ja.wikipedia.org/wiki/%E3%83%90%E3%83%83%E3%82%AF%E3%82%B9%E3%83%9A%E3%83%BC%E3%82%B9%E3%82%AD%E3%83%BC

https://ja.wikipedia.org/wiki/%E5%89%8A%E9%99%A4%E3%82%AD%E3%83%BC
https://zh.wikipedia.org/wiki/%E5%88%AA%E9%99%A4%E9%8D%B5
https://en.wikipedia.org/wiki/Delete_key

# Backspace 键和 Delete 键的一些冷知识

### Backspace 最初 _不是_ 专门用于删除字符

在早期 **打字机上**，“backspace” 键本质上只是让印字机的横梁向后移动一格，以便重新印字或覆盖字符，而不是真的“抹掉”已经打印的字迹。  
现代计算机里才演变为删除光标前字符的功能。

### ASCII 的 **Delete 字符（127 / DEL）** 原本与键盘无关

它是 ASCII 码表里的最后一个控制字符，最初用于 **纸带（punched tape）时代**标记“这个字符废弃、可以忽略掉”。

- 在纸带上，无论哪个位置出错，只要把所有孔打满（全部为 1），这个字符就会被忽略。
    
- 所以它被称为 _rubout_。[Wikipedia](https://en.wikipedia.org/wiki/Delete_character?utm_source=chatgpt.com)

### Backspace 有两种 ASCII 码对应

在计算机终端中，Backspace 有时会产生 **ASCII 8（^H）**，有时会产生 **ASCII 127（^?）**  
这是因为：

- 早期终端的一些实现把 Backspace 发出的是 `^H`
    
- 另一些终端或系统把 Backspace 映射为 ASCII 127（DEL，即 `^?`）
    
- 所以我们会看到 `stty` 里 erase 设置成 `^?`，但按键实际上是 Backspace 键  
    这样的兼容性遗留让 Unix 文化里出现了用 `^H` 代表“删除”的笑话写法（比如写文本里用 `^H` 来模拟删除动作）。[Wikipedia](https://en.wikipedia.org/wiki/Backspace?utm_source=chatgpt.com)

## 简单总结

| 冷知识点             | 内容                                                                                                                            |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Backspace 的历史用途  | 最初只是向后移动光标，而没真正删除内容（打字机时代）。[Wikipedia](https://en.wikipedia.org/wiki/Backspace?utm_source=chatgpt.com)                        |
| 为什么有 `^H` 和 `^?` | 早期终端历史遗留，不同实现映射不同。[Wikipedia](https://en.wikipedia.org/wiki/Backspace?utm_source=chatgpt.com)                                 |
| Mac Delete 的奇妙命名 | Mac 把 Backspace 标为 Delete，但不是向前删除。[Wikipedia](https://en.wikipedia.org/wiki/Delete_key?utm_source=chatgpt.com)                |
| Delete 键的原始意义    | ASCII DEL 是纸带废弃字符的标记。[Wikipedia](https://en.wikipedia.org/wiki/Delete_character?utm_source=chatgpt.com)                       |
| GUI 中键的不同用法      | Delete 也用于删除对象；Backspace 曾被用作浏览器“后退”键。[窓の杜](https://forest.watch.impress.co.jp/docs/news/1003596.html?utm_source=chatgpt.com) |

^H epanorthosis 義訓（ぎくん） 当て読み（あてよみ）

### epanorthosis 是什么？

- 是一种**修辞格**
    
- 指说话中途 **自我修正 / 反悔 / 加强**

英文可说：

- semantic reading
    
- meaning-based furigana
    
- gikun (直接音译，学界常用)