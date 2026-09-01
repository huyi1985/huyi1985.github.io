---
title: Unix V1 sysfork — 空闲进程槽查找
date: '2026-02-24'
tags:
- Unix
- 进程
- 系统调用
- PDP-11
- 代码
- return
- 字节
- 循环
- PC
- sed
- nc
- 索引
draft: true
---

# Unix V1 sysfork — 空闲进程槽查找

## 原始代码（PDP-11 汇编中 `/` 表示注释）

```asm
nproc = 16. / number of processes

sysfork: / create a new process
	clr	r1
1: / search p.stat table for unused process number
	inc	r1
	tstb	p.stat-1(r1) / is process active, unused, dead
	beq	1f / it's unused so branch
	cmp	r1,$nproc / all processes checked
	blt	1b / no, branch back
	add	$2,18.(sp) / add 2 to pc when trap occured, points
		           / to old process return
	br	error1 / no room for a new process
1:
```

## 逐行注释

# Unix V1 sysfork — 空闲进程槽查找
```asm
nproc = 16.                  	; 常量：进程表最多16个槽位

sysfork:                     	; fork 系统调用入口
	clr	r1               		; r1 = 0，用作进程表索引
1:                           	; 循环开始
	inc	r1               		; r1++，进程号从 1 开始（0 是系统进程，不分配）
	tstb	p.stat-1(r1)     	; 测试 p.stat[r1-1] 这个字节，设置零标志位
	                         	; -1 是因为 r1 从 1 开始，而数组从 0 开始
	                         	; r1=1 时访问 p.stat[0]，r1=2 时访问 p.stat[1]，以此类推
	beq	1f               		; 如果为 0（空闲），跳转到下方(forward)的 1: 标签 → 跳出循环
	                         	; 1f 的 f = forward，即代码中往下找最近的 1: 标签
	cmp	r1,$nproc        		; r1 和 16 比较
	blt	1b               		; r1 < 16 → 跳转到上方(backward)的 1: 标签 → 回到循环开始
	                         	; 1b 的 b = backward，即代码中往上找最近的 1: 标签
	...
1:                           	; r1 = 找到的空闲槽位编号
```
