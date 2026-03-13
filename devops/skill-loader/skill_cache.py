#!/usr/bin/env python3
"""
Skill Cache Module - 高效的 Skills 索引缓存系统

功能:
1. 预构建索引并持久化到本地缓存
2. 使用 file watcher 监听文件变化
3. 增量更新索引（只扫描变化的文件）
4. 支持内存缓存 + 磁盘缓存双层结构

性能目标:
- 首次加载：O(N) 扫描全量
- 增量更新：O(1) 只处理变化
- 查询响应：<10ms
"""

import json
import hashlib
import os
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent, FileDeletedEvent, DirDeletedEvent
import threading
import yaml

# 缓存配置
CACHE_DIR = Path(__file__).parent / ".cache"
INDEX_CACHE_FILE = CACHE_DIR / "skill_index.json"
METADATA_FILE = CACHE_DIR / "metadata.json"
CACHE_TTL_SECONDS = 300  # 5 分钟自动过期

# 扫描路径配置
DEFAULT_SKILL_PATHS = [
    "engineering",
    "productivity",
    "devops",
    "creative",
    "community",
]


@dataclass
class SkillMetadata:
    """Skill 元数据结构"""
    id: str
    name: str
    path: str
    description: str
    tags: List[str]
    file_hash: str
    file_mtime: float
    content_length: int
    section_count: int
    last_scanned: str


@dataclass
class CacheMetadata:
    """缓存元数据"""
    version: str = "1.0.0"
    created_at: str = ""
    updated_at: str = ""
    total_skills: int = 0
    file_hashes: Dict[str, str] = None

    def __post_init__(self):
        if self.file_hashes is None:
            self.file_hashes = {}


def compute_file_hash(file_path: Path) -> str:
    """计算文件的 SHA256 hash"""
    if not file_path.exists():
        return ""

    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        # 分块读取以支持大文件
        for chunk in iter(lambda: f.read(8192), b''):
            hasher.update(chunk)
    return hasher.hexdigest()


def parse_frontmatter(content: str) -> Optional[Dict]:
    """解析 YAML frontmatter"""
    parts = content.split("---")
    if len(parts) < 3:
        return None
    try:
        return yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return None


def extract_keywords(text: str) -> List[str]:
    """从文本中提取关键词（简化版）"""
    # 分词并去除停用词
    stopwords = {'the', 'a', 'an', 'is', 'are', 'for', 'with', 'to', 'in', 'on', 'at'}
    words = text.lower().split()
    keywords = []
    for word in words:
        # 只保留字母数字组成的词
        clean_word = ''.join(c for c in word if c.isalnum())
        if clean_word and clean_word not in stopwords and len(clean_word) > 2:
            keywords.append(clean_word)
    return keywords[:20]  # 限制最多 20 个关键词


