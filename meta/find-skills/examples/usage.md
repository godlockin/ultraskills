# find-skills 使用示例

## 搜索模式

### 基本用法

```bash
# 在项目根目录运行
cd /Users/chenchen/working/sourcecode/tools/ultraskils

# 搜索视频相关技能
python meta/find-skills/scripts/search.py 视频
```

输出示例：

```
找到 4 个匹配的 Skills:

============================================================

#1 [10分] 剪辑
   描述: 执行视频剪辑。根据确认的删除任务执行FFmpeg剪辑，循环直到零口...
   标签: video, editing, ffmpeg
   路径: ./video/剪辑/SKILL.md

#2 [6分] 视频帧提取
   描述: Extracts image frames from video files. Uses FFmpeg to extract...
   标签: video, extraction, ffmpeg
   路径: ./tools/video-frame-extractor/SKILL.md
...
```

### 搜索不同类型的 Skills

```bash
# 搜索 Git 相关
python meta/find-skills/scripts/search.py git

# 搜索文档处理
python meta/find-skills/scripts/search.py 文档

# 搜索测试相关
python meta/find-skills/scripts/search.py 测试
```

## 生成模式

### 基本用法

```bash
# 生成一个新的 Skill
python meta/find-skills/scripts/generate.py "视频压缩"

# 指定输出目录
python meta/find-skills/scripts/generate.py "图片处理" ./custom-skills
```

输出示例：

```
✅ Skill 已生成: ./video-compression

📋 下一步:
1. 查看并完善 SKILL.md
2. 实现 scripts/main.py 中的实际逻辑
3. 完善 examples/basic-usage.md 示例
```

### 生成的文件结构

```
video-compression/
├── SKILL.md              # Skill 定义
├── scripts/
│   └── main.py           # 入口脚本占位
└── examples/
    └── basic-usage.md    # 使用示例占位
```

## 在 Claude Code 中使用

### 触发方式

直接调用 Skill：

```
/find-skills
```

或自然语言：

```
"帮我找一个处理视频的 skill"
"我需要一个做 X 的 skill"
"找不到合适的 skill，帮我创建一个"
```

### 工作流程

1. **输入任务描述** - 描述你想要完成的任务
2. **搜索结果** - 查看匹配的 Skills
3. **选择操作**：
   - 使用某个匹配的 Skill
   - 或选择「生成新 Skill」
4. **生成后** - 完善自动生成的 SKILL.md

## 评分算法

```
得分 = name完全匹配(10) + name包含(5) + description包含(3) + tags匹配(2/个)

例如：搜索"视频"
- name="视频剪辑" 包含 "视频" → 5分
- description 包含 "视频" → 3分
- tags=["video","media"] 包含 "视频" → 4分 (2×2)
- 总分：12分
```

## 注意事项

1. 确保在项目根目录运行脚本（需要读取 index.json）
2. 生成的 Skill 是基础脚手架，需要人工完善
3. 搜索是关键词匹配，描述越具体匹配越准确