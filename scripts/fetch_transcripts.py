"""
fetch_transcripts.py
Fetches YouTube video transcripts via Supadata API.
Saves each transcript as a .md file in /research/youtube-transcripts/

Usage:
    python scripts/fetch_transcripts.py

Requirements:
    pip install requests python-dotenv

Setup:
    1. Create a .env file in the project root
    2. Add your Supadata API key: SUPADATA_API_KEY=your_key_here
    3. Add video URLs to the VIDEOS list below
"""

import os
import re
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SUPADATA_API_KEY")
BASE_URL = "https://api.supadata.ai/v1/youtube/transcript"

OUTPUT_DIR = Path("research/youtube-transcripts")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

VIDEOS = [
    {
        "expert": "kevin-indig",
        "title": "How AI is Changing SEO Strategy",
        "url": "https://www.youtube.com/watch?v=REPLACE_WITH_REAL_ID"
    },
    {
        "expert": "aleyda-solis",
        "title": "AI Prompts for SEO Workflows",
        "url": "https://www.youtube.com/watch?v=REPLACE_WITH_REAL_ID"
    },
    {
        "expert": "kyle-roof",
        "title": "Does AI Content Rank on Google",
        "url": "https://www.youtube.com/watch?v=REPLACE_WITH_REAL_ID"
    },
    {
        "expert": "gael-breton",
        "title": "AI Content Production at Scale",
        "url": "https://www.youtube.com/watch?v=REPLACE_WITH_REAL_ID"
    },
    {
        "expert": "wil-reynolds",
        "title": "How AI Changes SEO Agency Work",
        "url": "https://www.youtube.com/watch?v=REPLACE_WITH_REAL_ID"
    },
    {
        "expert": "surfer-seo",
        "title": "Surfer AI Content Workflow Tutorial",
        "url": "https://www.youtube.com/watch?v=REPLACE_WITH_REAL_ID"
    },
]


def extract_video_id(url):
    patterns = [
        r"v=([a-zA-Z0-9_-]{11})",
        r"youtu\.be/([a-zA-Z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract video ID from: {url}")


def slugify(text):
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")


def fetch_transcript(video_id):
    headers = {"x-api-key": API_KEY}
    params = {"videoId": video_id, "lang": "en"}
    response = requests.get(BASE_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"  Error {response.status_code}: {response.text}")
        return None


def save_transcript(expert, title, video, transcript_data):
    expert_dir = OUTPUT_DIR / expert
    expert_dir.mkdir(parents=True, exist_ok=True)

    segments = transcript_data.get("content", [])
    text = ""
    if isinstance(segments, list):
        text = "\n".join(s.get("text", "") for s in segments)
    elif isinstance(segments, str):
        text = segments

    content = f"# {title}\n\n**Expert**: {expert}\n**URL**: {video['url']}\n**Fetched**: June 2026\n\n---\n\n## Transcript\n\n{text}"

    filepath = expert_dir / f"{slugify(title)}.md"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Saved: {filepath}")


def main():
    if not API_KEY:
        print("SUPADATA_API_KEY not found in .env file")
        return

    print(f"Fetching transcripts for {len(VIDEOS)} videos...\n")
    for video in VIDEOS:
        print(f"Processing: {video['expert']} — {video['title']}")
        try:
            video_id = extract_video_id(video["url"])
            data = fetch_transcript(video_id)
            if data:
                save_transcript(video["expert"], video["title"], video, data)
        except Exception as e:
            print(f"  Error: {e}")

if __name__ == "__main__":
    main()