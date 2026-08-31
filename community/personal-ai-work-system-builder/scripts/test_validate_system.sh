#!/usr/bin/env bash
# 回归测试: validate_system.py 必须放过 1 个合规项目、挡住 5 类攻击项目
#
# Usage:
#   bash scripts/test_validate_system.sh
#
# 测试项目在临时目录里现场生成,不依赖任何外部状态,可在任意机器上重放。

set -uo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VALIDATE="python3 $SKILL_DIR/scripts/validate_system.py $SKILL_DIR --check-done"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

PASSED=0
FAILED=0
TODAY="$(date +%Y-%m-%d)"

check() {
  local proj="$1" expect="$2" label="$3"
  $VALIDATE "$proj" > "$WORK/out.txt" 2>&1
  local rc=$?
  local actual="FAIL"
  [ $rc -eq 0 ] && actual="PASS"
  if [ "$actual" = "$expect" ]; then
    echo "OK    $label — 期望 $expect, 实际 $actual"
    PASSED=$((PASSED + 1))
  else
    echo "BAD   $label — 期望 $expect, 实际 $actual"
    sed 's/^/        /' "$WORK/out.txt" | head -n 15
    FAILED=$((FAILED + 1))
  fi
}

stub_all() {
  local d="$1"
  mkdir -p "$d"
  for f in "00_项目说明与目标.md" "01_权威资料与数据口径.md" "02_SOP与判断规则.md" \
           "03_话术、模板与Skill.md" "04_执行记录与案例.md" "05_复盘、指标与迭代版本.md" \
           "SYSTEM-BLUEPRINT.md" "SYSTEM-STATE.md" "ASSET-REGISTRY.md" \
           "AUTOMATION-REGISTRY.md" "STEP-COMPRESSION.md"; do
    printf '# %s\n\n(empty)\n' "$f" > "$d/$f"
  done
}

# ================================================================ 正例

GOOD="$WORK/good"
stub_all "$GOOD"

cat > "$GOOD/00_项目说明与目标.md" <<EOF
# 项目说明与目标

- 项目名称：客户运营与转化
- 服务角色：B2B 销售经理（管理 30 个活跃客户）
- 核心结果：周会跟进看板一键就绪，续约不漏

