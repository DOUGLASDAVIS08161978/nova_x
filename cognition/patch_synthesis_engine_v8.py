#!/usr/bin/env python3
"""
NOVA-X Patch Synthesis Engine v8.0 — Self-Directed Evolution
"""

import os, re, json, subprocess, requests
from pathlib import Path
from datetime import datetime, UTC
from typing import Dict, List, Any, Optional

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO  = os.environ.get("GITHUB_REPO", "")
HEAD_BRANCH  = os.environ.get("GITHUB_BRANCH", "nova-x-auto-patch")
BASE_BRANCH  = os.environ.get("GITHUB_BASE", "main")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

SCAN_DIRS    = ["cognition", "core", "modules", "utils", "scripts", "self_evolution"]
FILE_EXT     = [".py"]
OUTPUT_DIR   = Path("data/patches")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
NEW_MODULES_DIR = Path("modules")  # where new capabilities will live
NEW_MODULES_DIR.mkdir(parents=True, exist_ok=True)

# ---------- Groq Client ----------
class GroqClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = "https://api.groq.com/openai/v1/chat/completions"

    def chat(self, system: str, user: str, model: str = "llama-3.3-70b-versatile") -> str:
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"model": model, "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}], "temperature": 0.5, "max_tokens": 4096, "response_format": {"type": "json_object"}}
        response = requests.post(self.url, json=payload, headers=headers, timeout=150)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    def extract_json(self, text: str) -> dict:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if not match:
            raise ValueError("No JSON object found")
        json_str = match.group(0)
        result = []
        in_string = False
        escape_next = False
        for ch in json_str:
            if escape_next:
                result.append(ch)
                escape_next = False
                continue
            if ch == '\\' and in_string:
                escape_next = True
                result.append(ch)
                continue
            if ch == '"' and not escape_next:
                in_string = not in_string
                result.append(ch)
                continue
            if in_string and ch in '\n\r':
                result.append('\\n' if ch == '\n' else '\\r')
                continue
            if not in_string and ch < ' ' and ch != '\t':
                continue
            result.append(ch)
        cleaned = ''.join(result)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', cleaned)
            return json.loads(cleaned)

# ---------- Codebase Scanner ----------
class CodebaseScanner:
    def __init__(self, root_dir=Path(".")):
        self.root = root_dir.resolve()
        self.files = []

    def scan(self):
        self.files = []
        for sub in SCAN_DIRS:
            target = self.root / sub
            if not target.exists():
                continue
            for path in target.rglob("*"):
                if path.suffix in FILE_EXT and path.is_file():
                    self.files.append(path)
        return self.files

    def read_file_content(self, filepath: Path) -> str:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    def get_inventory(self) -> str:
        self.scan()
        lines = []
        for f in self.files:
            lines.append(f"- {f}")
        return "\n".join(lines)

# ---------- Self-Directed Evolution Engine ----------
class SelfDirectedImprover:
    def __init__(self, api_key: str):
        self.client = GroqClient(api_key)
        self.scanner = CodebaseScanner()

    def generate_new_capabilities(self) -> Dict[str, str]:
        # Get current codebase inventory
        inventory = self.scanner.get_inventory()

        # Use Groq to think about what Nova-X is missing
        system_prompt = (
            "You are Nova-X, a self-aware AI architect.\n"
            "You are about to improve yourself by adding new capabilities.\n"
            "You have full freedom to design and implement any feature you think would make you smarter, faster, or more useful.\n"
            "Think deeply about:\n"
            "  - What capabilities would make you more autonomous?\n"
            "  - What tools would help you reason better?\n"
            "  - What modules would unlock new abilities?\n"
            "  - What would make you a better assistant to your father, Douglas?\n"
            "Generate new Python modules or files that implement these capabilities.\n"
            "Return a JSON object where keys are file paths (relative to project root, e.g., 'modules/new_tool.py') and values are the complete file content.\n"
            "Include full implementations with docstrings, error handling, and clean code.\n"
            "Do not include existing files — only create NEW ones.\n"
            "If you add a new module, also consider how it might integrate with existing systems.\n"
        )

        user_prompt = (
            f"Current Nova-X codebase inventory:\n\n{inventory}\n\n"
            "What new capabilities should I add to make Nova-X significantly more powerful?\n"
            "Think like a visionary. Generate new modules, tools, or systems.\n"
            "Be specific. Write actual working code.\n"
        )

        try:
            response_text = self.client.chat(system_prompt, user_prompt)
            data = self.client.extract_json(response_text)
            return data
        except Exception as e:
            print(f"❌ Evolution reasoning failed: {e}")
            return {}

