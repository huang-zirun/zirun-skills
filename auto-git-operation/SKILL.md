---
name: "auto-git-operation"
description: "Automatically performs Git commit, push or pull operations with retry mechanism and Conventional Commits support. Invoke when user needs to commit code with standardized messages, push or pull code, and wants to handle network failures automatically."
triggers:
  - "推送到仓库"
  - "推送代码"
  - "git push"
  - "push"
  - "更新到仓库"
  - "提交到仓库"
  - "上传到仓库"
  - "拉取代码"
  - "git pull"
  - "pull"
  - "同步代码"
  - "更新代码"
  - "提交代码"
  - "git commit"
  - "commit"
  - "生成提交信息"
  - "commit message"
  - "规范提交"
---

# Auto Git Operation

## When to Use

Use this skill when:
- User needs to **commit code** with standardized Conventional Commits format (提交代码/git commit/commit/生成提交信息/commit message/规范提交)
- User needs to **push code** to remote Git repository (推送到仓库/推送代码/git push/push/更新到仓库/提交到仓库/上传到仓库)
- User needs to **pull code** from remote Git repository (拉取代码/git pull/pull/同步代码/更新代码)
- Network connection is unstable
- User wants to automatically handle Git operation failures
- User requests to retry Git operations until successful

## How to Execute

### Operation 1: Generate Conventional Commit Message

When user wants to commit code or generate commit message:

1. **Check Staged Changes**: Run `git diff --cached --stat` to see what files are staged
2. **Get Detailed Diff**: Run `git diff --cached` to see the actual code changes
3. **Analyze Changes**: Determine the type and scope of changes
4. **Generate Commit Message**: Follow Conventional Commits format:
   ```
   <type>(<scope>): <subject>

   <body>

   <footer>
   ```
5. **Present to User**: Show the generated commit message and ask for confirmation
6. **Execute Commit**: If user confirms, run `git commit -m "<message>"`

#### Commit Type Guidelines

| Type | Description | Example |
|------|-------------|---------|
| **feat** | New feature | `feat(auth): add user login functionality` |
| **fix** | Bug fix | `fix(api): resolve null pointer exception` |
| **docs** | Documentation changes | `docs(readme): update installation instructions` |
| **style** | Code style (formatting, no logic change) | `style: unify indentation to 2 spaces` |
| **refactor** | Code refactoring | `refactor(utils): optimize date handling function` |
| **perf** | Performance improvement | `perf(query): optimize database query speed` |
| **test** | Test related | `test(unit): add user module unit tests` |
| **chore** | Build/tooling/dependencies | `chore(deps): upgrade lodash to v4` |
| **ci** | CI/CD configuration | `ci(github): add automated deployment` |
| **build** | Build system | `build(webpack): configure code splitting` |
| **revert** | Revert previous commit | `revert: revert feat(auth) changes` |

#### Commit Message Rules

- **Subject**: 
  - Use verb in present tense
  - Lowercase first letter
  - No period at the end
  - Max 50 characters (Chinese) or 72 characters (English)
- **Scope**: Module name or file name (optional but recommended)
- **Body**: Explain WHY the change was made (optional, wrap at 72 chars)
- **Footer**: Reference issues or breaking changes (optional)

#### Example Commit Messages

**Simple:**
```
feat(user): add password reset functionality
```

**With body:**
```
fix(payment): resolve double charging issue

Payment was processed twice when user clicked submit button
rapidly. Added debounce and idempotency key check.

Fixes #567
```

**Breaking change:**
```
feat(api): migrate to RESTful endpoints

BREAKING CHANGE: All endpoints now use /api/v2/ prefix.
Old /v1/ endpoints are deprecated and will be removed in v3.0.
```

### Operation 2: Git Push

When user wants to push code:

1. **Check Remote**: Verify remote repository is configured
2. **Check Commits**: Ensure there are commits to push
3. **Run Push Loop**:
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

### Operation 3: Git Pull

When user wants to pull code:

1. **Check Status**: Ensure local repository is ready to pull
2. **Run Pull Loop**:
   ```powershell
   while ($true) {
       Write-Host '尝试拉取...' -ForegroundColor Green
       git pull
       if ($LASTEXITCODE -eq 0) {
           Write-Host '拉取成功！' -ForegroundColor Green
           break
       } else {
           Write-Host '拉取失败，5秒后重试...' -ForegroundColor Red
           Start-Sleep -Seconds 5
       }
   }
   ```

## Complete Workflow Examples

### Workflow 1: Commit and Push

When user says "提交并推送代码":

1. Check staged changes: `git diff --cached --stat`
2. If no staged changes, inform user to stage changes first
3. Generate Conventional Commit message based on diff
4. Present message to user for confirmation
5. Execute commit: `git commit -m "<message>"`
6. Push to remote with retry mechanism

### Workflow 2: Quick Push

When user says "推送代码":

1. Check if there are commits to push: `git log @{u}..HEAD --oneline`
2. If no commits, inform user
3. Execute push with retry mechanism

## What to Expect

- **Commit Generation**: AI analyzes changes and generates standardized commit message
- **User Confirmation**: Always ask user to confirm commit message before executing
- **Push Success**: Green "推送成功！" message and process completes
- **Push Failure**: Red "推送失败，5秒后重试..." message and retry after 5 seconds
- **Pull Success**: Green "拉取成功！" message and process completes
- **Pull Failure**: Red "拉取失败，5秒后重试..." message and retry after 5 seconds
- **Continues**: Push/pull runs until operation succeeds or user interrupts

## Notes

- **Commit Message**: Always generate Conventional Commits format for consistency
- **User Confirmation**: Always get user approval before committing
- **Staged Changes**: Commit only works if changes are staged (`git add`)
- **Network Stability**: Push/pull retry mechanism handles network failures
- **Remote Configuration**: Ensure remote repository is properly configured
- **Branch Protection**: Respect branch protection rules on remote repository
