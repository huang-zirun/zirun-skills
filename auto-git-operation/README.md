# Auto Git Operation

自动执行 Git 提交、推送和拉取操作，支持重试机制和 Conventional Commits 规范。

## 功能特性

- **自动生成提交信息**: 基于代码变更自动生成符合 Conventional Commits 规范的提交信息
- **智能推送**: 自动处理推送失败，带重试机制
- **自动拉取**: 网络不稳定时自动重试拉取操作
- **提交类型支持**: feat, fix, docs, style, refactor, perf, test, chore, ci, build, revert

## 使用场景

- 需要提交代码并生成规范化的提交信息
- 推送代码到远程仓库时网络不稳定
- 从远程仓库拉取代码时遇到网络问题
- 希望自动处理 Git 操作失败的情况

## 提交信息规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 提交类型

| 类型 | 说明 | 示例 |
|------|------|------|
| feat | 新功能 | `feat(auth): add user login functionality` |
| fix | 修复 bug | `fix(api): resolve null pointer exception` |
| docs | 文档变更 | `docs(readme): update installation instructions` |
| style | 代码格式 | `style: unify indentation to 2 spaces` |
| refactor | 代码重构 | `refactor(utils): optimize date handling function` |
| perf | 性能优化 | `perf(query): optimize database query speed` |
| test | 测试相关 | `test(unit): add user module unit tests` |
| chore | 构建/工具/依赖 | `chore(deps): upgrade lodash to v4` |
| ci | CI/CD 配置 | `ci(github): add automated deployment` |
| build | 构建系统 | `build(webpack): configure code splitting` |
| revert | 回滚提交 | `revert: revert feat(auth) changes` |

## 触发关键词

- 推送: `推送到仓库`, `推送代码`, `git push`, `push`, `更新到仓库`, `提交到仓库`, `上传到仓库`
- 拉取: `拉取代码`, `git pull`, `pull`, `同步代码`, `更新代码`
- 提交: `提交代码`, `git commit`, `commit`, `生成提交信息`, `commit message`, `规范提交`

## 工作流程

### 提交并推送

1. 检查已暂存的变更: `git diff --cached --stat`
2. 分析变更内容
3. 生成符合规范的提交信息
4. 用户确认后执行提交
5. 推送到远程仓库（带重试机制）

### 快速推送

1. 检查是否有待推送的提交: `git log @{u}..HEAD --oneline`
2. 执行推送（带重试机制）

### 拉取代码

1. 检查本地仓库状态
2. 执行拉取（带重试机制）

## 重试机制

推送和拉取操作会在失败时自动重试：

```powershell
while ($true) {
    Write-Host '尝试推送...' -ForegroundColor Green
    git push
    if ($LASTEXITCODE -eq 0) {
        Write-Host '推送成功！' -ForegroundColor Green
        break
    } else {
        Write-Host '推送失败，5秒后重试...' -ForegroundColor Red
        Start-Sleep -Seconds 5
    }
}
```

## 注意事项

- 提交前需要先将变更添加到暂存区 (`git add`)
- 确保远程仓库已正确配置
- 遵守远程仓库的分支保护规则
- 提交信息会请求用户确认后再执行
