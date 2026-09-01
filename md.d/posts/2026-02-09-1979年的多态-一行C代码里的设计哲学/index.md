---
title: 1979年的多态：一行C代码里的设计哲学
date: '2026-02-09'
tags:
- Unix
- Linux
- BSD
- 内核
- 命令
- 指令
- 文件
- 系统调用
- Bell Laboratories
- 贝尔实验室
- Ken Thompson
- Dennis Ritchie
- PDP-11
- V7
- time-sharing
- C语言
- C++
- Go
- Java
- 代码
- code
- 函数
- 参数
- 语法
- 类型
- 指针
- 设备
- 性能
- IP
- sed
- nc
- vi
- 数据
- 索引
- AI
- 模型
- Windows
- 编译
- 构建
- 工程师
draft: true
---

# 1979年的多态：一行C代码里的设计哲学

## 引子

1979年1月，当Dennis Ritchie和Ken Thompson在贝尔实验室发布UNIX第七版时，面向对象编程还是个模糊的学术概念。Smalltalk-76刚刚在施乐帕克研究中心崭露头角，而C++要到1985年才会问世。然而，在V7的内核代码中，有一行看似平淡无奇的C语句，却已经展现出了多态的精髓：

```c
(*cdevsw[major(dev)].d_ioctl)(dev, uap->cmd, uap->cmarg, fp->f_flag);
```

这行代码位于`usr/sys/dev/tty.c`第161行，是ioctl系统调用的核心调度逻辑。它用纯粹的C语言，在没有class、没有继承、没有虚函数的年代，实现了一个优雅的多态系统。

## 问题：设备多样性的困境

1979年的UNIX需要支持各种各样的设备：

- DZ11串口控制器
- DH11多路复用器
- LP11行式打印机
- RK05磁盘驱动器
- TU10磁带机

每种设备都有不同的控制命令。传统的做法可能是：

```c
// 反面教材：设备类型判断地狱
ioctl(int fd, int cmd, void *arg) {
    if (device_type == DZ11) {
        // DZ11 特定处理
        if (cmd == SET_BAUD_RATE) { ... }
        else if (cmd == SET_PARITY) { ... }
        // ... 数十个判断
    } else if (device_type == DH11) {
        // DH11 特定处理
        if (cmd == ...) { ... }
        // ... 又是数十个判断
    } else if (device_type == LP11) {
        // ...
    }
    // 这将是一个数千行的怪物函数
}
```

这种做法的问题显而易见：
- 添加新设备需要修改核心代码
- 函数体积膨胀
- 编译时间线性增长
- 维护成本高昂

## 方案：函数指针表的多态

贝尔实验室的工程师选择了另一条路。让我们拆解这行代码：

```c
(*cdevsw[major(dev)].d_ioctl)(dev, uap->cmd, uap->cmarg, fp->f_flag);
 ^        ^          ^         ^
 |        |          |         |
 |        |          |         +-- 实际调用，传递参数
 |        |          +-- 取出函数指针
 |        +-- 提取主设备号作为数组`cdevsw`的索引
 +-- 函数指针解引用
```

### 数据结构：设备驱动契约

在`usr/src/sys/h/conf.h`中定义了设备驱动的"契约"：

```c
struct cdevsw {
    int (*d_open)();
    int (*d_close)();
    int (*d_read)();
    int (*d_write)();
    int (*d_ioctl)();    // ioctl方法指针
    int (*d_stop)();
    struct tty *d_ttys;
};
```

这个结构体相当于后来面向对象语言中的"接口"或"抽象基类"。每个设备驱动必须提供这些函数的实现。

### 设备驱动表：静态绑定

在`usr/src/sys/sys/conf.c`中构建了全局驱动表：

```c
struct cdevsw cdevsw[] = {
    /* major 0 */ { cnopen, cnclose, cnread, cnwrite, cnioctl, nulldev, 0 },
    /* major 1 */ { dzopen, dzclose, dzread, dzwrite, dzioctl, dzstop, dz_tty },
    /* major 2 */ { syopen, nulldev, syread, sywrite, syioctl, nulldev, 0 },
    /* major 3 */ { nulldev, nulldev, mmread, mmwrite, nodev, nulldev, 0 },
    // ...
};
```

