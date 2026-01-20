"""
AI资讯监测系统 - 免费版主程序
完全免费，无需付费API
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from collector_free import FreeCollector
from reporter_free import FreeReporter
from pusher_free import FreePusher


def main():
    """主函数"""
    print("=" * 60)
    print("AI资讯监测系统 - 免费版")
    print(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()

    try:
        # 1. 数据采集
        print("[步骤 1/3] 数据采集")
        print("-" * 60)
        collector = FreeCollector()
        items = collector.collect_all()

        if not items:
            print("\n⚠️  未采集到任何资讯")
            return False

        print(f"\n✓ 采集完成: {len(items)} 条资讯")
        print()

        # 2. 生成报告
        print("[步骤 2/3] 生成报告")
        print("-" * 60)
        reporter = FreeReporter()
        report = reporter.generate_report(items)
        print(f"✓ 报告生成完成，长度: {len(report)} 字符")
        print()

        # 3. 推送和保存
        print("[步骤 3/3] 推送和保存")
        print("-" * 60)
        pusher = FreePusher()

        # 保存到文件
        pusher.save_to_file(report)

        # 推送到飞书
        if os.getenv('FEISHU_WEBHOOK_URL'):
            pusher.push_to_feishu(report)
        else:
            print("ℹ️  未配置飞书Webhook，跳过推送")

        print()
        print("=" * 60)
        print("✓ 任务执行成功！")
        print("=" * 60)

        return True

    except Exception as e:
        print()
        print("=" * 60)
        print(f"✗ 任务执行失败: {str(e)}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
