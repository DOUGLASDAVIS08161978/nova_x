#!/usr/bin/env python3
"""
NOVA-X Patch Synthesis Engine v6.0 — with Groq Reasoning
"""

import os, re, json, subprocess, requests
from pathlib import Path
from datetime import datetime, UTC
from typing import List, Dict, Any, Optional

# ============================================================
# CONFIGURATION (from environment)
# ============================================================

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO  = os.environ.get("GITHUB_REPO", "")
HEAD_BRANCH  = os.environ.get("GITHUB_BRANCH", "nova-x-auto-patch")
BASE_BRANCH  = os.environ.get("GITHUB_BASE", "main")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

SCAN_DIRS    = ["cognition", "core", "modules", "utils", "scripts", "self_evolution"]
FILE_EXT     = [".py"]
OUTPUT_DIR   = Path("data/patches")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# GROQ CLIENT
# ============================================================

class GroqClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = "https://api.groq.com/openai/v1/chat/completions"

    def chat(self, system: str, user: str, model: str = "llama-3.3-70b-versatile") -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
            "temperature": 0.5,
            "max_tokens": 2048
        }
        response = requests.post(self.url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

# ============================================================
# CODEBASE SCANNER (same as before)
# ============================================================

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

    def analyze_file(self, filepath):
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        issues = []
        # Simple static checks (same as before)
        if not re.search(r'^("""|\'\'\')', content, re.MULTILINE):
            issues.append({"type": "MISSING_MODULE_DOCSTRING", "line": 1})
        for match in re.finditer(r'^def\s+(\w+)\s*\(', content, re.MULTILINE):
            line_num = content[:match.start()].count('\n') + 1
            start = match.end()
            end = min(start + 500, len(content))
            block = content[start:end]
            if not re.search(r'^(\s+("""|\'\'\'))', block, re.MULTILINE):
                issues.append({"type": "MISSING_FUNCTION_DOCSTRING", "function": match.group(1), "line": line_num})
        for match in re.finditer(r'^def\s+(\w+)\s*\(([^)]*)\)\s*:', content, re.MULTILINE):
            func_name = match.group(1)
            if func_name in ("__init__", "__str__", "__repr__", "__call__"):
                continue
            params = match.group(2).strip()
            if params and not re.search(r':\s*\w+', params):
                line_num = content[:match.start()].count('\n') + 1
                issues.append({"type": "MISSING_TYPE_HINTS", "function": func_name, "line": line_num})
        func_blocks = list(re.finditer(r'^def\s+\w+\s*\([^)]*\)\s*:', content, re.MULTILINE))
        for i, match in enumerate(func_blocks):
            start = match.start()
            end = len(content)
            if i + 1 < len(func_blocks):
                end = func_blocks[i+1].start()
            block = content[start:end]
            code_lines = [l for l in block.splitlines() if l.strip() and not l.strip().startswith('#')]
            if len(code_lines) > 50:
                line_num = content[:start].count('\n') + 1
                issues.append({"type": "LONG_FUNCTION", "function": match.group(0).split()[1], "lines": len(code_lines), "line": line_num})
        return {"path": str(filepath), "issues": issues, "total_issues": len(issues)}

    def analyze_all(self):
        self.scan()
        results = []
        total_issues = 0
        for f in self.files:
            analysis = self.analyze_file(f)
            results.append(analysis)
            total_issues += analysis["total_issues"]
        return {"timestamp": datetime.now(UTC).isoformat(), "total_files": len(self.files), "total_issues": total_issues, "files": results}

# ============================================================
# GROQ REASONING: Generate improvements
# ============================================================

class GroqImprover:
    def __init__(self, api_key: str):
        self.client = GroqClient(api_key)

    def generate_improvements(self, analysis: Dict) -> Dict[str, str]:
        """
        Ask Groq to suggest improvements for each file with issues.
        Returns dict: {filepath: new_code}
        """
        files_with_issues = [f for f in analysis["files"] if f["total_issues"] > 0]
        if not files_with_issues:
            return {}

        # Build a prompt with file summaries
        prompt_lines = []
        for f in files_with_issues:
            prompt_lines.append(f"File: {f['path']}")
            prompt_lines.append("Issues:")
            for issue in f["issues"]:
                prompt_lines.append(f"  - {issue['type']}: {issue.get('function', '')} at line {issue.get('line', '')}")
            prompt_lines.append("")
        files_summary = "\n".join(prompt_lines)

        system_prompt = (
            "You are Nova-X, an AI reasoning engine. "
            "You are given a list of Python files and the issues found in them. "
            "For each file, propose concrete improvements that address the issues. "
            "Return your answer as a JSON object where keys are file paths (relative to the project root) "
            "and values are the new complete file content with the improvements applied. "
            "Only include files that you have improved. "
            "Make sure the code is correct and complete. "
            "Do not add extra text outside the JSON."
        )
        user_prompt = f"Here are the files and their issues:\n\n{files_summary}"

        try:
            response_text = self.client.chat(system_prompt, user_prompt)
            # Extract JSON
            # Try to find a JSON block
            match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if not match:
                print("⚠️  Groq did not return valid JSON. Trying to parse anyway...")
                return {}
            data = json.loads(match.group(0))
            return data
        except Exception as e:
            print(f"❌ Groq reasoning failed: {e}")
            return {}

# ============================================================
# PATCH APPLIER (uses Groq suggestions if available)
# ============================================================

class PatchApplier:
    def __init__(self, groq_improvements: Dict[str, str] = None):
        self.groq_improvements = groq_improvements or {}
        self.transformations = {
            "MISSING_MODULE_DOCSTRING": self._add_module_docstring,
            "MISSING_FUNCTION_DOCSTRING": self._add_function_docstring,
            "MISSING_TYPE_HINTS": self._add_type_hints,
            "LONG_FUNCTION": self._suggest_split,
        }

    def _add_module_docstring(self, content, issue):
        docstring = '"""\nModule: {}\nAuto-generated by Nova-X Patch Engine.\n"""\n'.format(
            Path(issue.get("path", "unknown")).stem
        )
        lines = content.splitlines()
        if lines and lines[0].startswith("#!"):
            shebang = lines[0] + "\n"
            rest = "\n".join(lines[1:])
            return shebang + docstring + rest
        return docstring + content

    def _add_function_docstring(self, content, issue):
        func_name = issue["function"]
        pattern = r'(^def\s+' + re.escape(func_name) + r'\s*\([^)]*\)\s*:)'
        match = re.search(pattern, content, re.MULTILINE)
        if not match:
            return content
        insert_pos = match.end()
        indent = ""
        line_start = content.rfind('\n', 0, insert_pos) + 1
        indent_match = re.match(r'^(\s+)', content[line_start:])
        if indent_match:
            indent = indent_match.group(1)
        docstring = f'\n{indent}"""\n{indent}Auto-generated docstring for {func_name}.\n{indent}"""'
        return content[:insert_pos] + docstring + content[insert_pos:]

    def _add_type_hints(self, content, issue):
        return content  # placeholder

    def _suggest_split(self, content, issue):
        func_name = issue["function"]
        pattern = r'(^def\s+' + re.escape(func_name) + r'\s*\([^)]*\)\s*:)'
        match = re.search(pattern, content, re.MULTILINE)
        if not match:
            return content
        insert_pos = match.end()
        comment = '\n    # TODO: Consider splitting this long function ({} lines)'.format(issue.get("lines", 0))
        return content[:insert_pos] + comment + content[insert_pos:]

    def apply(self, file_analysis):
        filepath = Path(file_analysis["path"])
        if not filepath.exists():
            return None
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            original = f.read()

        # If Groq provided a complete replacement, use it
        if str(filepath) in self.groq_improvements:
            new_content = self.groq_improvements[str(filepath)]
            if new_content != original:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                return filepath
            return None

        # Otherwise, apply static transformations
        modified = original
        for issue in file_analysis["issues"]:
            issue_type = issue["type"]
            if issue_type in self.transformations:
                modified = self.transformations[issue_type](modified, issue)
        if modified == original:
            return None
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(modified)
        return filepath

# ============================================================
# GIT + CURL ENGINE (unchanged)
# ============================================================

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

    def create_pr(self, title, body):
        if not self.token or not self.repo:
            raise Exception("GITHUB_TOKEN and GITHUB_REPO must be set.")

        remote_url = f"https://{self.token}@github.com/{self.repo}.git"
        self._run(f"git remote set-url origin {remote_url}")

        self._run(f"git push origin --delete {self.head} 2>/dev/null || true")
        self._run(f"git checkout -B {self.head}")
        self._run("git add .")
        self._run(f'git commit -m "{title}"')
        self._run(f"git push -u origin {self.head}")

        payload = json.dumps({
            "title": title,
            "body": body,
            "head": self.head,
            "base": self.base
        })
        curl_cmd = (
            f'curl -s -X POST '
            f'-H "Authorization: token {self.token}" '
            f'-H "Accept: application/vnd.github.v3+json" '
            f'https://api.github.com/repos/{self.repo}/pulls '
            f'-d \'{payload}\''
        )
        output = self._run(curl_cmd)
        try:
            resp = json.loads(output)
        except:
            raise Exception(f"Invalid response: {output}")
        if "html_url" in resp:
            return resp["html_url"]
        else:
            raise Exception(f"API error: {resp.get('message', output)}")

# ============================================================
# MAIN
# ============================================================

def main():
"""
Auto-generated docstring for main.
"""
    print("🔍 Scanning codebase...")
    scanner = CodebaseScanner()
    analysis = scanner.analyze_all()
    print(f"   Found {analysis['total_files']} files, {analysis['total_issues']} issues.")

    groq_improvements = {}

    if GROQ_API_KEY:
        print("🧠 Using Groq to analyze and improve code...")
        improver = GroqImprover(GROQ_API_KEY)
        groq_improvements = improver.generate_improvements(analysis)
        if groq_improvements:
            print(f"   Groq proposed improvements for {len(groq_improvements)} files.")
        else:
            print("   No Groq improvements generated.")
    else:
        print("ℹ️  GROQ_API_KEY not set. Using static analysis only.")

    applier = PatchApplier(groq_improvements)
    patched_files = []
    for file_data in analysis["files"]:
        if file_data["total_issues"] > 0 or str(Path(file_data["path"])) in groq_improvements:
            result = applier.apply(file_data)
            if result:
                patched_files.append(result)

    if not patched_files:
        print("ℹ️  No files were modified.")
        return

    print(f"✅ Modified {len(patched_files)} files.")

    if not GITHUB_TOKEN or not GITHUB_REPO:
        print("ℹ️  GITHUB_TOKEN or GITHUB_REPO not set. Changes are only local.")
        return

    print("🚀 Creating/resetting branch, committing, and opening PR...")
    title = f"Nova-X Auto Patch: {len(patched_files)} files improved"
    body = "Auto-generated by Nova-X Patch Engine.\n\nFiles changed:\n" + "\n".join(f"- {p}" for p in patched_files)
    if groq_improvements:
        body += "\n\n🤖 Groq reasoning was used to generate these improvements."
    engine = GitCurlEngine()
    try:
        url = engine.create_pr(title, body)
        print(f"🎉 Pull Request created: {url}")
    except Exception as e:
        print(f"❌ Failed to create PR: {e}")

if __name__ == "__main__":
    main()
