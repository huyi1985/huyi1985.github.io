---
title: code
date: '2026-09-10'
tags:
- Java
- JavaScript
- 代码
- 函数
- 参数
- 语法
- 字符
- 字符串
- IP
- 浏览器
- HTML
- nc
draft: true
---

```javascript
b = (e) => document.body.innerHTML = m(
  73,
  e || [~9, ..."1172711", ~9]
    .map(j => m[i -= j] ? ++e : i)
    .map(
      j => b(b[i = j] ^ 1 | e),
      b[i] = !m[C--, i] * ~e
    )
);

b(
  m = (t) => t-- ? `<a onmouseup=b(b[i=${t}]^=event.which)>${
    t % 9
      ? "*#F"[
        x = b[t] ??= (
          C -= m[t] = Math.random() < .1,
          1
        )
      ] ?? ~x
      : "<p>"
  }` + m(t) : C,
  C = 64
)
```

* `function b(e) { document.body.innerHTML = m(73, <second_param>); }`
* `function m(t) {}`， 但是调用时可以多传递参数：`b(<first_param>, C=64)`
* `b()` 的同时可以 `b[]`
* `${...}`就是JavaScript模板字符串（template literal）里的字符串插值语法
* `function b(e) {...} b()`
* `b`负责“状态变化→重新渲染”，`m`负责“状态→HTML”
* 技巧：原始代码中根本没有结束`</p>`标签`</a>`，浏览器不允许`<a>`标签包含自身，也不允许`<p>`标签包含自身。
* 带有旗帜和数字的可见棋盘，以及指示地雷位置的实际棋盘。我们恰好有两个可以使用的对象——`and`b函数m！
* 棋盘上所有可见单元格都b被初始化1，并随机生成一个雷区，m其中有 10% 的概率存在地雷。初始化后，C剩余的单元格数量即为玩家需要探索的安全单元格总数。