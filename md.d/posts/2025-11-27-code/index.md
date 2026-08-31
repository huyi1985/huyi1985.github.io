---
title: code
date: '2025-11-27'
---

```c
// usr/sys/conf/c.c
struct    cdevsw    cdevsw[] =
{
    ...
    nulldev, nulldev, mmread, mmwrite, nodev, nulldev, 0,     /* mem = 8 */
    ...
    
// usr/sys/dev/mem.c
/*
 * Memory special file
 * minor device 0 is physical memory
 * minor device 1 is kernel memory
 * minor device 2 is EOF/RATHOLE
 */

...
 
mmread(dev)
{
    ...
    if(minor(dev) == 2)
        return;
    ...
}

mmwrite(dev)
{
    ...
    if(minor(dev) == 2) {
        u.u_count = 0;
        return;
    }
    ...
}
```