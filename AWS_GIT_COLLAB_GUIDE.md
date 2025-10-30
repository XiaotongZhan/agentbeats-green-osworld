---
title: AWS GIT COLLAB GUIDE
author: Zhan Xiaotong
date: 2025-10-30
---

# 1. 准备个人工作目录

创建一个自己的独立文件夹，例如：

```bash
mkdir -p ~/zxt && cd ~/zxt
````

# 2. 生成个人 SSH 密钥（每人一把，不会冲突）

注意文件名使用自己的名字缩写或 ID，比如 `id_ed25519_zxt`：

```bash
ssh-keygen -t ed25519 -C "你的GitHub邮箱" -f ~/.ssh/id_ed25519_zxt -N ""
```

启动 ssh-agent 并加载密钥：

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519_zxt
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519_zxt ~/.ssh/id_ed25519_zxt.pub
```

# 3. 配置 SSH 别名（让 Git 知道用哪把钥匙）

打开或创建配置文件：

```bash
nano ~/.ssh/config
```

在文件末尾添加：

```bash
# === zxt 专用 GitHub SSH 配置 ===
Host github-zxt
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_zxt
    IdentitiesOnly yes
```

保存退出：

* `Ctrl + O` → 回车保存
* `Ctrl + X` → 退出编辑器

然后设置权限：

```bash
chmod 600 ~/.ssh/config
```

# 4. 把公钥加到 GitHub

查看公钥内容：

```bash
cat ~/.ssh/id_ed25519_zxt.pub
```

复制整行内容，然后在 GitHub 中操作：

**GitHub → Settings → SSH and GPG keys → New SSH key**

* **Title**: `aws-zxt`
* **Key**: 粘贴刚才复制的内容
* 点击 **Add SSH key**

验证是否配置成功：

```bash
ssh -T git@github-zxt
```

成功提示示例：

```bash
Hi <你的GitHub用户名>! You've successfully authenticated, but GitHub does not provide shell access.
```

# 5. 克隆仓库（用你自己的别名）

```bash
cd ~/zxt
git clone git@github-zxt:XiaotongZhan/cs294-ai-agent.git
cd cs294-ai-agent
```

# 6. 设置仓库级 Git 身份（只影响当前仓库）

```bash
git config user.name  "Zhan Xiaotong"
git config user.email "你的邮箱@example.com"
```

验证配置：

```bash
git config --list
```