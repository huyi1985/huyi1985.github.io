```sql
[2019-11-11 11:38:32] production.INFO: select * from `jz_customer` where `bd_id` = "6962" and `status` in (0, 2) and `customer_type` = 1 | pathInfo: /api/customer/assign | elapsed: 291.51 ms | total: 305.38 ms (95.4581177549%) | 2/15 

-->

覆盖索引
select `id` from `jz_customer` where `bd_id` = "6962" and `status` in (0, 2) and `customer_type` = 1 
```


```bash

cd  /data/www/html/jz_crm_customer
fgrep 'customer/assign' storage/logs/laravel-2019-11-11.log  | grep -P 'select \* from `jz_customer` where `bd_id` = "[0-9]+" and `status` in \(0, 2\) and `customer_type` = 1'  | awk '{print $1, $2, $25, $26}' 
> /tmp/sql.log

fgrep 'customer/assign' storage/logs/laravel-2019-11-11.log  | grep -P 'select `id` from `jz_customer` where `bd_id` = "[0-9]+" and `status` in \(0, 2\) and `customer_type` = 1'  | awk '{print $1, $2, $25, $26}' 

fgrep 'customer/assign' ./www/jz_crm_customer/storage/logs/laravel-2019-11-11.log  | grep -P '`jz_customer` where `bd_id` = "[0-9]+" and `status` in \(0, 2\) and `customer_type` = 1'  | awk '{print $1, $2, $25, $26}' | tr -d '[]' > ~/huyi1/sql.csv
```

