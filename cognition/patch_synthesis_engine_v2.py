#!/usr/bin/env python3
"""
============================================================
NOVA-X Patch Synthesis Engine v2.1 — curl-based GitHub
============================================================

Features:
  - Scans codebase for issues
  - Generates unified diffs
  - Creates GitHub Pull Requests using `curl` (no extra libs)
"""

import os
import re
import json
import uuid
import subprocess
from pathlib import Path
from datetime import datetime, UTC
from typing import List, Dict, Any, Optional

# ============================================================
# Configuration
# ============================================================

SCAN_DIRS = ["cognition", "core", "modules", "utils", "scripts", "self_evolution"]
FILE_EXTENSIONS = [".py"]
REPORT_DIR = Path("self_evolution/reports")
OUTPUT_DIR = Path("data/patches")
REPORT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO = os.environ.get("GITHUB_REPO", "")  # e.g., "DOUGLASDAVIS08161978/nova_x"
GITHUB_BRANCH = os.environ.get("GITHUB_BRANCH", "nova-x-auto-patch")


# ============================================================
# Codebase Scanner (unchanged)
# ============================================================

class CodebaseScanner:
    def __init__(self, root_dir: Path = Path("."), scan_dirs: List[str] = None):
        self.root = root_dir.resolve()
        self.scan_dirs = scan_dirs or SCAN_DIRS
        self.files = []

    def scan(self) -> List[Path]:
        self.files = []
        for sub in self.scan_dirs:
            target = self.root / sub
            if not target.exists():
                continue
            for path in target.rglob("*"):
                if path.suffix in FILE_EXTENSIONS and path.is_file():
                    self.files.append(path)
        return self.files

    def analyze_file(self, filepath: Path) -> Dict[str, Any]:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        lines = content.splitlines()
        issues = []
        if not re.search(r'^("""|\'\'\')', content, re.MULTILINE):
            issues.append({"type": "MISSING_MODULE_DOCSTRING", "line": 1})
        for match in re.finditer(r'^def\s+(\w+)\s*\(', content, re.MULTILINE):
            line_num = content[:match.start()].count('\n') + 1
            start_idx = match.end()
            end_idx = min(start_idx + 500, len(content))
            block = content[start_idx:end_idx]
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

    def analyze_all(self) -> Dict[str, Any]:
        self.scan()
        results = []
        total_issues = 0
        for f in self.files:
            analysis = self.analyze_file(f)
            results.append(analysis)
            total_issues += analysis["total_issues"]
        return {"timestamp": datetime.now(UTC).isoformat(), "total_files": len(self.files), "total_issues": total_issues, "files": results}


# ============================================================
# Diff Generator (unchanged)
# ============================================================

class DiffGenerator:
    def __init__(self):
        self.transformations = {
            "MISSING_MODULE_DOCSTRING": self._add_module_docstring,
            "MISSING_FUNCTION_DOCSTRING": self._add_function_docstring,
            "MISSING_TYPE_HINTS": self._add_type_hints,
            "LONG_FUNCTION": self._suggest_split,
        }

    def _add_module_docstring(self, content: str, issue: Dict) -> str:
        docstring = '"""\nModule: {}\nAuto-generated by Nova-X Patch Engine.\n"""\n'.format(
            Path(issue.get("path", "unknown")).stem
        )
        lines = content.splitlines()
        if lines and lines[0].startswith("#!"):
            shebang = lines[0] + "\n"
            rest = "\n".join(lines[1:])
            return shebang + docstring + rest
        return docstring + content

    def _add_function_docstring(self, content: str, issue: Dict) -> str:
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

    def _add_type_hints(self, content: str, issue: Dict) -> str:
        # Placeholder: add a comment suggesting type hints
        func_name = issue["function"]
        pattern = r'(^def\s+' + re.escape(func_name) + r'\s*\()([^)]*)(\))'
        return content  # No actual change for now

    def _suggest_split(self, content: str, issue: Dict) -> str:
        func_name = issue["function"]
        pattern = r'(^def\s+' + re.escape(func_name) + r'\s*\([^)]*\)\s*:)'
        match = re.search(pattern, content, re.MULTILINE)
        if not match:
            return content
        insert_pos = match.end()
        comment = '\n    # TODO: Consider splitting this long function ({} lines)'.format(issue.get("lines", 0))
        return content[:insert_pos] + comment + content[insert_pos:]

    def generate_patch(self, file_analysis: Dict) -> Optional[str]:
        filepath = Path(file_analysis["path"])
        if not filepath.exists():
            return None
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            original = f.read()
        modified = original
        for issue in file_analysis["issues"]:
            issue_type = issue["type"]
            if issue_type in self.transformations:
                modified = self.transformations[issue_type](modified, issue)
        if modified == original:
            return None
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(original)
            orig_path = f.name
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(modified)
            new_path = f.name
        diff_cmd = ['diff', '-u', orig_path, new_path]
        result = subprocess.run(diff_cmd, capture_output=True, text=True)
        diff_text = result.stdout
        os.unlink(orig_path)
        os.unlink(new_path)
        return diff_text if diff_text else None


