Linux IO耗时指标

/data
dd if=/dev/urandom of=sample.data bs=64M count=16

echo 1 > /proc/sys/vm/drop_caches
iostat -hkcx /dev/vda3 1

```c
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

// gcc -D_GNU_SOURCE random_read_file_on_disk.c
//  error: ‘O_DIRECT’ undeclared (first use in this function)
int main() {
   sleep(10);
   time_t t;

   /* Intializes random number generator */
   srand((unsigned) time(&t));

    char *filename = "/data/sample.data";
    // int fd = open(filename, O_RDONLY | O_SYNC);
    int fd = open(filename, O_RDONLY);

    struct stat st;
    stat(filename, &st);
    int filesize = st.st_size;

    int i = 0;
    char *c = (char *) calloc(8 * 1024, sizeof(char));
    for (i = 0; i < 100000000; i++) {
        int offset = rand() % filesize;
        lseek(fd, offset, SEEK_SET);
        int n = read(fd, c, 8 * 1024);
        // perror("read error: ");
        // printf("%d %d %d  %hhx %hhx %hhx %hhx\n", filesize, offset, n, c[0], c[1], c[2], c[3]);
    }
}
```

>>> 
JackalHu:
$N = isset($argv[1]) ? $argv[1] : 10000;
$C = isset($argv[2]) ? $argv[2] : 64;

$file = "/data/sample.data";
$handler = fopen($file, "rb");
$filesize = filesize($file);

for ($i = 0; $i < $N; $i++) {
        fseek($handler, mt_rand(0, $filesize));
        $data = fread($handler, 4096 * 64);
        // echo substr($data, 0, 16), PHP_EOL;
}

和我想的有点不一样啊，iostat和pidstat里和io read相关的指标还是0

王木杉:
预计命中page_cache了

王木杉:
改为直接io再试试呢

JackalHu:
嗯 我改为C语言的 以为随机读能降低page cache命中率呢

王木杉:
go有个工具，可以看page_cache

JackalHu:
应该就是page cache，echo 1 > /proc/sys/vm/drop_caches
一下，iowait和r/s，就有值了

JackalHu:
O_DIRECT加上read报错了，O_SYNC好像没啥用


