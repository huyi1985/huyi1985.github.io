# 斗兽棋接口文档

## 坐标
![387b7b2983a6691d34b3ed52c.png](http://bos.nj.bpc.baidu.com/ibox-thumbnail98/2cc69f84b79515e6dcc200d7ffdeaaee?authorization=bce-auth-v1%2Faa63c2039e006dd7e80698dcc7c78d36%2F2018-11-23T10%3A27%3A14Z%2F1800%2F%2F139e5a02ffac6ff09ad99f2dbb8850e82ac5836ce26e959de4df5083c7ed71ef)

## POST /rule
玩家走棋

### Request
```
{
    "board": {          // key是棋子的code，value是棋子的坐标
        "11": 56,
        "12": 10,
        "13": 20,
        "14": 46,
        "15": 38,
        "16": 0,
        "17": 54,
        "18": 2,
        "21": 6,
        "22": 52,
        "23": 42,
        "24": 16,
        "25": 24,
        "26": 62,
        "27": 8,
        "28": 60
    },
    "pieceId": 18,
    "gridIdx": 3	
}
```

|字段|类型|含义|
|-|-|-|
|board|array|棋盘数据，key是棋子的code，value是棋子的坐标|
|pieceId|int|玩家棋子的code|
|gridIdx|int|玩家棋子移动的目标位置|

### Response
```
{
    "errno": 0,
    "data": {
        "board": {
            "11": 56,
            "12": 10,
            "13": 20,
            "14": 46,
            "15": 38,
            "16": 0,
            "17": 54,
            "18": 34,
            "21": 6,
            "22": 52,
            "23": 42,
            "24": 16,
            "25": 24,
            "26": 62,
            "27": 8,
            "28": 60
        },
        "isOk": false,
        "finished": false,
        "hint": "不能这样移动"
    }
}
```
|字段|类型|含义|
|-|-|-|
|errno|int|错误码|
|data.board|array|棋盘数据，key是棋子的code，value是棋子的坐标|
|data.isOk|bool|玩家走的棋是否符合规则|
|data.finished|bool|本局是否结束|
|data.hint|string|提示语。当`data.isOk`为`false`时，提示语是玩家的走法违反的规则；当`data.finished`为`true`时，提示语是哪方获胜的信息|



## GET /ai
电脑走棋

### Request
```
{
    "board": {
        "11": 56,
        "12": 10,
        "13": 20,
        "14": 46,
        "15": 38,
        "16": 0,
        "17": 54,
        "18": 2,
        "21": 6,
        "22": 52,
        "23": 42,
        "24": 16,
        "25": 24,
        "26": 62,
        "27": 8,
        "28": 60
    }
}
```
|字段|类型|含义|
|-|-|-|
|board|array|棋盘数据，key是棋子的code，value是棋子的坐标|

### Response

 