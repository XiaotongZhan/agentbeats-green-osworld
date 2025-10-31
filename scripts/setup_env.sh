#!/bin/bash
# =========================================================
# Activate the cs294 environment and load .env (non-interactive friendly)
# Usage: source scripts/setup_env.sh
#        or in other scripts: source "$(dirname "$0")/setup_env.sh"
# =========================================================

set -e

# Move to repo root (script lives in scripts/)
cd "$(dirname "$0")/.." || exit 1

# ---------------- 1) Initialize conda hook ---------------
if command -v conda >/dev/null 2>&1; then
  __conda_setup="$('conda' 'shell.bash' 'hook' 2>/dev/null)" || true
  if [ -n "$__conda_setup" ]; then
    eval "$__conda_setup"
  fi
fi

# Fallback: source conda.sh directly if conda hook is not available
if ! command -v conda >/dev/null 2>&1 || [ -z "${CONDA_EXE:-}" ]; then
  for CAND in \
    "$HOME/miniconda3/etc/profile.d/conda.sh" \
    "$HOME/anaconda3/etc/profile.d/conda.sh" \
    "/opt/conda/etc/profile.d/conda.sh"
  do
    if [ -f "$CAND" ]; then
      # shellcheck source=/dev/null
      . "$CAND"
      break
    fi
  done
fi

# ---------------- 2) Activate cs294 env (prefer conda, fallback to local venv) ----------------
ENV_NAME="${VENV_NAME:-cs294}"

if command -v conda >/dev/null 2>&1; then
  echo "Found conda. Activating env: $ENV_NAME"
  conda activate "$ENV_NAME"
elif [ -d "./$ENV_NAME/bin" ]; then
  # Support a local Python venv at ./cs294
  # shellcheck source=/dev/null
  source "./$ENV_NAME/bin/activate"
  echo "Activated venv: ./$ENV_NAME"
else
  echo "Cannot activate environment '$ENV_NAME'."
  echo "  - Conda: conda create -n $ENV_NAME python=3.10 && conda activate $ENV_NAME"
  echo "  - venv : python -m venv $ENV_NAME && source $ENV_NAME/bin/activate"
  exit 1
fi

# Quick confirmation
echo "Active env: ${CONDA_DEFAULT_ENV:-$(basename "${VIRTUAL_ENV:-}" 2>/dev/null)}"
python -V || true
which python || true

# ---------------- 3) Load .env (export all vars) ----------------
if [ -f ".env" ]; then
  set -a
  # shellcheck source=/dev/null
  . ./.env
  set +a
  echo "Loaded environment variables from .env"
else
  echo ".env not found. You may need to create it (see .env.example)"
fi

# ---------------- 4) Print key signals (masked) ----------------
echo "AWS_REGION=${AWS_REGION:-<unset>}"

mask() {
  # Print first 8 chars then asterisks; if empty, print "<unset>"
  local val="$1"
  if [ -n "$val" ]; then
    printf "%s********\n" "${val:0:8}"
  else
    printf "<unset>\n"
  fi
}

# Prefer explicit per-provider signals to avoid confusion
echo -n "OPENAI_API_KEY=";        mask "${OPENAI_API_KEY:-}"
echo -n "ANTHROPIC_API_KEY=";     mask "${ANTHROPIC_API_KEY:-}"
echo -n "DASHSCOPE_API_KEY=";     mask "${DASHSCOPE_API_KEY:-}"
echo -n "AZURE_OPENAI_API_KEY=";  mask "${AZURE_OPENAI_API_KEY:-}"

echo "Environment setup complete!"
