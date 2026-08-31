---
title: Ref 明文密码是否会显示在纸上
date: '2025-12-25'
---

柯林翰 一切都是纸

input password显示为*

should be suid with owner

是的！找到了 passwd 的 man 手册，而且发现了一个关键证据。

  手册文件

  1. passwd(I) 命令手册 - usr/doc/man/man1/passwd.1
  2. passwd(V) 文件格式 - usr/doc/man/man5/passwd.5

  关键证据

  SYNOPSIS（用法）：
  passwd name password

  手册明确要求密码作为命令行参数！

  BUGS 部分：
  .sh BUGS


  完全为空 - 说明当时认为这没有问题。

  渲染后的效果

  用户执行 man passwd 会看到：

  PASSWD(I)                  9/1/72                  PASSWD(I)

  NAME
       passwd - change login password

  SYNOPSIS
       passwd name password          ← 明确的用法

  DESCRIPTION
       The password becomes associated with the given login name.
       This can only be done by corresponding user or by the
       super-user.  An explicit null argument ("") for the password
       argument removes any password.

  FILES
       /etc/passwd

  SEE ALSO
       login(I), passwd(V), crypt(III)

  BUGS
                                     ← 空的！

  核心结论

  1. ✅ 不是 bug，是设计：手册明确写明 passwd name password
  2. ❌ 没有安全警告：BUGS 部分为空
  3. ✅ 手册与代码一致：
    - 手册：passwd name password
    - 代码：if(argc != 3)
  4. ✅ 这反映了 1972 年的安全观念

  特殊功能：删除密码

  手册还说明了一个有趣的功能：

  $ passwd alice ""    # 传递空字符串删除密码

  删除密码后，用户登录时不需要输入密码！

  我已经创建了详细分析：claudedocs/passwd_manual_analysis.md

  这份手册是最有力的证据，证明 passwd 的命令行参数设计是当时的标准做法，而不是一个疏忽。这反映了 1972
  年与现代截然不同的安全意识和威胁模型。