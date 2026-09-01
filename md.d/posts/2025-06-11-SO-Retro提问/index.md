---
title: SO Retro提问
date: '2025-06-11'
tags:
- Unix
- 命令
- 文件
- man
- 系统调用
- system call
- Go
- Java
- 代码
- cat
- sed
- nc
- AI
---

%% Unix上的touch命令为什么叫touch，与new/create/update有什么联系

touch命令用于更新文件的访问时间（atime）和修改时间（mtime），或是创建新文件。我的母语不是英语，所以一直很好奇为什么touch会和update或create有关（按照系统调用的写法，应该写作拼写错误的creat）。

touch这个动作会让我想到一幅名画，Sistine Chapel上Michelangelo的The Creation of Adam。上帝伸出右手手指，亚当也抬起手指回应，两人的指尖几乎相触。这一瞬间倒是有“创造”的含义。

这两天在读《Seven Languages in Seven Weeks》这本书的时候，发现一段介绍Scala中mutable和immutable区别的代码，从上下文来看，touch倒是也和change/update有点关联，不过我的英语水平是体会不到其中的微妙联系了。 %%

**Why is the Unix command `touch` called _touch_? How is it related to new/create or update?**

The Unix `touch` command is used to **update** a file’s access time (`atime`) and modification time (`mtime`), or to **create**(misspelled `creat` in system call) a new file. Since English isn’t my first language, I’ve always wondered why this kind of action is called _touch_.

The word makes me think of Michelangelo’s _The Creation of Adam_, where God and Adam reach out and their fingers nearly ***touch***. In that moment, _touch_ seems to carry a sense of **creation**.

While reading _Seven Languages in Seven Weeks_ recently, I saw a Scala example explaining mutable vs. immutable data. In that context, **_touch_** also seemed to suggest a small change or **update**.

I’m not sure I fully understand the nuance. Would love to hear how native speakers or longtime Unix users interpret the choice of the word.

```scala
scala> var mutable = "I am mutable"
mutable: java.lang.String = I am mutable

scala> mutable = "Touch me, change me..."
mutable: java.lang.String = Touch me, change me...

scala> val immutable = "I am not mutable"
immutable: java.lang.String = I am not mutable

scala> immutable = "Can't touch this"
<console>:5: error: reassignment to val
```