---
title: pip install mahjong
date: '2025-07-01'
---

如果你喜欢打麻将🀄️，又刚好学了一点Python编程🐍，那说不定会对“mahjong”这个开源项目感兴趣。

只需几行代码就可以判断出是不是“上听”了或者能不能“和牌”，甚至还能算出番数。

这些功能对进行麻将模拟或者编写麻将AI都非常有用。

```python
# pip install mahjong
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.tile import TilesConverter
from mahjong.agari import Agari

# 创建一副麻将牌（共14张），代表一副可能的和牌形
# man 表示“万”，pin 表示“筒”，sou 表示“索”
# 这副牌是：2,3,4,5,5,5 万；5,5,5 筒；2,2,5,5,5 索
tiles = TilesConverter.string_to_136_array(
	man='234555', pin='555', sou='22555')

# 指定“和牌牌”——也就是最后一张摸到的牌，这里是“5索”
win_tile = TilesConverter.string_to_136_array(sou='5')[0]

# 创建 Agari 实例，用于判断是否能和牌（是否是合法的胡牌形）
agari = Agari()
print("能否和牌：", agari.is_agari(
	TilesConverter.to_34_array(tiles)))

# 创建得分计算器实例
calculator = HandCalculator()

# 估算这副牌的番数、符数和总得分
result = calculator.estimate_hand_value(tiles, win_tile)

# 打印结果（包含番型、得分等信息）
print(result)

# 打印详细的符数计算项（例如门前清、对对和、头牌符等）
for fu_item in result.fu_details:
    print(fu_item)


# 输出结果
# 能否和牌： True
# 3 han, 40 fu
# {'fu': 30, 'reason': 'base'}
# {'fu': 4, 'reason': 'closed_pon'}
# {'fu': 4, 'reason': 'closed_pon'}
# {'fu': 2, 'reason': 'open_pon'}

```