这是一个二维的函数指针表：
- 第一维：设备主设备号（major number）
- 第二维：操作类型（open/close/read/write/ioctl/stop）

### 运行时调度：动态分派

当用户调用`ioctl(fd, cmd, arg)`时：

1. **设备识别**：从文件描述符`fd`获取设备号`dev`
2. **索引计算**：`major(dev)`提取主设备号（如1代表DZ11）
3. **函数查找**：`cdevsw[1].d_ioctl`找到`dzioctl`函数
4. **动态调用**：通过函数指针调用，传递参数

整个过程是**O(1)**时间复杂度，没有任何条件判断。

## 深入：为什么这是多态？

多态的本质是：**同一个操作作用于不同的对象，可以有不同的解释和实现**。

在这个系统中：
- **统一接口**：所有设备驱动都提供`d_ioctl`函数
- **不同实现**：`dzioctl`、`cnioctl`、`syioctl`各不相同
- **动态绑定**：根据设备类型在运行时选择正确的实现
- **封装细节**：调用者不需要知道具体设备类型

用伪代码表示面向对象的等价形式：

```cpp
// C++ 伪代码（1985年才出现）
class DeviceDriver {
public:
    virtual int ioctl(dev_t dev, int cmd, caddr_t arg, int flag) = 0;
};

class DZ11Driver : public DeviceDriver {
public:
    int ioctl(dev_t dev, int cmd, caddr_t arg, int flag) override {
        // DZ11 特定实现
    }
};

// 调用
DeviceDriver* driver = driverTable[major(dev)];
driver->ioctl(dev, cmd, arg, flag);  // 虚函数调用
```

C语言版本和C++版本在**语义上完全等价**，都是：
1. 定义统一接口（`cdevsw`结构体 vs 虚基类）
2. 不同实现（函数指针 vs 虚函数）
3. 通过表查找（函数指针表 vs 虚函数表）

事实上，C++的虚函数表（vtable）机制很可能受到了UNIX这种设计的启发。

## 实例：DZ11驱动的实现

看看具体的设备驱动如何实现这个契约（`usr/src/sys/sys/dz.c`）：

```c
dzioctl(dev, cmd, addr, flag)
caddr_t addr;
dev_t dev;
{
    register struct tty *tp;

    tp = &dz_tty[minor(dev)];

    // 委托给通用TTY处理函数
    if (ttioccomm(cmd, tp, addr, dev)) {
        // 某些命令需要设备特定的后处理
        if (cmd == TIOCSETP || cmd == TIOCSETN)
            dzparam(minor(dev));  // 设置DZ11硬件参数
    } else {
        u.u_error = ENOTTY;  // 不支持的命令
    }
}
```

这里展现了另一层设计：
1. **职责分层**：通用TTY操作由`ttioccomm`处理
2. **特化处理**：设备特定操作在驱动中实现
3. **代码复用**：避免在每个驱动中重复通用逻辑

## 影响：设计思想的传承

这种设计模式影响深远：

### 1. Linux内核（1991-至今）

Linux内核的设备驱动系统几乎是原样继承：

```c
// linux/fs.h
struct file_operations {
    ssize_t (*read) (struct file *, char __user *, size_t, loff_t *);
    ssize_t (*write) (struct file *, const char __user *, size_t, loff_t *);
    long (*unlocked_ioctl) (struct file *, unsigned int, unsigned long);
    // ...
};
```

### 2. Windows驱动模型（1993-至今）

Windows的I/O管理器也使用类似的分发表：

```c
typedef struct _DRIVER_OBJECT {
    PDRIVER_INITIALIZE DriverInit;
    PDRIVER_STARTIO DriverStartIo;
    PDRIVER_UNLOAD DriverUnload;
    PDRIVER_DISPATCH MajorFunction[IRP_MJ_MAXIMUM_FUNCTION + 1];
    // ...
} DRIVER_OBJECT;
```

### 3. 面向对象范式

