---
title: 会写TypeScript就能理解日语语法——Typed Japanese项目能做到（吗？）
date: '2025-04-16'
tags:
- 命令
- Go
- 代码
- 函数
- 参数
- main
- 语法
- 类型
- 字符
- 字符串
- 计算机
- HTTP
- HTTPS
- IP
- GitHub
- 开源
- nc
- AI
- 模型
- Git
- 构建
- 开发
- 程序员
---

# 会写TypeScript就能理解日语语法——Typed Japanese项目能做到（吗？）

近日，Yifeng Wang 和 Satoshi Terasaki 发布了名为 **Typed Japanese** 的开源项目。该项目旨在**借助 TypeScript 的类型系统帮助程序员学习日语**。会写 TypeScript 就能理解日语语法——**自然语言的语法规则完全可以映射到 TypeScript 的类型系统**之中。

> **If you can write TypeScript, you can understand Japanese!**
> https://github.com/typedgrammar/typed-japanese/

**Typed Japanese** 提供了一个基于 TypeScript 类型系统的库（type-level library），将日语语法规则编码为 DSL（领域特定语言），使**开发者能够用 TypeScript 编写并标注日语句子，并借助类型检查器验证语法是否正确**。

接下来，我们将从**日语动词的活用形**和**如何描述日语句子**两个方面介绍这个项目的核心。

## 日语动词的活用形

我们先通过下面这一小段代码，看看 Typed Japanese 如何使用 DSL 来描述动词的活用形。

```ts
// https://github.com/typedgrammar/typed-japanese/blob/main/blog.md#implementing-japanese-verb-conjugation-with-type-programming

// Define simplified Japanese verb types
type SimpleJapaneseVerb = {
  type: "godan" | "ichidan";
  stem: string;
  ending: string;
};

// Define conjugation forms
type JapaneseVerbForm = "辞書形" | "て形" | "た形";
```

代码中首先定义了一个简化版的日语动词结构 `SimpleJapaneseVerb`。动词由种类 `type`（五段或一段）、词干 `stem` 和词尾（送假名）`ending` 构成。然后定义了 3 种活用形，`辞書形`、`て形`、和 `た形`。

感觉这里应该是受某些日语教材的影响，仅仅因为接续不同（是接续“助詞て”还是“助動詞た”），这里就把（音便）连用形拆分成了两种形态。不知道在接续“たら”时，会不会又独立于“た形”，出现一个“たら形”。

接下来的代码就比较有意思了，

```ts
// Simplified Japanese verb conjugation
type ConjugateSimpleJapaneseVerb<
  V extends SimpleJapaneseVerb,
  Form extends JapaneseVerbForm
> = Form extends "辞書形"
  ? `${V["stem"]}${V["ending"]}`
  : Form extends "て形"
  ? V["type"] extends "godan"
    ? V["ending"] extends "う"
      ? `${V["stem"]}って`
      : V["ending"] extends "く"
      ? `${V["stem"]}いて`
      : `${V["stem"]}${V["ending"]}`
    : V["type"] extends "ichidan"
    ? `${V["stem"]}て`
    : `${V["stem"]}${V["ending"]}`
  : Form extends "た形"
  ? V["type"] extends "godan"
    ? V["ending"] extends "う"
      ? `${V["stem"]}った`
      : V["ending"] extends "く"
      ? `${V["stem"]}いた`
      : `${V["stem"]}${V["ending"]}`
    : V["type"] extends "ichidan"
    ? `${V["stem"]}た`
    : `${V["stem"]}${V["ending"]}`
  : `${V["stem"]}${V["ending"]}`;

// Examples
type KauVerb = { type: "godan"; stem: "買"; ending: "う" };
type KauTeForm = ConjugateSimpleJapaneseVerb<KauVerb, "て形">; // "買って"
type KauTaForm = ConjugateSimpleJapaneseVerb<KauVerb, "た形">; // "買った"
```

`ConjugateSimpleJapaneseVerb` 是一个**泛型类型别名（generic type alias）**，其中的 `V` 表示一个动词，类型为刚刚定义的 `SimpleJapaneseVerb`；之后的 `Form` 是动词活用形。

接下来是一大片类似三元表达式（`a ? b : c`）的**条件类型（conditional types）**，

```ts
Form extends "辞書形"
  ? ...
  : Form extends "て形"
  ? ...
  : Form extends "た形"
  ? ...
  : ...
```

TypeScript 能够根据 `Form` 的字面量类型值（如 "て形"）来选择对应的分支逻辑，从而生成不同的结果类型。结果类型又是 TypeScript 的特性之一**模板字面量类型（template literal types）**，其作用是在类型层拼接字符串，从而生成新的类型。

