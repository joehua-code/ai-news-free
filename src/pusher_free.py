"""
免费版推送模块 - 飞书Webhook
"""

import os
import requests
from datetime import datetime


class FreePusher:
    """免费版推送器"""

    def __init__(self):
        self.feishu_webhook = os.getenv('FEISHU_WEBHOOK_URL')

        if not self.feishu_webhook:
            print("⚠️  未配置飞书Webhook，报告将只保存到本地")

    def push_to_feishu(self, content: str) -> bool:
        """推送到飞书"""
        if not self.feishu_webhook:
            return False

        try:
            payload = {
                "msg_type": "interactive",
                "card": {
                    "header": {
                        "title": {
                            "content": f"🤖 AI资讯日报 - {datetime.now().strftime('%Y年%m月%d日')}",
                            "tag": "plain_text"
                        },
                        "template": "blue"
                    },
                    "elements": [
                        {
                            "tag": "markdown",
                            "content": self._truncate_for_feishu(content)
                        },
                        {
                            "tag": "hr"
                        },
                        {
                            "tag": "note",
                            "elements": [
                                {
                                    "tag": "plain_text",
                                    "content": f"💰 完全免费 | 📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                                }
                            ]
                        }
                    ]
                }
            }

            response = requests.post(
                self.feishu_webhook,
                json=payload,
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0 or result.get('StatusCode') == 0:
                    print("✓ 飞书推送成功")
                    return True
                else:
                    print(f"✗ 飞书推送失败: {result}")
                    return False
            else:
                print(f"✗ 飞书推送失败，HTTP {response.status_code}")
                return False

        except Exception as e:
            print(f"✗ 飞书推送异常: {str(e)}")
            return False

    def save_to_file(self, content: str) -> bool:
        """保存到文件"""
        try:
            import os
            os.makedirs('data/reports', exist_ok=True)

            filename = f"data/reports/ai-news-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"✓ 报告已保存: {filename}")
            return True

        except Exception as e:
            print(f"✗ 保存文件失败: {str(e)}")
            return False

    def _truncate_for_feishu(self, content: str) -> str:
        """截断内容以适配飞书限制"""
        MAX_LENGTH = 8000

        if len(content) <= MAX_LENGTH:
            return content

        return content[:MAX_LENGTH] + "\n\n...(内容过长，已截断。完整报告请查看GitHub仓库)"


if __name__ == "__main__":
    pusher = FreePusher()

    test_content ="""# 测试报告

这是一条测试消息。

## 测试内容

- 项目1
- 项目2
"""

    pusher.push_to_feishu(test_content)
    pusher.save_to_file(test_content)
