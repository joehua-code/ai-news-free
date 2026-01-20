"""
免费版报告生成器 - 使用模板，不使用AI
"""

from datetime import datetime
from typing import List, Dict


class FreeReporter:
    """免费版报告生成器"""

    def __init__(self):
        print("✓ 免费版报告生成器初始化完成")

    def generate_report(self, items: List[Dict]) -> str:
        """生成报告"""
        if not items:
            return "今日暂无AI资讯更新。"

        categorized = self._categorize(items)
        report = self._build_report(categorized, items)

        return report

    def _categorize(self, items: List[Dict]) -> Dict:
        """简单分类"""
        categories = {
            'papers': [],
            'discussions': [],
            'news': [],
            'other': []
        }

        for item in items:
            title_lower = item['title'].lower()

            if any(word in title_lower for word in ['paper', '论文', 'arxiv']):
                categories['papers'].append(item)
            elif any(word in item['source'].lower() for word in ['reddit', 'hacker']):
                categories['discussions'].append(item)
            else:
                categories['other'].append(item)

        return categories

    def _build_report(self, categorized: Dict, all_items: List[Dict]) -> str:
        """构建报告"""
        today = datetime.now().strftime('%Y年%m月%d日')

        report = f"""# 🤖 AI资讯日报 - {today}

> 由GitHub Actions自动采集 | 完全免费

## 📊 今日概览

今日共采集到 **{len(all_items)}** 条AI行业资讯，涵盖学术论文、社区讨论、行业新闻等多个维度。

---

## 🔥 热门资讯 TOP 10

"""

        for idx, item in enumerate(all_items[:10], 1):
            report += self._format_item(idx, item)

        if categorized['papers']:
            report += "\n---\n\n## 📚 学术论文\n\n"
            for idx, item in enumerate(categorized['papers'][:5], 1):
                report += self._format_simple_item(idx, item)

        if categorized['discussions']:
            report += "\n---\n\n## 💬 社区讨论\n\n"
            for idx, item in enumerate(categorized['discussions'][:5], 1):
                report += self._format_simple_item(idx, item)

        report += f"""

---

## 📌 说明

- 📡 **数据来源**: Hacker News, Reddit, arXiv等
- 🤖 **自动化**: GitHub Actions每天自动运行
- 💰 **成本**: 完全免费
- 📅 **更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

⭐ **觉得有用？** 给项目点个Star吧！
"""

        return report

    def _format_item(self, idx: int, item: Dict) -> str:
        """格式化条目（详细版）"""
        metadata = item.get('metadata', {})

        meta_str = ""
        if 'points' in metadata:
            meta_str += f" | 👍 {metadata['points']}分"
        if 'comments' in metadata:
            meta_str += f" | 💬 {metadata['comments']}评论"
        if 'score' in metadata:
            meta_str += f" | ⬆️ {metadata['score']}"

        return f"""### {idx}. {item['title']}

**来源**: {item['source']}{meta_str}

**摘要**: {item['summary'][:150]}{'...' if len(item['summary']) > 150 else ''}

[🔗 查看详情]({item['url']})

"""

    def _format_simple_item(self, idx: int, item: Dict) -> str:
        """格式化条目（简洁版）"""
        return f"{idx}. **{item['title']}**\n   - 来源: {item['source']}\n   - 链接: {item['url']}\n\n"


if __name__ == "__main__":
    test_items = [
        {
            'title': 'Claude 4.0发布',
            'summary': '全新架构，性能提升50%',
            'url': 'https://example.com',
            'source': '机器之心',
            'priority': 10,
            'metadata': {}
        }
    ]

    reporter = FreeReporter()
    report = reporter.generate_report(test_items)
    print(report)