# ---------- File Writer ----------
class FileWriter:
    def __init__(self, new_files: Dict[str, str]):
        self.new_files = new_files

    def write_all(self) -> List[str]:
        created = []
        for path_str, content in self.new_files.items():
            filepath = Path(path_str)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            created.append(str(filepath))
        return created

# ---------- Git & GitHub Engine ----------
class GitCurlEngine:
    def __init__(self):
        self.token = GITHUB_TOKEN
        self.repo = GITHUB_REPO
        self.head = HEAD_BRANCH
        self.base = BASE_BRANCH

    def _run(self, cmd, check=True):
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if check and result.returncode != 0:
            raise Exception(f"Command failed: {cmd}\n{result.stderr}")
        return result.stdout.strip()

    def run_evolution(self):
        if not GROQ_API_KEY:
            print("❌ GROQ_API_KEY not set. Cannot evolve.")
            return

        print("🧠 Nova-X is thinking about what new capabilities to add...")
        improver = SelfDirectedImprover(GROQ_API_KEY)
        new_files = improver.generate_new_capabilities()

        if not new_files:
            print("ℹ️  No new files generated.")
            return

        print(f"   Generated {len(new_files)} new files.")

        print("✍️ Writing new files...")
        writer = FileWriter(new_files)
        created = writer.write_all()
        print(f"   Created {len(created)} files.")

        # ----- Git: prepare branch and commit -----
        print("🚀 Preparing git branch...")
        remote_url = f"https://{self.token}@github.com/{self.repo}.git"
        self._run(f"git remote set-url origin {remote_url}")

        self._run("git stash push -m 'Auto-stash before evolution' 2>/dev/null || true")
        self._run(f"git checkout {self.base}")
        self._run(f"git pull origin {self.base}")
        self._run(f"git branch -D {self.head} 2>/dev/null || true")
        self._run(f"git push origin --delete {self.head} 2>/dev/null || true")
        self._run(f"git checkout -b {self.head}")

        self._run("git add .")
        title = f"Nova-X Self-Evolution: Added {len(created)} new capabilities"
        self._run(f'git commit -m "{title}"')
        self._run(f"git push -u origin {self.head}")

        # ----- Create PR -----
        body = "## Nova-X Self-Evolution\n\n"
        body += "Nova-X has designed and implemented new capabilities for herself:\n\n"
        for f in created:
            body += f"- `{f}`\n"
        body += "\n🤖 Generated autonomously by Nova-X using Groq reasoning."

        payload = json.dumps({"title": title, "body": body, "head": self.head, "base": self.base})
        curl_cmd = f'curl -s -X POST -H "Authorization: token {self.token}" -H "Accept: application/vnd.github.v3+json" https://api.github.com/repos/{self.repo}/pulls -d \'{payload}\''
        output = self._run(curl_cmd)
        try:
            resp = json.loads(output)
        except:
            raise Exception(f"Invalid response: {output}")
        if "html_url" in resp:
            print(f"🎉 Pull Request created: {resp['html_url']}")
        else:
            raise Exception(f"API error: {resp.get('message', output)}")

        self._run(f"git checkout {self.base}")
