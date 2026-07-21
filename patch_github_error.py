from pathlib import Path
import json

path = Path("cognition/patch_synthesis_engine_v2.py")
text = path.read_text()

old = '''        if "html_url" in resp:
            return resp["html_url"]
        elif "message" in resp:
            raise Exception(f"GitHub API error: {resp['message']}")
        else:
            raise Exception(f"Unexpected response: {resp}")'''

new = '''        if "html_url" in resp:
            return resp["html_url"]
        elif "message" in resp:
            raise Exception(
                "GitHub API response:\\n"
                + json.dumps(resp, indent=2)
            )
        else:
            raise Exception(
                "Unexpected GitHub response:\\n"
                + json.dumps(resp, indent=2)
            )'''

if old not in text:
    print("❌ Expected code block not found.")
    raise SystemExit(1)

path.write_text(text.replace(old, new))
print("✅ Patch applied successfully.")