C语言的这种实践反过来影响了OOP语言的设计：
- 接口/协议的概念
- 虚函数表的实现机制
- 依赖倒置原则（Dependency Inversion Principle）

## 性能考量

有人可能会问：函数指针调用是否有性能开销？

1979年的答案是：**有，但值得**。

函数指针调用需要：
- 一次数组索引（`cdevsw[major]`）
- 一次结构体成员访问（`.d_ioctl`）
- 一次间接跳转（`(*func_ptr)(...)`）

对比if-else链：
- 平均需要N/2次比较
- 代码缓存效率差
- 分支预测失败率高

在PDP-11和VAX这样的小型机上，函数指针调用的开销是**3-5条指令**，而大型if-else链可能需要**数百次比较**。权衡之下，函数指针表是明智的选择。

更重要的是，这种设计带来的**可维护性和可扩展性**是无价的。贝尔实验室的工程师不是在追求微观性能，而是在追求**系统的优雅性**。

## 现代启示

2025年的今天，我们已经习惯了Rust的trait、Go的interface、Java的多态。但在1979年，用纯粹的C语言构建这样一个系统，需要的不仅是技术能力，更是**设计洞察力**。

这行代码告诉我们：

1. **多态不依赖语言特性**：核心是思想，而非语法糖
2. **约束激发创造力**：C语言的限制反而促成了更清晰的设计
3. **简单性是终极复杂性**：看似简单的一行代码，背后是整个架构的支撑
4. **好的设计超越时代**：45年后，这个模式依然在无数系统中使用

## 结语

当我们在2025年讨论Clean Architecture、SOLID原则、依赖注入时，不妨回头看看1979年的这行代码。它没有花哨的语法，没有框架的支持，只有函数指针、结构体和数组。

但它实现了：
- 开闭原则（Open-Closed Principle）：对扩展开放，对修改关闭
- 依赖倒置原则（Dependency Inversion）：高层模块不依赖低层模块
- 接口隔离原则（Interface Segregation）：每个驱动只实现需要的函数

Dennis Ritchie和Ken Thompson可能从未读过设计模式的书（《Design Patterns》要到1994年才出版），但他们在实践中发现了这些永恒的真理。

这就是工程的美学：**在约束中寻找优雅，在简单中追求深刻**。

---

## 附录：代码溯源

### 相关源文件位置

**UNIX V7 (1979)**
- 系统调用实现：`usr/sys/dev/tty.c:136-168`
- 设备驱动表：`usr/src/sys/sys/conf.c:69-91`
- 驱动接口定义：`usr/src/sys/h/conf.h:29`
- DZ11驱动实现：`usr/src/sys/sys/dz.c:192-204`

**BSD 3 (1980)**
- 系统调用实现：`usr/src/sys/sys/tty.c:136-168`
- stty/gtty封装：`usr/src/sys/sys/tty.c:117-129`

### 历史时间线

| 时间 | 事件 |
|------|------|
| 1971年 | UNIX V1 发布，使用 stty/gtty 系统调用 |
| 1975年 | UNIX V6 发布，依然使用 stty/gtty |
| **1979年1月** | **UNIX V7 发布，引入 ioctl（系统调用54）** |
| 1980年1月 | BSD 3 发布，采用 ioctl，重构 stty/gtty 为封装 |
| 1985年 | C++ 1.0 发布，引入虚函数概念 |
| 1991年 | Linux 0.01 发布，继承 UNIX ioctl 设计 |
| 1994年 | 《Design Patterns》出版 |

---

**参考文献：**
- UNIX V7 Source Code, `/usr/sys/dev/tty.c`, Bell Laboratories, 1979
- UNIX V7 Source Code, `/usr/src/sys/sys/conf.c`, Bell Laboratories, 1979
- BSD 3 Source Code, `/usr/src/sys/sys/tty.c`, UC Berkeley, 1980
- Ritchie, Dennis M. "The Evolution of the Unix Time-sharing System", 1984
- Lions, John. "Lions' Commentary on UNIX 6th Edition", 1977
- Stroustrup, Bjarne. "The Design and Evolution of C++", 1994
