#!/usr/bin/env python3
"""Download all images from Squarespace XML export, organized by gallery/page."""

import xml.etree.ElementTree as ET
import urllib.request
import os
import re
import time
from pathlib import Path

XML_FILE = "/Users/SamWolson/Desktop/Website/Squarespace-Wordpress-Export-06-20-2026.xml"
OUTPUT_DIR = "/Users/SamWolson/Desktop/Website/images"

NS = {
    "content": "http://purl.org/rss/1.0/modules/content/",
    "wp": "http://wordpress.org/export/1.2/",
    "excerpt": "http://wordpress.org/export/1.2/excerpt/",
    "dc": "http://purl.org/dc/elements/1.1/",
}

def slugify(name):
    name = name.strip().lower()
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[\s_]+", "-", name)
    return name

def extract_img_urls(html):
    return re.findall(r'src="(http://images\.squarespace-cdn\.com/[^"]+)"', html or "")

def download(url, dest):
    if dest.exists():
        return "skip"
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            dest.write_bytes(resp.read())
        return "ok"
    except Exception as e:
        return f"err: {e}"

def main():
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    channel = root.find("channel")

    # Map attachment URL -> filename from wp:post_name
    attachment_names = {}
    for item in channel.findall("item"):
        post_type = item.findtext("wp:post_type", namespaces=NS)
        if post_type == "attachment":
            url = item.findtext("wp:attachment_url", namespaces=NS)
            post_name = item.findtext("wp:post_name", namespaces=NS, default="")
            if url:
                attachment_names[url] = post_name

    # Collect pages with their images
    pages = []
    for item in channel.findall("item"):
        post_type = item.findtext("wp:post_type", namespaces=NS)
        status = item.findtext("wp:status", namespaces=NS)
        if post_type == "page" and status == "publish":
            title = item.findtext("title") or "untitled"
            encoded = item.find("content:encoded", NS)
            html = encoded.text if encoded is not None else ""
            urls = extract_img_urls(html)
            if urls:
                pages.append((title, urls))

    total = sum(len(u) for _, u in pages)
    print(f"Found {len(pages)} galleries, {total} images total\n")

    downloaded = skipped = errors = 0

    for title, urls in pages:
        folder = Path(OUTPUT_DIR) / slugify(title)
        folder.mkdir(parents=True, exist_ok=True)
        print(f"[{title}] → {folder.name}/ ({len(urls)} images)")

        for url in urls:
            # Derive filename from URL or attachment name
            filename = attachment_names.get(url, "")
            if filename:
                ext = Path(url).suffix or ".jpg"
                filename = filename.replace("-JPG", "").replace("-jpg", "") + ext
            else:
                filename = Path(url).name.split("?")[0]

            result = download(url, folder / filename)
            if result == "ok":
                downloaded += 1
                print(f"  ✓ {filename}")
            elif result == "skip":
                skipped += 1
            else:
                errors += 1
                print(f"  ✗ {filename}: {result}")
            time.sleep(0.05)  # be polite

    print(f"\nDone: {downloaded} downloaded, {skipped} skipped, {errors} errors")

if __name__ == "__main__":
    main()
