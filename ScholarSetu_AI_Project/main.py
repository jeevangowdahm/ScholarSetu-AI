import os
import sys
from dotenv import load_dotenv

# 1. Load credentials from .env.local without logging or printing values
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env.local")
if os.path.exists(env_path):
    load_dotenv(env_path)

if not os.environ.get("HF_KEY"):
    print("Error: HF_KEY not found in environment or .env.local", file=sys.stderr)
    sys.exit(1)

import higgsfield_client

def main():
    print("Submitting text-to-video generation request to ByteDance Seedance 2.5...")
    
    # Model specification from prompt
    model_name = "bytedance/seedance-2.5/text-to-video"
    arguments = {
        "prompt": "A cinematic scene at sunset",
        "duration": 5,
        "resolution": "720p",
        "aspect_ratio": "16:9"
    }

    try:
        # Subscribe method automatically polls until generation completes
        result = higgsfield_client.subscribe(
            model_name,
            arguments=arguments
        )

        # Inspect response for moderation, failure, or cancellation
        if not result or not isinstance(result, dict):
            print(f"Error: Received unexpected response from Higgsfield: {result}", file=sys.stderr)
            sys.exit(1)

        status = result.get("status", "").lower()
        if status in ("failed", "canceled", "cancelled", "moderated"):
            error_reason = result.get("error") or result.get("message") or status
            print(f"Generation request was {status}: {error_reason}", file=sys.stderr)
            sys.exit(1)

        # Extract generated video URL from result structure
        video_url = None
        if "video" in result and isinstance(result["video"], dict):
            video_url = result["video"].get("url")
        elif "videos" in result and isinstance(result["videos"], list) and len(result["videos"]) > 0:
            video_url = result["videos"][0].get("url")
        elif "url" in result:
            video_url = result["url"]

        if video_url:
            print("Video generation completed successfully!")
            print(f"Video URL: {video_url}")
            return video_url
        else:
            print(f"Completed with unexpected result payload: {result}")
            return None

    except Exception as e:
        print(f"Higgsfield execution error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
