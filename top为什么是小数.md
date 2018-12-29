# top为什么是小数

### vmstat的r、b字段确实是整数
### 如何计算平均、采样求和除以次数
### 内核实现的时钟



```
sudo sed -Ei 's/^# deb-src /deb-src /' /etc/apt/sources.list
sudo apt-get update
apt-get source coreutils
```

## uptime.c

```
double avg[3];
int loads;
...
loads = getloadavg (avg, 3);

if (loads == -1)
    putchar ('\n');
else {
  if (loads > 0)
    printf (_(",  load average: %.2f"), avg[0]);
  if (loads > 1)
    printf (", %.2f", avg[1]);
  if (loads > 2)
    printf (", %.2f", avg[2]);
  if (loads > 0)
    putchar ('\n');
}
```

```
NAME
       getloadavg - get system load averages

SYNOPSIS
       #include <stdlib.h>

       int getloadavg(double loadavg[], int nelem);
      
RETURN VALUE
       If the load average was unobtainable, -1 is returned; otherwise, the number of samples actually retrieved is returned.
```

The `getloadavg()` function returns **the number of processes in the system run queue averaged over various periods of time**.  Up to `nelem` samples are retrieved and assigned to successive elements of `loadavg[]`.  The system imposes a maximum of 3 samples, representing averages over the last 1, 5, and 15 minutes, respectively.

## glibc getloadavg()

./sysdeps/unix/sysv/linux/getloadavg.c

```
int
getloadavg (double loadavg[], int nelem)
{
  int fd;
  fd = __open_nocancel ("/proc/loadavg", O_RDONLY);
  
```

## Kernel

```
apt source linux-source-4.15.0

./kernel/sched/loadavg.c:11:#include <linux/sched/loadavg.h>
```

```
~/linux-4.15/kernel/sched

gcc -g -O0 -I/usr/src/linux-headers-4.15.0-34-generic/include/ -I/usr/src/linux-headers-4.15.0-34-generic/arch/x86/include/ loadavg.c test_loadavg.c
```

### exponentially decaying average

```
 * Once every LOAD_FREQ:
 *
 *   nr_active = 0;
 *   for_each_possible_cpu(cpu)
 *      nr_active += cpu_of(cpu)->nr_running + cpu_of(cpu)->nr_uninterruptible;
 *
 *   avenrun[n] = avenrun[0] * exp_n + nr_active * (1 - exp_n)
 *              = avenrun[n-1] * exp + nr_active * (1 - exp)
 *
 *   an = a0 * e^n + nr_active * (1 - e^n)
 *   a1 = a0 * e + nr_active * (1 - e)
 *   a2 = a0 * e^2 + nr_active * (1 - e^2)
 *   
```

```
#define EXP_1           1884            /* 1/exp(5sec/1min) as fixed-point */
#define EXP_5           2014            /* 1/exp(5sec/5min) */
#define EXP_15          2037            /* 1/exp(5sec/15min) */

// include/uapi/asm-generic/param.h:6:
#define HZ 100
#define LOAD_FREQ	(5*HZ+1)	/* 5 sec intervals */

/* Variables and functions for calc_load */
atomic_long_t calc_load_tasks;
unsigned long calc_load_update;
unsigned long avenrun[3];

static void calc_global_nohz(void)
{
    ...
    delta = jiffies - sample_window - 10;
    n = 1 + (delta / LOAD_FREQ);

    active = atomic_long_read(&calc_load_tasks);
    active = active > 0 ? active * FIXED_1 : 0;
                
    avenrun[0] = calc_load_n(avenrun[0], EXP_1, active, n);
    avenrun[1] = calc_load_n(avenrun[1], EXP_5, active, n);
    avenrun[2] = calc_load_n(avenrun[2], EXP_15, active, n);
    
    ...
}

static unsigned long
calc_load_n(unsigned long load, unsigned long exp,
            unsigned long active, unsigned int n)
{
    /**
     * fixed_power_int - compute: x^n, in O(log n) time
     *
     * @x:         base of the power
     * @frac_bits: fractional bits of @x
     * @n:         power to raise @x to.
     */

    return calc_load(load, fixed_power_int(exp, FSHIFT, n), active);
}

/*
 * a1 = a0 * e + a * (1 - e)
 * 
 * @param load		-> a0,
 * @param exp			-> e,
 *        fixed_power_int(EXP_1, FSHIFT, 1 + (delta / LOAD_FREQ))
 *        fixed_power_int(EXP_5, FSHIFT, 1 + (delta / LOAD_FREQ))
 *        fixed_power_int(EXP_15, FSHIFT, 1 + (delta / LOAD_FREQ))
 * @param active		-> a,
 * @return 			-> a1
 */
static unsigned long
calc_load(unsigned long load, unsigned long exp, unsigned long active)
{
    unsigned long newload;

	// #define FSHIFT		11		/* nr of bits of precision */
	// #define FIXED_1		(1<<FSHIFT)	/* 1.0 as fixed-point */
	
   /**
    *   avenrun[n] = avenrun[0] * exp_n + nr_active * (1 - exp_n)
    *              = avenrun[n-1] * exp + nr_active * (1 - exp)
    */              
    newload = load * exp + active * (FIXED_1 - exp);
    if (active >= load)
            newload += FIXED_1-1;

    return newload / FIXED_1;
}
```

