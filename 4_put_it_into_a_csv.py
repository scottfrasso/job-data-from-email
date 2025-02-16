#!/usr/bin/env python3

import os
import json
import pandas as pd
from pydantic import BaseModel


class JobListing(BaseModel):
    job_title: str
    company: str
    minimum_salary: int | None
    maximum_salary: int | None
    currency: str
    technology: str | None
    primary_location_city: str
    primary_location_country: str | None
    remote: bool | None
    job_timestamp: str | None


def convert_currency_to_usd(amount, currency):
    exchange_rates = {"USD": 1, "EUR": 1.1, "PLN": 0.25, "GBP": 1.3}
    return amount * exchange_rates.get(currency, 1)


def process_job_files(folder_path, output_csv):
    all_jobs = []

    for filename in os.listdir(folder_path):
        with open(os.path.join(folder_path, filename), "r") as file:
            data = json.load(file)
            for job_data in data:
                job = JobListing(**job_data)
                all_jobs.append(job.model_dump())

    df = pd.DataFrame(all_jobs)

    if "job_timestamp" in df.columns:
        df["job_timestamp"] = pd.to_datetime(
            df["job_timestamp"], errors="coerce", utc=True
        ).dt.strftime("%Y-%m-%d")

    df.to_csv(output_csv, index=False)


# Example usage:
process_job_files("data/3_refined", "job_data.csv")
