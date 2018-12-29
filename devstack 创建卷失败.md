# devstack 创建卷失败

[https://s3-ap-northeast-1.amazonaws.com/huyi07-images/WechatIMG79.jpeg]

```
tail -ff syslog | fgrep -v dstat | fgrep cinder

Nov 28 12:52:47 devstack cinder-scheduler[1003]:...Setting Volume e246c8ac-09d8-44f5-ad55-edca909dad16 to error due to: No valid backend was found. No weighed backends available...
```


https://www.ibm.com/developerworks/community/blogs/132cfa78-44b0-4376-85d0-d3096cd30d3f/entry/%E5%87%86%E5%A4%87_LVM_Volume_Provider_%E6%AF%8F%E5%A4%A95%E5%88%86%E9%92%9F%E7%8E%A9%E8%BD%AC_OpenStack_49?lang=en_us

Cinder 真正负责 Volume 管理的组件是 volume provider。

Cinder 支持多种 volume provider，LVM 是默认的 volume provider。

Devstack 安装之后，/etc/cinder/cinder 已经配置好了 LVM，如下图所示： 

```
/etc/cinder/cinder.conf

[DEFAULT]
default_volume_type = lvmdriver-1
enabled_backends = lvmdriver-1

[lvmdriver-1]
image_volume_cache_enabled = True
volume_clear = zero
lvm_type = auto
target_helper = tgtadm
volume_group = stack-volumes-lvmdriver-1
volume_driver = cinder.volume.drivers.lvm.LVMVolumeDriver
volume_backend_name = lvmdriver-1
```
 

上面的配置定义了名为“lvmdriver-1”的 volume provider，也称作 backend。其 driver 是 LVM，LVM 的 volume group 名为“stack-volumes-lvmdriver-1”。 

Devstack 安装时并没有自动创建 volume group，所以需要我们手工创建。 如下步骤演示了在 /dev/sdb 上创建 VG “stack-volumes-lvmdriver-1”： 

1. 首先创建 physical volume /dev/sdb

`# pvcreate /dev/sdb`

Linux 的 lvm 默认配置不允许在 /dev/sdb 上创建 PV(`Device /dev/sdb not found (or ignored by filtering). `)，需要将 sdb 添加到 /etc/lvm.conf 的 filter 中。

`
global_filter = ["a|sdb|", "a|loop0", ...
`

```
# vgs
  VG                        #PV #LV #SN Attr   VSize  VFree
  stack-volumes-lvmdriver-1   1   0   0 wz--n- 50.00g 50.00g
```

2. 然后创建 VG stack-volumes-lvmdriver-1

```
# vgcreate stack-volumes-lvmdriver-1 /dev/sdb
  Volum group "stack-volumes-lvmdriver-1" successfully created
```
	 
打开 Web GUI，可以看到 OpenStack 已经创建了 Volume Type “lvmdriver-1”

![](http://7xo6kd.com1.z0.glb.clouddn.com/upload-ueditor-image-20160619-1466308846897026680.jpg)

其 Extra Specs volume\_backend\_name 为 lvmdriver-1

![](http://7xo6kd.com1.z0.glb.clouddn.com/upload-ueditor-image-20160619-1466308847169012123.jpg)

后面各小节都将以 LVM 为 volume provider 详细讨论 volume 的各种操作。 

