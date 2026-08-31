---
title: 极客的幽默：fool^H^H^H\^Hgentleman
date: '2026-01-12'
---

# 极客的幽默：fool^H^H^H\^Hgentleman

> Be nice to this **fool^H^H^H^Hgentleman**; he's visiting from corporate HQ.  
> （对这位来自总部的××友好点。）

这句话里的 `^H` 是什么意思？是某种古老的颜文字吗？  

而这位来自总部的同事，到底是“fool”（傻瓜）还是“gentleman”（绅士）呢？

要理解 `^H`，得先从 ASCII 的**控制字符**以及它的**表记方法**说起。不过为了简单，我们先讲结论：

- 一个 `^H` 就相当于按了一次删除键（退格键，← Backspace 或 ⌫）
- 句子里连续 4 个 `^H` 刚好把前面的 “f-o-o-l” 4 个字母删掉，只留下 “gentleman”

表面上是删掉了 “fool”，实际上是表面一套，心里另一套，阳奉阴违，**暗讽来自总部的同事**。

好了，你已经知道 `^H` 的意思了。下面的内容非常无聊^H^H^H^H 十分有趣！
## ASCII 控制字符与 caret notation

要理解 `^H`，我们得先聊聊 **ASCII 的控制字符** 和 **caret notation（脱字符表记法）**。

ASCII 中有一类特殊字符，叫作**控制字符**（control characters）。这些字符不是用来表示语言文字的，不会显示到屏幕上，而是用来控制终端或设备的行为。按下回车键输入的**换行符**就是典型的控制字符之一。

为了方便表示这些不可见字符，除了使用缩写的名称，如 `CR`、`LF` 等，人们还发明了称为 **caret notation** 的表记法。其规则很巧妙：用 `^` 后面跟一个大写字母表示一个 ASCII 控制码。字母 A 对应控制码 1（`^A`），B 对应 2（`^B`）……一直到 Z 对应 26。

而 `H` 是字母表中的第 8 个字母，所以 `^H` 就对应 **ASCII 控制码 8**。这个控制码的标准缩写是 BS，也就是 **BackSpace（退格键）** 的意思。

换句话说，当你在终端里看到 `^H`，它其实是在告诉你：“你刚刚按了一次退格键，把前面一个字符删掉了。”可以用下面的命令体验按下删除键后的效果：

```
$ stty -icanon 
$ jq . 
Hello^?  

# 用退格键删除字母o
# 体验完记得用 stty sane 复原终端
```

caret notation 不仅限于 `^A`～`^Z`，还有：

- `^@` 表示 NUL（ASCII 0）
- `^[` 表示 ESC（ASCII 27）
- `^?` 表示 DEL（ASCII 127）

我们还可以把 `^H` 理解为：

- **HTML** 中的 `<s>fool</s>`gentleman
- **Markdown** 中的 `~~fool~~gentleman**`
- **编程语言** 中的 `/*fool*/gentleman`

表面上是“删掉文字”，实际上是在传递**作者微妙的态度**。