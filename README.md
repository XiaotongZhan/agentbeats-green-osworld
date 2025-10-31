# 1. Initialize

## 1.1 Configure Environment

```bash
# Example using Conda
conda env create -f environment.yml
conda activate cs294
poetry install --no-root
```

## 1.2 Quickstart Test

Change into the OSWorld directory:

```bash
cd third_party/osworld
```

Set your AWS region:

```bash
export AWS_REGION=us-east-1
```

Then run:

```bash
python quickstart.py --provider_name aws --os_type Ubuntu
```

## 1.3 Green Agent Smoke Test

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