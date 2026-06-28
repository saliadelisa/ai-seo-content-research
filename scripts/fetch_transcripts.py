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
        "title": "SEO In The Age of AI Expert Insights from Kevin Indig",
        "url": "https://www.youtube.com/watch?v=gFqNOCWbF-4"
    },
    {
        "expert": "kevin-indig",
        "title": "Preparing for Organic Growth in 2025 AirOps and Kevin Indig",
        "url": "https://www.youtube.com/watch?v=Vt_C1pEfNd8"
    },
    {
        "expert": "aleyda-solis",
        "title": "Crawling Mondays AI SEO Prompts and Workflows",
        "url": "https://www.youtube.com/watch?v=FceqAiMTE5M"
    },
    {
        "expert": "kyle-roof",
        "title": "Does AI Content Actually Rank on Google",
        "url": "https://www.youtube.com/watch?v=8SGwUFPPBjE"
    },
    {
        "expert": "gael-breton",
        "title": "AI Content Production at Scale Authority Hacker",
        "url": "https://www.youtube.com/watch?v=4ZtFkbSaFCo"
    },
    {
        "expert": "wil-reynolds",
        "title": "How AI Is Changing SEO Agency Work",
        "url": "https://www.youtube.com/watch?v=9jXQFhGKMfA"
    },
    {
        "expert": "surfer-seo",
        "title": "Surfer AI Full Content Workflow Tutorial",
        "url": "https://www.youtube.com/watch?v=PdPV5GBxYQo"
    },
]


def extract_video_id(url):
    patterns = [r"v=([a-zA-Z0-9_-]{11})", r"youtu\.be/([a-zA-Z0-9_-]{11})"]
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
    text = "\n".join(s.get("text", "") for s in segments) if isinstance(segments, list) else segments
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