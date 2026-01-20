# AI资讯监测系统 - 免费版

> 完全免费，无需任何付费API，使用GitHub Actions自动运行

## ✨ 特点

- 🎉 **完全免费** - 零成本运行
- 🚀 **自动运行** - GitHub Actions每天自动执行
- 📊 **5+数据源** - 覆盖AI行业核心资讯
- 🔍 **智能过滤** - 基于关键词自动筛选
- 📱 **飞书推送** - 自动推送到飞书群

## 快速开始

### 1. 配置飞书Webhook

1. 飞书群 → 添加机器人 → 自定义机器人
2. 复制Webhook地址

### 2. 配置GitHub Secrets

1. Settings → Secrets and variables → Actions
2. New repository secret
3. Name: `FEISHU_WEBHOOK_URL`
4. Value: 你的飞书Webhook地址

### 3. 启用GitHub Actions

1. Actions 标签
2. "I understand my workflows, go ahead and enable them"

### 4. 手动测试

Actions → AI News Collection → Run workflow

## 成本

**$0/月** - 完全免费！

## 数据源

- Hacker News
- Reddit r/MachineLearning
- Reddit r/Artificial
- arXiv AI论文
- 机器之心
