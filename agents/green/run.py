# agents/green/run.py
import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OSWORLD_DIR = REPO_ROOT / "third_party" / "osworld"

def osworld_path() -> str:
    return str(OSWORLD_DIR)

def _infer_domain_from_example(example_path: Path) -> str:
    parts = list(example_path.resolve().parts)
    if "examples" in parts:
        idx = parts.index("examples")
        if idx + 1 < len(parts):
            return parts[idx + 1]
    return example_path.parent.name

def _build_temp_meta_for_single(example_path: Path) -> Path:
    domain = _infer_domain_from_example(example_path)
    example_id = example_path.stem

    data = {domain: [example_id]}

    tmp = tempfile.NamedTemporaryFile(
        "w", delete=False, suffix=".json", prefix="osworld_meta_", dir=str(REPO_ROOT)
    )
    with tmp as f:
        json.dump(data, f)
    return Path(tmp.name)

def run_osworld_runner(
    agent_name: str,
    model: str,
    result_dir: str,
    provider_name: str,
    headless: bool,
    max_steps: int,
    num_envs: int,
    test_all_meta_path: str | None = None,
    domain: str | None = None,
    single_example: str | None = None,
):
    py_exec = sys.executable
    runner = OSWORLD_DIR / "run_multienv_qwen25vl.py"

    cmd = [
        py_exec, str(runner),
        "--headless" if headless else "",
        "--observation_type", "screenshot",
        "--model", model,
        "--result_dir", result_dir,
        "--max_steps", str(max_steps),
        "--num_envs", str(num_envs),
        "--provider_name", provider_name,
        "--region", os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1")),
    ]

    cmd = [c for c in cmd if c]

    if single_example:
        example_path = Path(single_example)
        if not example_path.exists():
            raise FileNotFoundError(f"single_example not found: {example_path}")
        meta_path = _build_temp_meta_for_single(example_path)
        cmd += ["--test_all_meta_path", str(meta_path)]
        cmd += ["--domain", _infer_domain_from_example(example_path)]
    else:
        if test_all_meta_path:
            cmd += ["--test_all_meta_path", str(Path(test_all_meta_path).resolve())]
        if domain:
            cmd += ["--domain", domain]

    cmd += ["--screen_width", "1920", "--screen_height", "1080"]

    env = os.environ.copy()
    print("▶️  Running:", " ".join(cmd))
    subprocess.run(cmd, check=True, cwd=osworld_path(), env=env)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent_name", type=str, default="qwen/qwen2.5-vl-32b-instruct")
    parser.add_argument("--model", type=str, default="qwen/qwen2.5-vl-32b-instruct")
    parser.add_argument("--test_all_meta_path", type=str, default=None)
    parser.add_argument("--result_dir", type=str, default=str(REPO_ROOT / "results"))
    parser.add_argument("--provider_name", type=str, default="aws")
    parser.add_argument("--os_type", type=str, default="Ubuntu")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--max_steps", type=int, default=5)
    parser.add_argument("--num_envs", type=int, default=1)
    parser.add_argument("--domain", type=str, default=None)
    parser.add_argument("--single_example", type=str, default=None, help="Path to a single example .json")
    parser.add_argument("--skip_run", action="store_true")
    args = parser.parse_args()

    if args.skip_run:
        print("[info] skip_run enabled; not launching OSWorld.")
        return

    run_osworld_runner(
        agent_name=args.agent_name,
        model=args.model,
        result_dir=args.result_dir,
        provider_name=args.provider_name,
        headless=args.headless,
        max_steps=args.max_steps,
        num_envs=args.num_envs,
        test_all_meta_path=args.test_all_meta_path,
        domain=args.domain,
        single_example=args.single_example,
    )

if __name__ == "__main__":
    main()