---
title: 参考
date: '2025-05-30'
draft: true
---

# 参考

https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/units-of-measure

https://zh.wikipedia.org/wiki/%E5%8A%A0%E6%8B%BF%E5%A4%A7%E8%88%AA%E7%A9%BA143%E8%99%9F%E7%8F%AD%E6%A9%9F%E4%BA%8B%E6%95%85

Floating point and signed integer values in F# can have associated **units of measure**, which are typically used to indicate length, volume, mass, and so on. By using **quantities with units**, you enable the compiler to verify that arithmetic relationships have the correct units, which helps prevent programming errors.

Syntax

```F#
[<Measure>] type unit-name [ = measure ]
```

Remarks

The previous syntax defines `unit-name` as a unit of measure. The optional part is used to define a new `measure` in terms of previously defined units. For example, the following line defines the measure `cm` (centimeter).


```F#
[<Measure>] type cm
```

The following line defines the measure `ml` (milliliter) as a cubic centimeter (`cm^3`).

```F#
[<Measure>] type ml = cm^3
```

The following code example illustrates how to convert **from a dimensionless floating point number to a dimensioned floating point value**. You just multiply by 1.0, applying the dimensions to the 1.0. You can abstract this into a function like `degreesFahrenheit`.

Also, when you pass dimensioned values to functions that expect dimensionless floating point numbers, you must cancel out the units or cast to `float` by using the `float` operator. In this example, you divide by `1.0<degC>` for the arguments to `printf` because `printf` expects dimensionless quantities.

```F#
// U+00B0 ° 度数符号（例如 30°）  
// U+2103 ℃ 摄氏度符号（如 30℃）  
// U+2109 ℉ 华氏度符号（如 86℉）  
  
// [<Measure>] 是 F# 中用于定义“计量单位”的特性
// 把物理单位（如摄氏度、华氏度、米、千克等）和数值绑定在一起，可以提高类型安全
  
[<Measure>]  
type C // 定义一个“单位”：C 表示摄氏度（Celsius/Centigrade）  
  
[<Measure>]  
type F // 定义另一个“单位”：F 表示华氏度（Fahrenheit）  
  
// FtoC 函数：把带单位的华氏温度 float<F> 转换为摄氏温度 float<C>let FtoC (temp: float<F>) : float<C> =  
    // 华氏转摄氏公式： (F - 32) × 5/9    // 注意：我们使用 32.0<F> 表示数值 32，单位是华氏度  
    // 1.0<C / F> 是转换结果的单位：从 F 到 C    5.0 / 9.0 * (temp - 32.0<F>) * 1.0<C / F>  
  
// toF 函数：将一个普通的 float 数值转为带单位的 float<F>let toF (temp: float) : float<F> = temp * 1.0<F>  
  
// 示例变量 x 是一个普通浮点数，代表华氏温度 100°Flet x = 100.0  
  
// 把 x 转为 float<F> 单位 → 调用 FtoC 转为摄氏度 → 除以 1.0<C> 去掉单位用于显示  
printfn "%.2f°F = %.2f°C" x (FtoC(toF x) / 1.0<C>)
```

The following example session shows the outputs from and inputs to this code.

```Bash
Enter a temperature in degrees Fahrenheit.
90
That temperature in degrees Celsius is    32.22.
```
