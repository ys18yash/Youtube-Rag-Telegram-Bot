import re
from typing import List, Dict
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound


class TranscriptError(Exception):
    pass


def extract_video_id(url: str) -> str:
    parsed_url = urlparse(url)

    # Standard YouTube link
    if "youtube.com" in parsed_url.netloc:
        query_params = parse_qs(parsed_url.query)
        if "v" in query_params:
            return query_params["v"][0]

    # Short youtu.be link
    if "youtu.be" in parsed_url.netloc:
        return parsed_url.path.strip("/")

    raise TranscriptError("Invalid YouTube URL.")


def fetch_transcript(video_id: str) -> List[Dict]:
    try:
        ytt_api = YouTubeTranscriptApi()

        transcript_list = ytt_api.fetch(video_id)

        return [
            {
                "text": entry.text,
                "start": entry.start,
                "duration": entry.duration,
            }
            for entry in transcript_list
        ]

    except TranscriptsDisabled:
        raise TranscriptError("Transcripts are disabled for this video.")
    except NoTranscriptFound:
        raise TranscriptError("No transcript available for this video.")
    except Exception as e:
        raise TranscriptError(f"Failed to fetch transcript: {str(e)}")