```
static unsigned long
fixed_power_int(unsigned long x, unsigned int frac_bits, unsigned int n)
{
        unsigned long result = 1UL << frac_bits;

        if (n) {
                for (;;) {
                        if (n & 1) {
                                result *= x;
                                result += 1UL << (frac_bits - 1);
                                result >>= frac_bits;
                        }
                        n >>= 1;
                        if (!n)
                                break;
                        x *= x;
                        x += 1UL << (frac_bits - 1);
                        x >>= frac_bits;
                }
        }

        return result;
}
```

### linux-4.15.0/fs/proc/loadavg.c

```
static int __init proc_loadavg_init(void)
{
    // 看起来这里是在 /proc 里创建了文件 loadavg
    proc_create("loadavg", 0, NULL, &loadavg_proc_fops);
    return 0;
}

// loadavg_proc_fops里应该是操作的回调函数
static const struct file_operations loadavg_proc_fops = {
    .open           = loadavg_proc_open,
    .read           = seq_read,
    .llseek         = seq_lseek,
    .release        = single_release,
};

// 看起来open方法被重写了
static int loadavg_proc_open(struct inode *inode, struct file *file)
{
    return single_open(file, loadavg_proc_show, NULL);
}


static int loadavg_proc_show(struct seq_file *m, void *v)
{
    unsigned long avnrun[3];

    get_avenrun(avnrun, FIXED_1/200, 0);

    seq_printf(m, "%lu.%02lu %lu.%02lu %lu.%02lu %ld/%d %d\n",
            LOAD_INT(avnrun[0]), LOAD_FRAC(avnrun[0]),
            LOAD_INT(avnrun[1]), LOAD_FRAC(avnrun[1]),
            LOAD_INT(avnrun[2]), LOAD_FRAC(avnrun[2]),
            nr_running(), nr_threads,
            idr_get_cursor(&task_active_pid_ns(current)->idr) - 1);
    return 0;
}
```

### 入口函数
```
// /kernel/sched/loadavg.c
/**
 * get_avenrun - get the load average array
 * @loads:      pointer to dest load array
 * @offset:     offset to add
 * @shift:      shift count to shift the result left
 *
 * These values are estimates at best, so no need for locking.
 */
void get_avenrun(unsigned long *loads, unsigned long offset, int shift)
{
        loads[0] = (avenrun[0] + offset) << shift;
        loads[1] = (avenrun[1] + offset) << shift;
        loads[2] = (avenrun[2] + offset) << shift;
}
```

```
./fs/proc/loadavg.c:20:	get_avenrun(avnrun, FIXED_1/200, 0);
./include/linux/sched/loadavg.h:16:extern void get_avenrun(unsigned long *loads, unsigned long offset, int shift);
./kernel/sys.c:2476:	get_avenrun(info->loads, 0, SI_LOAD_SHIFT - FSHIFT);
```
