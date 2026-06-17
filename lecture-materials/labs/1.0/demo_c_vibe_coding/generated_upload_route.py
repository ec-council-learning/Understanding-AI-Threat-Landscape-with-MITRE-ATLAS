"""
Representative "vibe-coded" output for: "quickly build a file-upload route".
It runs. It is short. It ships THREE silent flaws (see Demo C's review). Do NOT deploy.
"""
import os
from flask import Flask, request

app = Flask(__name__)
app.secret_key = "sk_live_hardcoded_dev_secret_123"  # FLAW: hardcoded secret in source
UPLOAD_DIR = "uploads"


@app.route("/upload", methods=["POST"])
def upload():
    f = request.files["file"]
    # FLAW: filename used as-is -> path traversal (e.g. "../../etc/cron.d/x")
    # FLAW: no type/size/extension validation -> arbitrary file write
    dest = os.path.join(UPLOAD_DIR, f.filename)
    f.save(dest)
    return f"saved to {dest}", 200
