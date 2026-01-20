"""
免费版数据采集器 - 无需AI API
只做数据采集和简单过滤
"""

import json
import time
from datetime import datetime, timedelta
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
import hashlib


class FreeCollector:
    """免费版采集器 - 不使用AI API"""

    def __init__(self):
        """初始化采集器"""
        self.sources = self._get_sources()
        self.keywords = self._get_keywords()
        self.seen_urls = set()

        print(f"✓ 免费版采集器初始化完成，共 {len(self.sources)} 个数据源")

    def _get_sources(self) -> List[Dict]:
        """获取免费数据源"""
        return [
            {
                "id": "hackernews",
                "name": "Hacker News",
                "type": "api",
                "url": "https://hn.algolia.com/api/v1/search?query=AI%20OR%20Claude%20OR%20GPT%20OR%20LLM&tags=story&numericFilters=created_at_i>{timestamp}",
                "priority": 8
            },
            {
                "id": "reddit_ml",
                "name": "Reddit MachineLearning",
                "type": "api",
                "url": "https://www.reddit.com/r/MachineLearning/top.json?t=day&limit=15",
                "priority": 8
            },
            {
                "id": "reddit_ai",
                "name": "Reddit Artificial",
                "type": "api",
                "url": "https://www.reddit.com/r/artificial/top.json?t=day&limit=10",
                "priority": 7
            },
            {
                "id": "arxiv_ai",
                "name": "arXiv AI论文",
                "type": "arxiv",
                "url": "http://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=10",
                "priority": 8
            }
        ]

    def _get_keywords(self) -> Dict:
        """获取过滤关键词"""
        return {
            "required": [
                "AI", "人工智能", "Claude", "GPT", "LLM", "机器学习",
                "深度学习", "Anthropic", "OpenAI", "大模型", "prompt",
                "agent", "transformer", "neural", "model", "chatbot"
            ],
            "excluded": [
                "crypto", "blockchain", "NFT", "广告", "推广", "spam"
            ]
        }

    def collect_all(self) -> List[Dict]:
        """采集所有数据源"""
        all_items = []

        for source in self.sources:
            try:
                print(f"采集: {source['name']}...", end=" ")
                items = self._collect_source(source)
                print(f"✓ {len(items)}条")
                all_items.extend(items)
                time.sleep(2)
            except Exception as e:
                print(f"✗ 失败: {str(e)}")
                continue

        unique_items = self._deduplicate(all_items)
        print(f"\n总计: {len(all_items)}条 → 去重后: {len(unique_items)}条")

        unique_items.sort(key=lambda x: (x.get('priority', 0), x.get('published_at', '')), reverse=True)

        return unique_items

    def _collect_source(self, source: Dict) -> List[Dict]:
        """采集单个数据源"""
        if source['type'] == 'api':
            if 'hackernews' in source['id']:
                return self._collect_hackernews(source)
            elif 'reddit' in source['id']:
                return self._collect_reddit(source)
        elif source['type'] == 'arxiv':
            return self._collect_arxiv(source)
        return []

    def _collect_hackernews(self, source: Dict) -> List[Dict]:
        """采集Hacker News"""
        items = []
        timestamp = int((datetime.now() - timedelta(days=1)).timestamp())
        url = source['url'].replace('{timestamp}', str(timestamp))

        response = requests.get(url, timeout=15)
        data = response.json()

        for hit in data.get('hits', [])[:10]:
            title = hit.get('title', '')
            if not self._is_relevant(title):
                continue

            items.append({
                'title': title,
                'summary': f"Hacker News热议: {title}",
                'url': hit.get('url', f"https://news.ycombinator.com/item?id={hit.get('objectID')}"),
                'source': source['name'],
                'priority': source['priority'] + (1 if hit.get('points', 0) > 100 else 0),
                'published_at': hit.get('created_at', ''),
                'metadata': {
                    'points': hit.get('points', 0),
                    'comments': hit.get('num_comments', 0)
                }
            })

        return items

    def _collect_reddit(self, source: Dict) -> List[Dict]:
        """采集Reddit"""
        items = []
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; AINewsBot/1.0)'}

        response = requests.get(source['url'], headers=headers, timeout=15)
        data = response.json()

        for post in data['data']['children'][:10]:
            post_data = post['data']
            title = post_data.get('title', '')

            if not self._is_relevant(title):
                continue

            items.append({
                'title': title,
                'summary': post_data.get('selftext', '')[:200] or f"Reddit讨论: {title}",
                'url': f"https://www.reddit.com{post_data.get('permalink')}",
                'source': source['name'],
                'priority': source['priority'] + (1 if post_data.get('score', 0) > 100 else 0),
                'published_at': datetime.fromtimestamp(post_data.get('created_utc')).isoformat(),
                'metadata': {
                    'score': post_data.get('score', 0),
                    'comments': post_data.get('num_comments', 0)
                }
            })

        return items

    def _collect_arxiv(self, source: Dict) -> List[Dict]:
        """采集arXiv论文"""
        items = []

        try:
            response = requests.get(source['url'], timeout=15)
            from xml.etree import ElementTree as ET
            root = ET.fromstring(response.content)

            ns = {'atom': 'http://www.w3.org/2005/Atom'}

            for entry in root.findall('atom:entry', ns)[:8]:
                title = entry.find('atom:title', ns).text.strip()
                summary = entry.find('atom:summary', ns).text.strip()[:300]

                if not self._is_relevant(title + ' ' + summary):
                    continue

                items.append({
                    'title': f"[论文] {title}",
                    'summary': summary,
                    'url': entry.find('atom:id', ns).text,
                    'source': source['name'],
                    'priority': source['priority'],
                    'published_at': entry.find('atom:published', ns).text,
                    'metadata': {'type': 'paper'}
                })

        except Exception as e:
            print(f"arXiv采集失败: {str(e)}")

        return items

    def _is_relevant(self, text: str) -> bool:
        """检查内容是否相关"""
        text_lower = text.lower()

        for excluded in self.keywords['excluded']:
            if excluded.lower() in text_lower:
                return False

        for required in self.keywords['required']:
            if required.lower() in text_lower:
                return True

        return False

    def _deduplicate(self, items: List[Dict]) -> List[Dict]:
        """去重"""
        unique_items = []
        seen_hashes = set()

        for item in items:
            content = f"{item['url']}_{item['title']}"
            content_hash = hashlib.md5(content.encode()).hexdigest()

            if content_hash not in seen_hashes:
                seen_hashes.add(content_hash)
                unique_items.append(item)

        return unique_items


if __name__ == "__main__":
    collector = FreeCollector()
    items = collector.collect_all()

    print(f"\n成功采集 {len(items)} 条资讯")
    for idx, item in enumerate(items[:5], 1):
        print(f"\n{idx}. {item['title']}")
        print(f"   来源: {item['source']}")
