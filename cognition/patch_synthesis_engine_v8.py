#!/usr/bin/env python3
"""
NOVA-X Patch Synthesis Engine v8.6 — Fixed 400 error
"""

import os, re, json, subprocess, requests, time
from pathlib import Path
from datetime import datetime, UTC

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO  = os.environ.get("GITHUB_REPO", "")
HEAD_BRANCH  = os.environ.get("GITHUB_BRANCH", "nova-x-auto-patch")
BASE_BRANCH  = os.environ.get("GITHUB_BASE", "main")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

SCAN_DIRS    = ["cognition", "core", "modules", "utils", "scripts", "self_evolution"]
FILE_EXT     = [".py"]

# ---------- Groq Client ----------
class GroqClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = "https://api.groq.com/openai/v1/chat/completions"

    def chat(self, system: str, user: str, model: str = "llama-3.3-70b-versatile") -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        # Truncate user prompt if too long
        if len(user) > 4000:
            user = user[:4000] + "\n[truncated]"
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
            "temperature": 0.4,
            "max_tokens": 1500,
        }
        for attempt in range(3):
            try:
                resp = requests.post(self.url, json=payload, headers=headers, timeout=90)
                if resp.status_code == 429:
                    wait = (attempt + 1) * 5
                    print(f"   ⏳ Rate limit, waiting {wait}s...")
                    time.sleep(wait)
                    continue
                if resp.status_code != 200:
                    # Print full response for debugging
                    print(f"   ❌ HTTP {resp.status_code}: {resp.text[:300]}")
                    raise Exception(f"HTTP {resp.status_code}")
                return resp.json()["choices"][0]["message"]["content"]
            except Exception as e:
                if attempt == 2:
                    raise
                time.sleep(2)
        raise Exception("Max retries exceeded")

    def extract_json(self, text: str):
        # Remove markdown
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        # Try array
        match = re.search(r'\[[\s\S]*\]', text)
        if match:
            try:
                return json.loads(match.group(0))
            except:
                pass
        # Try object
        match = re.search(r'\{[\s\S]*\}', text)
        if match:
            try:
                return json.loads(match.group(0))
            except:
                pass
        # Try multiple objects
        objects = re.findall(r'\{[^{}]*\}', text)
        if len(objects) > 1:
            try:
                return json.loads("[" + ",".join(objects) + "]")
            except:
                pass
        # Fallback: use ast.literal_eval
        try:
            import ast
            return ast.literal_eval(text)
        except:
            raise ValueError("Could not parse JSON")

# ---------- Scanner ----------
class CodebaseScanner:
    def __init__(self):
        self.root = Path(".")

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

    def get_file_list(self):
        self.scan()
        lines = []
        for f in self.files[:20]:  # Only first 20 files to avoid token overflow
            try:
                with open(f, "r", encoding="utf-8", errors="ignore") as fp:
                    first = fp.readline().strip()[:60]
                lines.append(f"- {f} ({first})")
            except:
                lines.append(f"- {f}")
        return "\n".join(lines)

# ---------- Self-Evolution ----------
class SelfDirectedImprover:
    def __init__(self, api_key: str):
        self.client = GroqClient(api_key)
        self.scanner = CodebaseScanner()

    def generate_capabilities(self) -> dict:
        print("   📋 Building codebase summary...")
        file_list = self.scanner.get_file_list()

        print("   💭 Asking Groq for new capabilities...")
        system = (
            "You are Nova-X, an AI architect. Propose 3 new Python modules that would make Nova-X significantly more powerful. "
            "Return ONLY a JSON array: [{'name':'ModuleName','description':'...'}]"
        )
        user = f"Current codebase files:\n{file_list}\n\nPropose 3 new capabilities."

        try:
            response = self.client.chat(system, user)
            ideas = self.client.extract_json(response)
            if isinstance(ideas, dict):
                if "capabilities" in ideas:
                    ideas = ideas["capabilities"]
                elif "modules" in ideas:
                    ideas = ideas["modules"]
                else:
                    ideas = [{"name": k, "description": str(v)[:50]} for k, v in ideas.items()]
            if not isinstance(ideas, list):
                raise Exception("Not a list")
            for item in ideas:
                if "name" not in item:
                    item["name"] = f"capability_{ideas.index(item)}"
                if "description" not in item:
                    item["description"] = "New capability"
            print(f"   💡 Groq proposed {len(ideas)} capabilities.")
        except Exception as e:
            print(f"   ❌ Failed to get ideas: {e}")
            return {}

        new_files = {}
        for idea in ideas:
            name = idea["name"]
            desc = idea["description"]
            print(f"   🔧 Generating code for: {name}...")
            code_prompt = (
                f"Write a Python module for '{name}'.\n"
                f"Description: {desc}\n"
                f"Create a class '{name}' with __init__ and run methods.\n"
                f"Include docstrings, type hints, error handling.\n"
                f"Return ONLY the Python code, no markdown."
            )
            try:
                code = self.client.chat(
                    "You are an expert Python developer. Generate clean, working code.",
                    code_prompt,
                    model="llama-3.1-8b-instant"
                )
                code = self._clean_code(code)
                if code:
                    clean_name = name.replace(" ", "_").lower()
                    filename = f"modules/{clean_name}.py"
                    new_files[filename] = code
                    print(f"   ✅ Generated {filename}")
            except Exception as e:
                print(f"   ❌ Failed to generate {name}: {e}")

        return new_files

    def _clean_code(self, text: str) -> str:
        text = re.sub(r'```python\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        text = text.strip()
        if not text or len(text) < 30:
            return None
        return text

# ---------- Git Engine ----------
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
            print("❌ GROQ_API_KEY not set.")
            return

        print("🧠 Nova-X is thinking about what new capabilities to add...")
        improver = SelfDirectedImprover(GROQ_API_KEY)
        new_files = improver.generate_capabilities()

        if not new_files:
            print("ℹ️  No new files generated.")
            return

        print(f"   Generated {len(new_files)} new files.")

        print("✍️ Writing new files...")
        for path_str, content in new_files.items():
            filepath = Path(path_str)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
        created = list(new_files.keys())
        print(f"   Created {len(created)} files.")

        print("🚀 Preparing git branch...")
        remote_url = f"https://{self.token}@github.com/{self.repo}.git"
        self._run(f"git remote set-url origin {remote_url}")

        # Stash everything, switch to main, pull, create branch
        self._run("git stash --include-untracked 2>/dev/null || true")
        self._run(f"git checkout {self.base}")
        self._run(f"git pull origin {self.base}")
        self._run(f"git branch -D {self.head} 2>/dev/null || true")
        self._run(f"git push origin --delete {self.head} 2>/dev/null || true")
        self._run(f"git checkout -b {self.head}")

        # Restore stashed files
        self._run("git stash pop 2>/dev/null || true")

        self._run("git add .")
        title = f"Nova-X Self-Evolution: Added {len(created)} new capabilities"
        self._run(f'git commit -m "{title}"')
        self._run(f"git push -u origin {self.head}")

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
