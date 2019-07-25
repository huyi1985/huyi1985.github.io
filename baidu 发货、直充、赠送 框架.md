# baidu 发货、直充、赠送 框架

## 直充

```
$row = fetch by UNIQUE INDEX

if (!empty($row) && $row['status'] == 'SUCCESS') {
	return SUCCESS;	// 幂等性，重复直充第一次返回成功，以后也依然返回成功。
                    // 因为直充成功的响应可能因为网络问题，导致调用方没有收到
}

if (empty($row)) {
	START Transaction
	
	// UNIQUE	index
	// 若并发请求该接口插入直充记录，只有一个请求能插入，其他请求阻塞在这里，直到那个能插入的请求commit
	
	// 1. 创建本地订单
	//       |- [!] 有一部分并发直充的请求“死”在这里，DUPLICATED
	// 2. 创建度秘订单，调用order模块接口创建订单，无法回滚
	$order = call_api()
	// 3. 关联直充记录和本地订单
	
	COMMIT       
} else {
	$order = fetch By Dumi Order Id
		|- [!] 有一部分并发直充请求拿到了order，但一个order只能成功发货一次！
}

// 发货，满足幂等性，一个order只能成功发货一次！
deliverItems($order)
	|- 这里面又会打开-提交事务

// 发货成功
// 4. 将度秘订单状态置为【已完成】
// 5. 更新partner_subscription表
```