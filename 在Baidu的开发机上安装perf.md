# 在开发机上安装perf

## issue 1
gcc好像默认带 -Werror 这个flag

```
./configure --prefix=/opt/gcc-4.9.4/ --enable-languages=c,c++ --disable-multilib
enable-multilib
```
