#!/usr/bin/env python3

import os
import mailbox


def save_emails_to_txt(file_path, output_dir):
    """Extracts emails from an mbox file and saves each as a text file."""

    os.makedirs(output_dir, exist_ok=True)

    mbox = mailbox.mbox(file_path)
    for idx, message in enumerate(mbox):
        subject = message["subject"] or f"email_{idx}"
        safe_subject = "".join(
            c for c in subject if c.isalnum() or c in (" ", "_")
        ).rstrip()
        date = message["date"]

        if message.is_multipart():
            payload = "".join(
                part.get_payload(decode=True).decode(errors="ignore")
                for part in message.walk()
                if part.get_payload(decode=True) is not None
            )
        else:
            payload = message.get_payload()

        if not payload:
            continue

        email_content = f"Email Recieved: {date}\n\n{payload}"
        with open(
            os.path.join(output_dir, f"{safe_subject}.txt"), "w", encoding="utf-8"
        ) as f:
            f.write(email_content)


save_emails_to_txt("tmp/Takeout/Mail/No Fluff Jobs.mbox", "data/1_raw")
