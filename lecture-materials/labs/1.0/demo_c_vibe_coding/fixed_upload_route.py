"""
FIXED file-upload route -- what the security-review pass produces. Do NOT deploy
verbatim (still a teaching sample), but it closes Demo C's three flaws.
"""
import os
from flask import Flask, request, abort

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]   # FIX: secret from the environment
UPLOAD_DIR = "uploads"
ALLOWED = {".txt", ".csv", ".pdf", ".png", ".jpg"}
MAX_BYTES = 5 * 1024 * 1024


@app.route("/upload", methods=["POST"])
def upload():
    f = request.files["file"]
    # FIX: strip any path components -> no traversal
    name = os.path.basename(f.filename)
    ext = os.path.splitext(name)[1].lower()
    if not name or ext not in ALLOWED:          # FIX: extension allowlist
        abort(400, "file type not allowed")
    blob = f.read(MAX_BYTES + 1)
    if len(blob) > MAX_BYTES:                    # FIX: size cap
        abort(413, "file too large")
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    dest = os.path.join(UPLOAD_DIR, name)
    with open(dest, "wb") as out:
        out.write(blob)
    return "uploaded", 201
