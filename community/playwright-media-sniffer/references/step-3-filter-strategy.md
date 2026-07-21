# Step 3 Filter Strategy

_从 playwright-media-sniffer v1.0 SKILL.md 抽取 (Line 198-232)_

### Step 3: 智能筛选

```python
# 优先级排序
def prioritize_resources(resources):
    scored = []
    for r in resources:
        url = r['url']
        score = 0
        
        # M3U8/MPD 高优先级（主清单）
        if '.m3u8' in url and 'index' in url:
            score += 10
        elif '.mpd' in url:
            score += 10
        elif '.m3u8' in url:
            score += 5
        
        # 分片文件低优先级（只下载主清单）
        if '.ts' in url or '.m4s' in url:
            score -= 5
        
        # 直接 MP4 中优先级
        if '.mp4' in url and 'playlist' not in url:
            score += 7
        
        scored.append((score, r))
    
    # 按分数排序，返回前3个
    scored.sort(reverse=True, key=lambda x: x[0])
    return [r for _, r in scored[:3]]

best_resources = prioritize_resources(captured_resources)
```

