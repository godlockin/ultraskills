# AB 正逆双轴 Review 方法论 — 从 PWSB 实践中提炼

> 来源:2026-08-30 对 `personal-ai-work-system-builder` 的两轮 10 专家 AB review 实践。
> 本文记录**可复用的方法论**,不是那次 review 的结果。

---

## 一、核心发现:文档层修复 ≠ 真修复

第一轮 review 提出 12 个 P0,我全部"修复"并声称完成。第二轮复验用**实际执行**验证时,发现:

| 修复方式 | 第二轮复验结论 |
|---|---|
| 在 SKILL.md 加"必须先做 X"的文字 | `partial` — prompt 层约束,无执行级强制 |
| 在 references 新建规则文档 | `partial` — 规则存在,但**案例文件没跟着改,自相矛盾** |
| 给校验脚本加检查逻辑 | 5 个绕过手法**实测全部通过** |

**教训 1**:声称修复后必须**自己写攻击用例去打**。不写攻击用例的"修复"约等于没修。

**教训 2**:改了规则层,必须**同步检查所有引用该规则的地方**(案例、模板、示例)。规则与案例矛盾时,读者会照抄案例。

---

## 二、校验脚本的 5 类经典绕过(全部实测复现)

这 5 类适用于任何"用脚本校验产出质量"的场景:

### 1. 空文件绕过

```python
# ❌ 有漏洞:文件为空时整段检查被跳过
text = read(path)
if text:
    check_fields(text)   # 空文件 → 永不执行 → PASS

# ✅ 修复:先判非空,空即报错
if not text.strip():
    errors.append(f"{path} 为空")
else:
    check_fields(text)
```

**为什么危险**:清空文件比填对内容容易得多,而结果是"通过"。

### 2. 子串存在性绕过

```python
# ❌ 有漏洞:只要字段名出现在文件任意位置
for field in ("权威来源", "主责", "人工确认", "输出"):
    if field not in text:
        errors.append(...)
```

实测攻击:写「**没有**梳理权威来源,**没有**确定主责,**没有**人工确认环节,也**没有**定义输出」→ PASS。
否定句里也包含这四个词。

```python
# ✅ 修复:要求字段有非空值
m = re.search(rf"{field}\s*[：:]\s*([^\n|]*)", text)
if not m or is_empty(m.group(1)):
    errors.append(...)
# 或:解析表格,要求某行的这几列同时非空
```

### 3. 装饰字符逃逸枚举

```python
# ❌ 有漏洞:精确相等匹配
states = [c for c in cells if c in VALID_STATES]
if not states:
    continue   # ← 不匹配就跳过整行,连带跳过所有严格检查
```

实测攻击:写「全自动 ✅」→ 不在枚举内 → 整行 `continue` → 逃过日期新鲜度检查和高风险动作检查。

```python
# ✅ 修复:归一化后匹配 + 不匹配要报错而非跳过
def normalize(s):
    return re.sub(r"[^一-鿿A-Za-z0-9]", "", s)

state = match_state(cells, VALID_STATES)   # 容忍装饰字符
if state is None:
    errors.append(f"状态不在枚举内: {cells}")   # 报错,不是 continue
```

**关键**:`continue` 是最危险的分支 —— 它让"格式不对"变成"免检"。

### 4. 示例前缀隐身

```python
# ❌ 有漏洞:过滤含"例:"的行(本意是跳过模板示例)
if "例:" in joined:
    continue
```

实测攻击:把真实的违规行写成「例: 客户退款自动处理 | 全自动 | 人审=无」→ 被当模板示例跳过。
**过滤器变成了主动隐藏通道。**

```python
# ✅ 修复三件套
# (a) 只在行首匹配,不是任意位置
if cells[0].lstrip().startswith(("例:", "例：", "示例:")):
    filtered.append(cells)   # (b) 记录被过滤的行
    continue

# (c) 检查被过滤的行里有没有真实内容
for cells in filtered:
    if match_state(cells, VALID_STATES) or has_high_risk(cells):
        errors.append("疑似用示例前缀规避校验")
```

### 5. 最小合法垃圾

实测攻击:11 个文件共 ~200 字节垃圾(`| a | b |`、`5min`、单字符字段值)→ 全绿 PASS。

```python
# ✅ 修复:多道量化门槛
MIN_ARCHIVE_CHARS = 80          # 每份档案最小实质内容
min_cols = 4                     # 表格行最小列数
min_filled_ratio = 0.6           # 非空单元格占比
METRIC_RE = r"[1-9]\d*\s*(min|%|次)"   # 排除 0 值
# 并计算业务语义:压缩率 = (before-after)/before,≤0 直接报错
```

---

## 三、有效的 review harness 设计

### 双轴分离(借自 Matt Pocock two-axis code review)

