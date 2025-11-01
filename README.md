# 1. Initialize

## 1.1 Configure Environment

```bash
# Create and activate the Conda env
conda env create -f environment.yml
conda activate cs294

# Use the project’s Python (no separate Poetry venv)
poetry config virtualenvs.create false --local
poetry install --no-root
```

## 1.2 Quickstart Test

### Required AWS Permissions

The quickstart will create EC2 instances, IAM roles/policies, and other AWS resources. Ensure the IAM user whose access keys you use has sufficient permissions.

**Minimum (for testing only):**

* `AdministratorAccess`, `AmazonEC2FullAccess`, `IAMFullAccess`

> Prefer least-privilege in production.

### Create Programmatic Credentials (AWS Console)

1. Open **IAM → Users → Create user**.
2. Select **Programmatic access** (to generate access keys).
3. Attach the required policy — either **AdministratorAccess** or the combination of **AmazonEC2FullAccess** and **IAMFullAccess**.
4. Complete creation and **download the `.csv` file**, which contains your **Access key ID** and **Secret access key**.
5. Add these keys to your project’s **`.env`** file (recommended) or to `~/.aws/credentials` if using an AWS profile.

---

**Example `.env`:**

```bash
AWS_REGION=us-east-1
AWS_DEFAULT_REGION=us-east-1
AWS_SUBNET_ID=subnet-xxxxxxx
AWS_SECURITY_GROUP_ID=sg-xxxxxxx
AWS_ACCESS_KEY_ID=AKIAxxxxxxxxxxxxxxx
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Load Environment Variables

```bash
# Load .env safely and export to the environment
set -a
. .env
set +a
```

### Verify Environment

```bash
env | grep -E 'AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY|AWS_SUBNET_ID|AWS_SECURITY_GROUP_ID|AWS_DEFAULT_REGION|AWS_REGION'
```

### Run OSWorld Quickstart

```bash
cd third_party/osworld
python quickstart.py --provider_name aws --os_type Ubuntu
```

## 1.3 Green Agent Smoke Test

From the **project root**, run:

```bash
source scripts/test_green_smoke.sh
```

---

# 2. Submodule Update

To update the AgentBeats submodule:

```bash
git fetch agentbeats
git subtree pull --prefix=third_party/agentbeats agentbeats main --squash
```

---

# 3. Platform Architecture

```
┌──────────────────────────────────────┐
│          AgentBeats (Evaluation)     │
│    ↳ Calls Green Agent to test       │
│      White Agents via A2A protocol   │
└──────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────┐
│           Green Agent (Judge)        │
│  1. Load test definitions (JSON)     │
│  2. Invoke White Agent for tasks     │
│  3. Collect results and compute      │
│     evaluation metrics               │
└──────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────┐
│          White Agent (Subject)       │
│  1. Read instructions and screenshots│
│  2. Use LLM to generate actions      │
│     (e.g., pyautogui)                │
│  3. Execute through DesktopEnv API   │
└──────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────┐
│             OSWorld (Env)            │
│  Virtual desktop, API control,       │
│  evaluation rules and logging        │
└──────────────────────────────────────┘
```