# ============================================================
# curl-based GitHub Pull Request Creator
# ============================================================

class GitHubCurlPR:
    def __init__(self, token: str, repo: str, base_branch: str = "main"):
        self.token = token
        self.repo = repo
        self.base_branch = base_branch
        self.head_branch = GITHUB_BRANCH
        self.api_base = "https://api.github.com"
        self.repo_api = f"{self.api_base}/repos/{repo}"

    def _curl_request(self, method: str, endpoint: str, data: Optional[dict] = None) -> dict:
        url = f"{self.repo_api}/{endpoint.lstrip('/')}"
        cmd = ["curl", "-s", "-X", method, "-H", f"Authorization: token {self.token}", "-H", "Accept: application/vnd.github.v3+json"]
        if data:
            cmd += ["-d", json.dumps(data)]
        cmd += [url]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"curl failed: {result.stderr}")
        try:
            return json.loads(result.stdout)
        except:
            raise Exception(f"Invalid JSON response: {result.stdout}")

    def create_pr(self, title: str, body: str) -> str:
        # Check if head branch exists, if not create it (simplified)
        # We'll just create the PR with the head branch; assume it exists or will be created.
        # Optionally, we could create a commit but for now we'll just create a PR with the diff in the body.
        data = {
            "title": title,
            "body": body,
            "head": self.head_branch,
            "base": self.base_branch
        }
        resp = self._curl_request("POST", "/pulls", data)
        if "html_url" in resp:
            return resp["html_url"]
        elif "message" in resp:
            raise Exception(
                "GitHub API response:\n"
                + json.dumps(resp, indent=2)
            )
        else:
            raise Exception(
                "Unexpected GitHub response:\n"
                + json.dumps(resp, indent=2)
            )

    def create_pr_from_patches(self, patches: Dict[str, str], title: str, description: str) -> str:
        body = description + "\n\nPatches:\n"
        for file_path, diff in patches.items():
            body += f"\n### {file_path}\n```diff\n{diff}\n```\n"
        return self.create_pr(title, body)


# ============================================================
# Enhanced Engine (with curl)
# ============================================================

class EnhancedPatchSynthesisEngine:
    def __init__(self):
        self.scanner = CodebaseScanner()
        self.diff_gen = DiffGenerator()
        self.github = None
        if GITHUB_TOKEN and GITHUB_REPO:
            self.github = GitHubCurlPR(GITHUB_TOKEN, GITHUB_REPO)
            print("✅ GitHub integration enabled (using curl).")
        else:
            print("ℹ️  GitHub integration not configured; patches saved locally.")

    def run(self):
        print("🔍 Scanning codebase...")
        analysis = self.scanner.analyze_all()
        print(f"   Found {analysis['total_files']} files, {analysis['total_issues']} issues.")

        patches = {}
        for file_data in analysis["files"]:
            if file_data["total_issues"] > 0:
                diff = self.diff_gen.generate_patch(file_data)
                if diff:
                    patches[file_data["path"]] = diff

        if not patches:
            print("No patches generated.")
            return

        patch_id = str(uuid.uuid4())
        patch_info = {
            "patch_id": patch_id,
            "generated": datetime.now(UTC).isoformat(),
            "status": "PROPOSED",
            "total_files_patched": len(patches),
            "patches": patches
        }
        patch_file = OUTPUT_DIR / f"{patch_id}.json"
        with open(patch_file, "w") as f:
            json.dump(patch_info, f, indent=4)

        print(f"✅ Patch JSON saved: {patch_file}")

        if self.github:
            title = f"Nova-X Auto Patch: {len(patches)} files improved"
            description = f"Auto-generated by Nova-X Patch Engine.\nPatch ID: {patch_id}\n\nImprovements:\n"
            for issue_type in ["MISSING_MODULE_DOCSTRING", "MISSING_FUNCTION_DOCSTRING", "MISSING_TYPE_HINTS", "LONG_FUNCTION"]:
                count = sum(1 for f in analysis["files"] for i in f["issues"] if i["type"] == issue_type)
                if count:
                    description += f"- {issue_type}: {count} instances\n"
            try:
                pr_url = self.github.create_pr_from_patches(patches, title, description)
                print(f"🎉 Pull Request created: {pr_url}")
            except Exception as e:
                print(f"❌ Failed to create PR: {e}")
        else:
            print("ℹ️  Patches saved locally — GitHub integration not active.")

if __name__ == "__main__":
    engine = EnhancedPatchSynthesisEngine()
    engine.run()