class SkillIndexCache:
    """Skills 索引缓存系统"""

    def __init__(self, project_root: Path, auto_watch: bool = True):
        self.project_root = project_root
        self.cache_dir = CACHE_DIR
        self.index_cache_file = INDEX_CACHE_FILE
        self.metadata_file = METADATA_FILE

        # 内存缓存
        self._index: Dict[str, SkillMetadata] = {}
        self._metadata: CacheMetadata = CacheMetadata()
        self._file_hashes: Dict[str, str] = {}

        # 文件监控
        self._observer: Optional[Observer] = None
        self._event_handler: Optional[SkillFileHandler] = None
        self._lock = threading.RLock()

        # 状态
        self._initialized = False

        # 初始化
        self._ensure_cache_dir()
        self._load_cache()

        if auto_watch:
            self._start_watcher()

    def _ensure_cache_dir(self):
        """确保缓存目录存在"""
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _load_cache(self):
        """从磁盘加载缓存"""
        if self.index_cache_file.exists():
            try:
                with open(self.index_cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                self._index = {
                    k: SkillMetadata(**v)
                    for k, v in data.get('index', {}).items()
                }

                meta = data.get('metadata', {})
                self._metadata = CacheMetadata(
                    version=meta.get('version', '1.0.0'),
                    created_at=meta.get('created_at', ''),
                    updated_at=meta.get('updated_at', ''),
                    total_skills=meta.get('total_skills', 0),
                    file_hashes=meta.get('file_hashes', {})
                )
                self._file_hashes = dict(self._metadata.file_hashes)

            except (json.JSONDecodeError, Exception) as e:
                print(f"⚠️  缓存加载失败，将重建索引：{e}")
                self._index = {}
                self._metadata = CacheMetadata()

        # 检查缓存是否过期
        if self._is_cache_stale():
            print("📡 缓存已过期，需要重建索引")
            self.rebuild_index()

    def _is_cache_stale(self) -> bool:
        """检查缓存是否过期"""
        if not self._metadata.updated_at:
            return True

        try:
            updated = datetime.fromisoformat(self._metadata.updated_at)
            age = (datetime.now() - updated).total_seconds()
            return age > CACHE_TTL_SECONDS
        except (ValueError, TypeError):
            return True

    def _save_cache(self):
        """保存缓存到磁盘"""
        with self._lock:
            data = {
                'index': {k: asdict(v) for k, v in self._index.items()},
                'metadata': {
                    'version': self._metadata.version,
                    'created_at': self._metadata.created_at,
                    'updated_at': self._metadata.updated_at,
                    'total_skills': self._metadata.total_skills,
                    'file_hashes': self._file_hashes
                }
            }

            # 原子写入（先写临时文件再重命名）
            temp_file = self.index_cache_file.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            temp_file.rename(self.index_cache_file)

    def _scan_skill_file(self, skill_md_path: Path) -> Optional[SkillMetadata]:
        """扫描单个技能文件"""
        if not skill_md_path.exists():
            return None

        try:
            content = skill_md_path.read_text(encoding='utf-8')
            frontmatter = parse_frontmatter(content)

            if not frontmatter:
                return None

            # 提取技能 ID（使用目录名）
            skill_id = skill_md_path.parent.name.lower().replace('_', '-').replace(' ', '-')

            # 计算文件 hash 和修改时间
            file_hash = compute_file_hash(skill_md_path)
            file_mtime = skill_md_path.stat().st_mtime

            # 统计章节数量
            section_count = content.count('\n## ') + content.count('\n### ')

            return SkillMetadata(
                id=skill_id,
                name=frontmatter.get('name', skill_id),
                path=str(skill_md_path.relative_to(self.project_root)),
                description=frontmatter.get('description', 'No description'),
                tags=frontmatter.get('tags', []),
                file_hash=file_hash,
                file_mtime=file_mtime,
                content_length=len(content),
                section_count=section_count,
                last_scanned=datetime.now().isoformat()
            )
        except Exception as e:
            print(f"⚠️  扫描失败 {skill_md_path}: {e}")
            return None

    def _scan_directory(self, category: str) -> List[SkillMetadata]:
        """扫描分类目录下的所有技能"""
        category_path = self.project_root / category
        if not category_path.exists():
            return []

        skills = []
        for item in category_path.iterdir():
            if not item.is_dir() or item.name.startswith('_'):
                continue

            skill_md = item / "SKILL.md"
            if skill_md.exists():
                skill = self._scan_skill_file(skill_md)
                if skill:
                    skills.append(skill)

        return skills

    def rebuild_index(self) -> Dict[str, SkillMetadata]:
        """重建完整索引"""
        print("🔨 正在重建索引...")
        start_time = time.time()

        all_skills: Dict[str, SkillMetadata] = {}

        # 扫描所有分类目录
        for category in DEFAULT_SKILL_PATHS:
            skills = self._scan_directory(category)
            for skill in skills:
                all_skills[skill.id] = skill

        # 扫描外部目录
        external_path = self.project_root / "external"
        if external_path.exists():
            for ext_dir in external_path.iterdir():
                if ext_dir.is_dir() and not ext_dir.name.startswith('.'):
                    skills = self._scan_external_directory(ext_dir)
                    for skill in skills:
                        all_skills[skill.id] = skill

        # 更新索引
        self._index = all_skills
        self._metadata.total_skills = len(all_skills)
        self._metadata.updated_at = datetime.now().isoformat()

        if not self._metadata.created_at:
            self._metadata.created_at = self._metadata.updated_at

        # 更新文件 hash 记录
        for skill_id, skill in all_skills.items():
            self._file_hashes[skill.path] = skill.file_hash
        self._metadata.file_hashes = self._file_hashes

        # 保存缓存
        self._save_cache()

        elapsed = time.time() - start_time
        print(f"✅ 索引重建完成：{len(all_skills)} 个技能，耗时 {elapsed:.2f}s")

        return all_skills

    def _scan_external_directory(self, ext_dir: Path) -> List[SkillMetadata]:
        """扫描外部目录中的技能"""
        skills = []

        # 尝试多种可能的技能路径模式
        patterns = [
            "*/SKILL.md",           # dir/SKILL.md
            "skills/*/SKILL.md",    # dir/skills/SKILL.md
            "*/*/SKILL.md",         # dir/subdir/SKILL.md
        ]

        for pattern in patterns:
            for skill_md in ext_dir.glob(pattern):
                skill = self._scan_skill_file(skill_md)
                if skill and skill.id not in [s.id for s in skills]:
                    skills.append(skill)

        return skills

    def _start_watcher(self):
        """启动文件监控"""
        if self._observer is not None:
            return

        self._event_handler = SkillFileHandler(self)
        self._observer = Observer()

        # 监控所有技能目录
        for category in DEFAULT_SKILL_PATHS:
            category_path = self.project_root / category
            if category_path.exists():
                self._observer.schedule(
                    self._event_handler,
                    str(category_path),
                    recursive=False
                )

        # 监控外部目录
        external_path = self.project_root / "external"
        if external_path.exists():
            self._observer.schedule(
                self._event_handler,
                str(external_path),
                recursive=True
            )

        self._observer.start()
        print("👁️  文件监控已启动")

    def _stop_watcher(self):
        """停止文件监控"""
        if self._observer:
            self._observer.stop()
            self._observer.join()
            self._observer = None
            print("🛑 文件监控已停止")

    def refresh_skill(self, skill_path: Path):
        """刷新单个技能（增量更新）"""
        with self._lock:
            # 检查是否是 SKILL.md 文件
            if skill_path.name != "SKILL.md":
                return

            skill = self._scan_skill_file(skill_path)
            if skill:
                # 检查是否有变化
                old_hash = self._file_hashes.get(str(skill.path), "")
                if old_hash != skill.file_hash:
                    self._index[skill.id] = skill
                    self._file_hashes[str(skill.path)] = skill.file_hash
                    self._metadata.file_hashes = self._file_hashes
                    self._metadata.updated_at = datetime.now().isoformat()
                    self._save_cache()
                    print(f"🔄 已更新技能：{skill.id}")
                else:
                    print(f"⏭️  技能未变化：{skill.id}")
            elif skill_path.exists():
                # 文件存在但解析失败，从索引中移除
                skill_id = skill_path.parent.name.lower().replace('_', '-').replace(' ', '-')
                if skill_id in self._index:
                    del self._index[skill_id]
                    self._save_cache()
                    print(f"🗑️  已移除技能：{skill_id}")

    def remove_skill(self, skill_path: Path):
        """从索引中移除技能"""
        with self._lock:
            skill_id = skill_path.parent.name.lower().replace('_', '-').replace(' ', '-')
            if skill_id in self._index:
                del self._index[skill_id]
                if str(skill_path) in self._file_hashes:
                    del self._file_hashes[str(skill_path)]
                self._metadata.file_hashes = self._file_hashes
                self._metadata.updated_at = datetime.now().isoformat()
                self._save_cache()
                print(f"🗑️  已移除技能：{skill_id}")

    def search(self, query: str, top_n: int = 10) -> List[Dict]:
        """搜索技能"""
        query_lower = query.lower()
        results = []

        for skill_id, skill in self._index.items():
            score = 0

            # name 完全匹配
            if skill.name.lower() == query_lower:
                score += 10
            # name 包含查询
            elif query_lower in skill.name.lower():
                score += 5

            # description 包含查询
            if query_lower in skill.description.lower():
                score += 3

            # tags 匹配
            for tag in skill.tags:
                if query_lower in tag.lower():
                    score += 2

            if score > 0:
                results.append({
                    **asdict(skill),
                    'score': score
                })

        # 按得分排序
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_n]

    def get_skill(self, skill_id: str) -> Optional[SkillMetadata]:
        """获取单个技能"""
        return self._index.get(skill_id)

    def get_all_skills(self) -> Dict[str, SkillMetadata]:
        """获取所有技能"""
        return self._index

    def get_index_stats(self) -> Dict:
        """获取索引统计信息"""
        return {
            'total_skills': self._metadata.total_skills,
            'cache_version': self._metadata.version,
            'created_at': self._metadata.created_at,
            'updated_at': self._metadata.updated_at,
            'cache_file_size': self.index_cache_file.stat().st_size if self.index_cache_file.exists() else 0
        }


