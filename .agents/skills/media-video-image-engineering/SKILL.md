---
name: media-video-image-engineering
description: Processing video, audio, and images for web applications. Covers FFmpeg CLI, WebP/AVIF compression, responsive image optimization, and generative media prompts.
---

# Media Video & Image Engineering Skill

## 1. Image Optimization
- Modern web formats: Convert legacy JPEG/PNG assets to WebP or AVIF for 40-70% file size reduction.
- Responsive image syntax: Use `<picture>` with `srcset` and `sizes` to serve resolution-matched assets.

## 2. Video Processing with FFmpeg
- Web-optimized H.264 video with fast-start streaming flag:
  ```bash
  ffmpeg -i input.mov -c:v libx264 -crf 23 -preset medium -movflags +faststart -c:a aac -b:a 128k output.mp4
  ```
- Poster frame extraction:
  ```bash
  ffmpeg -ss 00:00:01 -i input.mp4 -vframes 1 -q:v 2 poster.jpg
  ```