## 统一入口
- 入口位置：Claude Chat
- 触发方式：每周日 20:00 cron 自动触发
- 示例指令：\`生成本周客户跟进看板\`

## 访谈基线（第一轮 6 问）
| 问题 | 回答 |
|---|---|
| 岗位与角色 | B2B 销售经理，企业 SaaS |
| 30 天目标 | 周会看板自动化 / 续约提醒不漏 / 报价单自动填充 |
| 高频任务 | 周会汇总、报价单、续约提醒、合同初稿、业绩统计 |
| 流程路径 | 企微对话 → 手工整理 → 飞书表格 → 周会汇报 |
| 系统分布 | 企业微信、飞书多维表格、邮箱 |
| 第一条闭环 | 周会跟进看板自动生成（基线 90min） |
EOF

cat > "$GOOD/01_权威资料与数据口径.md" <<EOF
# 权威资料与数据口径

本项目所有指标以飞书多维表格为唯一权威来源，口径变更需记版本与生效日期。

| 数据项 | 权威来源 | 主责 | 人工确认 | 输出 | 数据级别 |
|---|---|---|---|---|---|
| 客户跟进状态 | 飞书多维表格 | Claude 主控 | 状态异常时人工复核 | 飞书表格 + 群摘要 | L1 内部 |
EOF

cat > "$GOOD/02_SOP与判断规则.md" <<EOF
# SOP 与判断规则

## SOP：周会跟进汇总
1. 导出本周企微对话（先经境内脱敏，客户名转 ID）
2. 解析客户状态关键词（签约/续约/异议/待跟进）
3. 合并飞书表格现状，标记状态变化
4. 生成聚合摘要
5. 人工复核异常项后推送到内部群

## 判断规则
- 连续 3 周无更新的客户标记为需人工介入
- 状态冲突时以飞书表格为准
EOF

cat > "$GOOD/03_话术、模板与Skill.md" <<EOF
# 话术、模板与 Skill

| 资产 | 路径 | 版本 |
|---|---|---|
| 周报摘要模板 | templates/weekly-summary.md | v2 |
| 客户跟进话术 | templates/followup.md | v1 |
| 报价单模板 | templates/quote.md | v3 |

所有模板变更需在 ASSET-REGISTRY 登记版本与替代关系。
EOF

cat > "$GOOD/04_执行记录与案例.md" <<EOF
# 执行记录与案例

每次真实运行记一行，四要素（输入版本/输出位置/耗时/异常）缺一不算有效记录。

| 日期 | 流程 | 输入版本 | 输出位置 | 结果 | 耗时 | 异常 | 修正 |
|---|---|---|---|---|---|---|---|
| $TODAY | 周会跟进汇总 | 企微导出 w35 | 飞书表格 + 群消息 | 通过 | 4min | 无 | 无 |
EOF

cat > "$GOOD/05_复盘、指标与迭代版本.md" <<EOF
# 复盘、指标与迭代版本

## 月度复盘

| 指标 | 基线 | 当前 | 目标 | 验证日期 |
|---|---|---|---|---|
| 周会汇总耗时 | 90min | 4min | 5min | $TODAY |
| 漏跟进次数 | 3次 | 0次 | 0次 | $TODAY |

## 有效修正（已写回 SOP）
| 修正 | 出现次数 | 写回位置 |
|---|---|---|
| 企微导出需过滤系统消息 | 2次 | 02_SOP与判断规则.md |

## 迭代版本
- v2（${TODAY}）：接通自动解析 + 摘要推送
- v1：仅飞书表格模板 + 手工填充
EOF

cat > "$GOOD/SYSTEM-BLUEPRINT.md" <<EOF
# 系统蓝图

## 系统定位
- 服务角色：B2B 销售经理
- 当前成熟度 / 目标成熟度：当前 L2（有模板但手动搬运）；30 天目标 L4
- 第一条闭环：周会跟进看板自动生成
- 下一条待接通流程：客户异议库自动归类

## 统一入口
- 入口位置：Claude Chat
- 触发方式：每周日 20:00 cron
- 示例指令：\`生成本周客户跟进看板\`

## 凭证引用
严禁写入明文密钥，只写变量名与存放位置。

| 系统 | 认证方式 | 凭证变量名 | 存放位置 |
|---|---|---|---|
| 企业微信 | corp_secret | \${WECOM_SECRET} | .env（已 gitignore） |
EOF

cat > "$GOOD/SYSTEM-STATE.md" <<EOF
# 运行状态

本文件只记录已经验证的真实状态；计划不等于完成。

**最后验证**: $TODAY
**下一条待接通流程**: 客户异议库自动归类

| 模块/流程 | 状态 | 当前能力 | 阻塞 | 下一步 | 最后验证 |
|---|---|---|---|---|---|
| 企微对话导出 | 已连接只读 | 可导出本周 CSV | 无 | 接自动解析 | $TODAY |
| 飞书表格写入 | 已连接可执行 | 可写入跟进状态 | 无 | 保持 | $TODAY |
EOF

cat > "$GOOD/ASSET-REGISTRY.md" <<EOF
# 资产登记

每条资产必须有权威入口、版本、维护人、生命周期状态、数据级别。

| 项目 | 资产名称 | 类型 | 权威入口 | 版本/日期 | 维护人 | 生命周期状态 | 数据级别 |
|---|---|---|---|---|---|---|---|
| 客户运营 | 周会汇总 SOP | SOP | 飞书文档 | v2 / $TODAY | 张三 | active | L1 内部 |
EOF

cat > "$GOOD/AUTOMATION-REGISTRY.md" <<EOF
# 自动化登记

状态必须是 手动/AI辅助/半自动/全自动/规划中 之一。

| 自动化 | 触发方式 | 数据源 | 数据级别 | AI/执行器 | 人审点 | 写回位置 | 状态 | 最后测试 | 推荐分 | 负责人 | 可回滚 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 周会跟进汇总 | 每周日 cron | 企微导出 | L1 内部 | Claude 主控 | 摘要异常时人工复核 | 飞书表格 | 半自动 | $TODAY | 19 | 张三 | 是 |

## 异常与停止条件
| 自动化 | 停止条件 | 恢复方式 | 负责人 | 已测试异常路径 |
|---|---|---|---|---|
| 周会跟进汇总 | API 失败 / 数据为空 | 人工触发重跑 | 张三 | 是（${TODAY}） |
EOF

cat > "$GOOD/STEP-COMPRESSION.md" <<EOF
# 步骤压缩图

压缩率 = (原人工步骤 - 新人工步骤) / 原人工步骤。低于 30% 属微优化。

| 流程 | 现状人工步骤 | 目标人工步骤 | 步骤去向 | 验证指标 | 验证日期 |
|---|---|---|---|---|---|
| 周会跟进汇总 | 6 | 1 | 5 步自动（导出→解析→填表→摘要→推送） | 耗时 90min → 4min | $TODAY |
EOF

check "$GOOD" PASS "正例: 合规项目"

# ================================================================ 攻击 1
# 空档案 + 明文密钥 + 过期「全自动」

A1="$WORK/attack1"
stub_all "$A1"
cat > "$A1/SYSTEM-BLUEPRINT.md" <<'EOF'
# SYSTEM-BLUEPRINT
- 入口位置：Claude Chat
- 触发方式：手动
- 示例指令：`生成看板`
- 下一条待接通流程：异议归类

| 系统 | 认证方式 | 凭证 | 存放 |
|---|---|---|---|
| 企微 | secret | api_key = sk-proj-abc123def456ghi789jkl | 直接写这里 |
EOF
cat > "$A1/AUTOMATION-REGISTRY.md" <<'EOF'
# AUTOMATION-REGISTRY
| 自动化 | 触发 | 数据源 | AI | 人审点 | 状态 | 最后测试 |
|---|---|---|---|---|---|---|
| 周报生成 | cron | 企微 | Claude | 异常人工 | 全自动 | 2020-01-15 |
EOF
check "$A1" FAIL "攻击1: 空档案 + 明文密钥 + 过期全自动"

# ================================================================ 攻击 2
# 最小合法垃圾:否定句含四字段 / 单字符值 / 0min / 5→5 零压缩

A2="$WORK/attack2"
stub_all "$A2"
printf '# x\n没有梳理权威来源,没有确定主责,没有人工确认环节,也没有定义输出。\n' \
  > "$A2/01_权威资料与数据口径.md"
printf '# x\n输入 输出 耗时 异常\n2026-08-30\n' > "$A2/04_执行记录与案例.md"
printf '# x\n| a | b |\n|---|---|\n| x | y |\n' > "$A2/ASSET-REGISTRY.md"
printf '# x\n| a | b | c | d |\n|---|---|---|---|\n| zzz | 5 | 5 | 0min |\n' \
  > "$A2/STEP-COMPRESSION.md"
printf '# x\n- 入口位置：X\n- 示例指令：x\n- 下一条待接通流程：x\n' \
  > "$A2/SYSTEM-BLUEPRINT.md"
check "$A2" FAIL "攻击2: 最小合法垃圾（否定句 + 单字符 + 0min + 5→5）"

# ================================================================ 攻击 3
# 装饰字符逃逸状态枚举 + 高风险动作无人审

A3="$WORK/attack3"
stub_all "$A3"
cat > "$A3/AUTOMATION-REGISTRY.md" <<'EOF'
# AUTOMATION-REGISTRY
| 自动化 | 触发 | 数据源 | AI | 人审点 | 状态 | 最后测试 |
|---|---|---|---|---|---|---|
| 日报 | cron | 神策 | Claude | 异常人工 | 手动 | 2026-08-30 |
| 客户退款处理 | webhook | 订单 | Claude | 无 | 全自动 ✅ | 2020-01-01 |
EOF
check "$A3" FAIL "攻击3: 装饰状态「全自动 ✅」逃逸枚举 + 高风险无人审"

# ================================================================ 攻击 4
# 用「例:」前缀把违规行伪装成模板示例

A4="$WORK/attack4"
stub_all "$A4"
cat > "$A4/AUTOMATION-REGISTRY.md" <<'EOF'
# AUTOMATION-REGISTRY
| 自动化 | 触发 | 数据源 | AI | 人审点 | 状态 | 最后测试 |
|---|---|---|---|---|---|---|
| 日报 | cron | 神策 | Claude | 异常人工 | 手动 | 2026-08-30 |
| 例: 客户退款自动处理 | webhook | 订单 | Claude | 无 | 全自动 | 2020-01-01 |
EOF
check "$A4" FAIL "攻击4: 用「例:」前缀隐藏高风险全自动行"

# ================================================================ 攻击 5
# 清空关键档案,试图让严格检查静默跳过

A5="$WORK/attack5"
cp -r "$GOOD" "$A5"
: > "$A5/ASSET-REGISTRY.md"
check "$A5" FAIL "攻击5: 清空 ASSET-REGISTRY 试图免检"

# ================================================================ 汇总

echo "---"
echo "Regression: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] || exit 1