class SkillFileHandler(FileSystemEventHandler):
    """技能文件变化事件处理器"""

    def __init__(self, cache: SkillIndexCache):
        self.cache = cache

    def on_modified(self, event):
        if isinstance(event, FileModifiedEvent) and event.src_path.endswith('SKILL.md'):
            print(f"📝 检测到文件修改：{event.src_path}")
            self.cache.refresh_skill(Path(event.src_path))

    def on_created(self, event):
        if isinstance(event, FileCreatedEvent) and event.src_path.endswith('SKILL.md'):
            print(f"📁 检测到新技能：{event.src_path}")
            self.cache.refresh_skill(Path(event.src_path))

    def on_deleted(self, event):
        if isinstance(event, (FileDeletedEvent, DirDeletedEvent)):
            if event.src_path.endswith('SKILL.md'):
                print(f"🗑️  检测到技能删除：{event.src_path}")
                self.cache.remove_skill(Path(event.src_path))


# 便捷函数
def get_skill_cache(project_root: Path = None, auto_watch: bool = True) -> SkillIndexCache:
    """获取技能缓存实例"""
    if project_root is None:
        project_root = Path(__file__).parent.parent.parent.parent
    return SkillIndexCache(project_root, auto_watch)


# CLI 入口
def main():
    import argparse

    parser = argparse.ArgumentParser(description="Skill Cache CLI")
    parser.add_argument('command', choices=['rebuild', 'search', 'stats', 'watch'],
                       help='操作命令')
    parser.add_argument('--query', '-q', help='搜索关键词')
    parser.add_argument('--project', '-p', type=Path, help='项目根目录')
    parser.add_argument('--no-watch', action='store_true', help='禁用文件监控')
    args = parser.parse_args()

    project_root = args.project or Path(__file__).parent.parent.parent.parent

    if args.command == 'rebuild':
        cache = get_skill_cache(project_root, auto_watch=False)
        cache.rebuild_index()

    elif args.command == 'search':
        cache = get_skill_cache(project_root, auto_watch=False)
        if not args.query:
            print("❌ 需要提供搜索关键词，使用 --query 参数")
            return

        results = cache.search(args.query)
        print(f"\n搜索结果 ({len(results)} 个):\n")
        for r in results:
            print(f"  [{r['score']}分] {r['name']}")
            print(f"    路径：{r['path']}")
            print(f"    描述：{r['description'][:80]}...")
            print()

    elif args.command == 'stats':
        cache = get_skill_cache(project_root, auto_watch=False)
        stats = cache.get_index_stats()
        print("\n索引统计:\n")
        print(f"  技能总数：{stats['total_skills']}")
        print(f"  缓存版本：{stats['cache_version']}")
        print(f"  创建时间：{stats['created_at']}")
        print(f"  更新时间：{stats['updated_at']}")
        print(f"  缓存大小：{stats['cache_file_size']:,} bytes")

    elif args.command == 'watch':
        print("👁️  启动文件监控（按 Ctrl+C 停止）...\n")
        cache = get_skill_cache(project_root, auto_watch=True)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            cache._stop_watcher()
            print("\n👋 已退出")


if __name__ == "__main__":
    main()
