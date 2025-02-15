# I pulled job data from my inbox to see if there was a trend

## Set up

1. install uv

2. Install dependencies & set up the venv

```
uv sync

uv venv

source .venv/bin/activate
```

3. Auth to GCP so you can use Gemini (you have to enable Vertex AI)

```bash
gcloud auth application-default login
```

## How I ran this (you probably shouldn't becuase you don't have the data in your gmail.)

1. Put the mbox from Google Takeout here `tmp/Takeout/Mail/No Fluff Jobs.mbox`

2. `python3 1_pull_out_text_from_mbox.py`

3.