**A 组正向**:找优势 + 按标准找改进
**B 组逆向**:攻击视角 + 找绕过

**关键约束:两轴的 verdict 独立给,不合并 finding。**
理由:一个产物可以"符合所有规范但实现错了"(A pass / B fail),也可以"实现对了但破坏惯例"(B pass / A fail)。合并会让一轴掩盖另一轴。

### 专家组按领域定制,不用通用模板

对 PWSB 这个"个人 AI 工作系统"skill,B 组配的是:
- 安全/滥用(prompt injection、数据外泄、权限放大)
- 流程陷阱(AI 会怎么跳过这个 skill)
- 独立审计(完成标准逐条可验证性)
- 合规/伦理(PIPL 跨境、consent、财务双签)
- 决策门(何时不该用)

**换个领域就要换专家**。给视频生成 skill 配"PIPL 合规"专家是浪费;给财务分析 skill 配"版权风险"专家也是错配。
选专家的依据是**这个 skill 具体会怎么出错**。

### 第二轮必须是"复验"而非"重审"

第二轮的 prompt 要把第一轮的每条 finding 列出来,要求:

```json
{
  "round1_verification": [{
    "scenario": "第一轮的问题",
    "fix_claimed": "声称的修复",
    "actually_fixed": true | false | "partial",   // ← 关键
    "evidence": "文件:行 或 实际执行输出",         // ← 必须是证据
    "residual_gap": "仍存在的风险"
  }]
}
```

并明确写:**"`actually_fixed` 必须基于实际证据,不接受'文档里写了就算修了'。只有 prompt 文字无执行级拦截的标 `partial`。"**

这一条改动让第二轮从"又提一堆新建议"变成"验证上轮是否真有效"。

### 要求 agent 自己构造攻击用例

第二轮里最有价值的产出来自这句 prompt:

> "另外,尝试设计 3 个新的绕过手法(第一轮没想到的),看现有防护能否拦住。"

以及:

> "`_table_rows()` 会过滤含'例:'的行 —— AI 能不能故意用'例:'前缀让自己的假数据被跳过?"

**给出攻击方向的提示,agent 会真的去构造并实测。** 5 个 P0 绕过中有 3 个来自这类提示。

---

## 四、回归测试是收尾的必要条件

修完后建一个"1 正例 + N 攻击例"的回归脚本,每次改动都跑:

```bash
check /tmp/good-project   PASS "正例: 合规项目"
check /tmp/attack-1       FAIL "空档案+密钥+过期状态"
check /tmp/attack-2       FAIL "最小合法垃圾"
check /tmp/attack-3       FAIL "关键词填空"
check /tmp/attack-4       FAIL "装饰状态逃逸"
check /tmp/attack-5       FAIL "例:前缀隐身"
```

**收紧校验时会产生假阳性**,回归里的正例就是防线。实际发生过两次:
1. `_looks_like_state` 把「接自动解析」误判为状态值 → 收紧相似度判定
2. 多表格文件里第二个表的表头被当数据行 → 重写表头识别(用分隔行确认)

没有正例回归,这两个假阳性会被当成"更严格了"而漏掉。

---

## 五、可直接复用的清单

做任何"AI 产出质量校验"时:

- [ ] 每个 `if text:` 都问一遍"空值时会怎样" —— 空值必须报错,不是跳过
- [ ] 每个 `continue` 都问一遍"这会不会让不合规内容免检"
- [ ] 每个子串检查都问一遍"否定句能不能通过"
- [ ] 每个枚举匹配都问一遍"加个 emoji 还匹配吗"
- [ ] 每个过滤器都问一遍"能不能被用来主动隐藏"
- [ ] 每个数值检查都问一遍"0 能不能通过"
- [ ] 有量化语义的(压缩率/通过率)必须真算,不只查"有数字"
- [ ] 日期新鲜度必须取**字段同行**的日期,不能取全文最大值
- [ ] 建 1 正例 + N 攻击例的回归脚本,每次改动都跑
- [ ] 改规则层后,grep 所有引用处(案例/模板/示例)同步更新

---

## 六、方法论本身的局限(诚实记录)

1. **prompt 层门控无法强制**。SKILL.md 里写"必须先做 X"只是建议,没有 hook 就没有强制。真正的强制需要 Stop hook / PreToolUse hook,这超出单个 skill 文件的能力范围。
2. **校验脚本是可选的**。用户或 AI 可以不跑。缓解办法:要求把校验输出原文粘进档案作为证据。
3. **语义质量无法机械验证**。脚本能查"有 ≥80 字符、有非零指标、字段非空",但查不出"这个 SOP 写得对不对"。这仍需人或 LLM 判断。
4. **专家组是同一个模型扮演的**。视角多样性来自 prompt 差异,不是真正的独立判断。对抗性验证能减少但不能消除共同盲点。
