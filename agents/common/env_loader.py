import os
from pathlib import Path
from dotenv import load_dotenv

def load_and_validate_env():
    # 1) 从仓库根目录加载 .env
    repo_root = Path(__file__).resolve().parents[2]
    env_path = repo_root / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)

    # 2) 最少校验
    required = ["AWS_REGION"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        raise EnvironmentError(f"Missing environment variable(s): {missing}. "
                               f"Put them in {env_path} or export before running.")

    # 3) 方便外部使用
    return {
        "AWS_REGION": os.getenv("AWS_REGION"),
        "AWS_DEFAULT_REGION": os.getenv("AWS_DEFAULT_REGION", os.getenv("AWS_REGION")),
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "OPENAI_BASE_URL": os.getenv("OPENAI_BASE_URL"),
        "REPO_ROOT": str(repo_root),
    }