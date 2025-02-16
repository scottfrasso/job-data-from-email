#!/usr/bin/env python3

import os
from markdownify import markdownify
from bs4 import BeautifulSoup


def html_to_clean_markdown(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n\n")  # Extract plain text with new lines
    return markdownify(text)


raw_dir = "data/1_raw"
processed_dir = "data/2_processed"

if not os.path.exists(processed_dir):
    os.makedirs(processed_dir)

for filename in os.listdir(raw_dir):
    raw_filepath = os.path.join(raw_dir, filename)
    processed_filepath = os.path.join(processed_dir, filename)

    print(f"Processing {raw_filepath}...")

    with open(raw_filepath, "r") as f:
        html = f.read()

    markdown = html_to_clean_markdown(html)

    with open(processed_filepath, "w") as f:
        f.write(markdown)
