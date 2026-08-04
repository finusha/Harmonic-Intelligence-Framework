
import os
import json
import requests
from datetime import datetime
from pathlib import Path

API_KEY = os.getenv("LASTFM_API_KEY")

URL = (
    "https://ws.audioscrobbler.com/2.0/"
    f"?method=chart.gettoptracks&api_key={API_KEY}&format=json&limit=20"
)

response = requests.get(URL, timeout=30)
response.raise_for_status()

tracks = response.json()["tracks"]["track"]

today = datetime.utcnow().strftime("%Y-%m-%d")

Path("archive").mkdir(exist_ok=True)

snapshot = {
    "generated_at": datetime.utcnow().isoformat() + "Z",
    "tracks": tracks,
}

with open("latest.json", "w", encoding="utf-8") as f:
    json.dump(snapshot, f, indent=2)

with open(f"archive/{today}.json", "w", encoding="utf-8") as f:
    json.dump(snapshot, f, indent=2)

readme = f"""# 🎵 Harmonic Intelligence Framework (HIF)

An autonomous framework that monitors global music trends using the Last.fm API.

## Latest Snapshot

Generated: {today}

| Rank | Track | Artist | Listeners |
|------|-------|--------|----------|
"""

for i, track in enumerate(tracks, start=1):
    readme += (
        f"| {i} | {track['name']} | {track['artist']['name']} | "
        f"{track['listeners']} |\n"
    )

readme += """

---

Data Source: Last.fm API

Automation: GitHub Actions
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)

print("README and snapshot generated successfully.")
