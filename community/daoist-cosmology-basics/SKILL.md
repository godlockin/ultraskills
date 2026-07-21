---
name: daoist-cosmology-basics
description: 道家命理哲学与术语统一 — 上游 stub。当用户问"五行/天干/地支/阴阳/相生相克/十神/神煞/三庭/五眼/十二宫/命理基础/玄学/子平术"等概念时调用此 skill。其他三个命理 skill(bazi-fortune / face-reading / palm-reading)都以本 skill 为前置知识。
version: 1.0.0
tags: [daoist, cosmology, 五行, 天干, 地支, yin-yang, 五行生克, 子平术, metaphysics, 李虚中, 徐子平, 九紫, 离火]
user-invocable: true
source: xun-taixu-90min-video
source_date: 2026-07-16
derived_from: 荀太虚《面相八字手相全系统教学》视频转写(2026)
disclaimer: 命理为参考框架,不替代医学/法律/职业决策。
---

# 道家命理基础 (Daoist Cosmology Basics)

> 📚 **本 skill 为上游 stub**。其他三个 domain skill (`bazi-fortune` / `face-reading` / `palm-reading`) 在 SKILL.md 顶部会引用本 skill 作为前置知识。
>
> 🎓 **来源**:荀太虚《面相八字手相全系统教学》视频转写(2026)

## 🎯 目标 (Goal)

为三个命理 skill 提供**统一的术语、对照表、哲学背景、历史源流**,避免每个 skill 重复维护相同的概念定义。

## 🧠 核心理念 (Core Concepts)

### 道家"天人合一"基础
- 自然界规律与人事规律同构
- 五行体现于天文、地理、人体、社会
- 阴阳消长是普遍规律

### 视频中的核心金句
- "我的命运取决于**我和客观世界的关系**"
- "古人是怎么理解我和世界的关系呢?用**十神**来总结就是**财官印食比**"
- 八字本质:**不是决定命运的魔咒,而是理解自己剧本的剧本**

## 🏛️ 历史源流

### 李虚中(唐朝)

视频原文:"命理祖师爷之一的**李虚中**,他所生活的唐朝,人口最巅峰的时候也不过**九千万**。如此一来,古人发明的这套以出生时间为依据的推命模型,还是比较扎实的。"

- **朝代**: 唐朝
- **贡献**: 创**三柱论命法**(年、月、日,**无时柱**)
- **局限**: 当时时辰不够精确,影响论命准确度

### 徐子平(宋代)

> 视频原文:"后来到了**宋代,徐子平**加以改进,引入时辰,把三柱扩展成**四柱**。后人为了纪念他,将四柱论命称为**子平术**或**子平命学**。"

- **朝代**: 宋代
- **贡献**: 引入**时柱**,创四柱八字完整体系
- **后世称**: 子平术

## 🚀 使用流程 (Workflow)

### Step 1: 命中判断

判断用户问询落在哪个 domain skill:

| 用户关键词 | 推荐使用 |
|---|---|
| 八字、四柱、生辰、排盘、命格 | → `bazi-fortune` |
| 面相、五官、印堂、三庭五眼 | → `face-reading` |
| 手相、掌纹、生命线、智慧线、八丘、手型 | → `palm-reading` |
| 纯哲学 / 历史 / 术语定义 | → 留在本 skill |

### Step 2: 术语输出

按 `resources/` 下的速查表回应术语查询。

### Step 3: 路由回 domain

确认用户问题为"应用层"后,**路由到对应 domain skill**进行实际操作。

## 📚 resources/(已基于转写填写)

| 文件 | 内容 |
|---|---|
| `heavenly-stems.md` | 天干(甲乙丙丁戊己庚辛壬癸)五行 + 阴阳 |
| `earthly-branches.md` | 地支 + 六合 + 藏干 |
| `five-elements.md` | 五行生克 + 比肩十神 |
| `yin-yang-flow.md` | 阴阳能量大小 + 阳克阴 |
| `stem-branch-five-clauses.md` | 天干五合 + 地支六合 |
| `history.md` | 李虚中 → 徐子平 → 子平术源流 |

## ✅ 检查清单 (Checklist)

- [ ] 命中用户问询 → 给出术语定义 / 链接回 domain skill
- [ ] 不在三者之间,纯哲学 → 直接回答
- [ ] 顶部 disclaimer 永远在(无论精简到几行)
- [ ] 引用具体术语时,**附上来源**(视频 vs 经典补充)

## 🔗 关联 Skill

- `bazi-fortune` — 八字/排盘/论命
- `face-reading` — 面相/三庭五眼
- `palm-reading` — 手相/手型/五指
