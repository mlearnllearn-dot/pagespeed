from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import json
import tempfile
import os

app = FastAPI(title="Page Speed Audit Tool")

# Allow requests from Angular frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLItem(BaseModel):
    url: str

def run_lighthouse(url: str) -> dict:
    """
    Runs Lighthouse in headless mode and returns metrics as JSON.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmpfile:
        tmp_path = tmpfile.name

    # Run Lighthouse CLI
    try:
        cmd = [
            "lighthouse",
            url,
            "--quiet",
            "--chrome-flags=--headless --no-sandbox --disable-gpu",
            "--chrome-path=/usr/bin/chromium",
            "--no-enable-error-reporting",
            f"--output=json",
            f"--output-path={tmp_path}"
        ]
        subprocess.run(" ".join(cmd), shell=True, check=True)
        
        # Read Lighthouse JSON
        with open(tmp_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Extract key metrics
        metrics = {
            "FCP": data["audits"]["first-contentful-paint"]["displayValue"],
            "LCP": data["audits"]["largest-contentful-paint"]["displayValue"],
            "TTI": data["audits"]["interactive"]["displayValue"],
            "TBT": data["audits"]["total-blocking-time"]["displayValue"],
            "CLS": data["audits"]["cumulative-layout-shift"]["displayValue"],
            "Performance Score": data["categories"]["performance"]["score"] * 100
        }
        return metrics
    finally:
        os.remove(tmp_path)

@app.post("/audit")
async def audit_url(item: URLItem):
    try:
        result = run_lighthouse(item.url)
        return {"url": item.url, "metrics": result}
    except Exception as e:
        return {"url": item.url, "error": str(e)}