例如，`type KauTeForm = ConjugateSimpleJapaneseVerb<KauVerb, "て形">` 就得到了一个新类型 `"買って"`。

由于 `"買って"` 是个类型，而不是值为 `"買って"` 的字符串，所以：

```ts
// const kau: KauTeForm = "買って" // ✅ OK
const kau: KauTeForm = "買うて" // ❌ Type '"買うて"' is not assignable to type '"買って"'.
```

也就是说，`type KauTeForm = "買って"` 现在是一个类型，因此，`KauTeForm` 类型的变量 `kau` **只能被赋与字符串 `"買って"`**。 

如果日语初学者不小心写成了 `"買うて"`，那么因为类型不匹配，会触发类型错误：`Type '"買うて"' is not assignable to type '"買って"'`。

需要注意的是，`KauTeForm` 只是类型层级上的操作，因此在运行时并不会自动生成 `"買って"` 这个值。 如果在实际中需要使用这个值，还需要通过其他方式显式地处理。

类似地，

```ts
type IkuVerb = { type: "godan"; stem: "行"; ending: "く" };
type IkuTeForm = ConjugateSimpleJapaneseVerb<IkuVerb, "て形">;
// const iku: IkuTeForm = "行いて" // ✅ OK
const iku: IkuTeForm = "行って"    // ❌ Type '"行って"' is not assignable to type '"行いて"'.
```

由此可见，如果没有把 `extends ? ... : ...` 这样的条件类型判断写得足够完善，“行く”的“て形”就可能会被错误地推导为“行いて”，这反而会误导日语初学者。

稍微总结一下，相较于我们熟悉的函数定义、调用，如 `function ConjugateVerb(verb, form)`，这里主要发生了 4 点转变：

1. 函数参数 → 泛型参数
2. `if / else` 条件语句 → 条件类型
3. 字符串拼接 → 模板字面量类型
4. 函数调用 → 类型声明或实例化

这 4 点汇成一句话就是：经过这样的类型处理后，**各个动词的各种活用形**并不是普通的 `string` 类型的值，而**是一个在 TypeScript 类型系统内部唯一的模板字面量类型**。

下面再来看看如何基于这 4 点定义一个日文的句子。

## 从“一词一型”到“一句一型”

我们以魔数 114514 所代表的句子”いいよ、来いよ“为例，简单看一看如何基于 TypeScript 的类型系统，描述并标注日语中的句子。

可以先定义如下的**单句类型** `PhraseWithParticle`，以及用于连接多个句子的**复句类型** `ConnectedPhrases`：

```ts
// https://github.com/typedgrammar/typed-japanese/blob/main/blog.md#compound-sentence-type-gymnastics-good-times-come-on 

// Phrase with particle
type PhraseWithParticle<
  Phrase extends string,
  P extends Particle
> = `${Phrase}${P}`;

// Phrases connected by Japanese comma
type ConnectedPhrases<P1 extends string, P2 extends string> = `${P1}、${P2}`;
```

然后定义形容词”いい“和动词”来る“对应的类型：

```ts
// Define the i-adjective "いい" (good), note that it has irregular conjugation
type いい = IAdjective & { stem: "い"; ending: "い"; irregular: true };
type いいよ = PhraseWithParticle<ConjugateAdjective<いい, "基本形">, "よ">;

// Define the irregular verb "来る" (to come)
type 来る = IrregularVerb & { dictionary: "来る" };
type 来いよ = PhraseWithParticle<ConjugateVerb<来る, "命令形">, "よ">;
```

通过这样的方式，我们就可以利用 TypeScript 的类型系统，来表达由多个独立单句构成的复句结构：

```ts
// Connect the two short sentences -> "いいよ、来いよ"
type いいよ来いよ = ConnectedPhrases<いいよ, 来いよ>;
```

话说，第一个よ难道不是名词「世」吗？第二个よ才是终助词（`Particle`）吧。

---

Typed Japanese 完全是基于 TypeScript 的类型系统构建的，利用**泛型参数 generic type alias + 条件类型 conditional types + 模板字面量类型 template literal types**，描述了日语语法，并将计算机语言的类型检查器用作了自然语言的语法检查器。

尽管存在“行いて”这样的错误，但 Typed Japanese 不仅展现了类型系统的强大表达力，也为 AI 辅助语言学习提供了新的思路——一种全新的中间表示格式，让大语言模型在生成日语语法分析结果时，用类型系统而非 JSON 描述语言结构，从而实现更严谨的语法验证。

在日本茶道宗师千利休的美学思想中，「一期一会」意指：每一次相遇都只有一次，每一次茶会都是独一无二的存在。

同样地，在 TypeScript 类型编程的世界里，我们逐渐从“一词一型”（每个词的每种形态都是独立的类型），走向更高层次的“一句一型”。

🔚

![](img1.png)
