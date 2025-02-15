import os
import json
from google import genai
from enum import StrEnum
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

# create client
client = genai.Client(
    vertexai=True,
    project="ai-web-scraper-444212",
    location="us-central1",
)


class SeniorityLevel(StrEnum):
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    STAFF = "staff"


class JobListing(BaseModel):
    job_title: str = Field(
        description="The title of the job listing",
    )
    company: str = Field(
        description="The company offering the job",
    )
    minimum_salary: int | None = Field(
        description="The starting salary for the job listing if there is one.",
    )
    maximum_salary: int | None = Field(
        description="The ending salary for the job listing if there is one.",
    )
    currency: str = Field(
        description="The currency in which the salary is offered.",
    )
    technology: str | None = Field(
        description="The technology or programming language required for the job.",
    )
    primary_location_city: str = Field(
        description="""
        Convert the name of the city into the common english language spelling of the city.
        Just the location of the job. (e.g., 'Warsaw', 'Kraków', 'Remote'). 
        Just pick the first if there's multiples.""",
    )
    primary_location_country: str | None = Field(
        description="""
        Convert the country into the common english language spelling of the country.
        The country where the job is located if you can determine it from the city.
        (e.g., 'Poland', 'Germany', 'United States'). 
        Just pick the first if there are multiples.""",
    )
    seniority: SeniorityLevel | None = Field(
        description="""
        The seniority level of the job (must be one of: 'junior', 'mid', 'senior', 'staff' or None).
        If it specifically says its a manager position use 'staff'.
        If there is no seniority level specified, use None.
        """,
    )
    remote: bool | None = Field(
        description="True if the job is listed as remote, False if the job is listed as on-site. None if the remote status is not specified.",
    )
    job_timestamp: str = Field(
        description="""
        Convert it to YYYY-MM-DD format.
        It will be at the top of the page like so: Email Recieved: Mon, 26 Jun 2023 07:57:55 +0000.
        """,
    )

    @field_validator("job_timestamp")
    def validate_timestamp(cls, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("job_timestamp must be in YYYY-MM-DD format")
        return value


input_dir = "/Users/scottfrasso/work/email-parser/data/2_processed/"
output_dir = "/Users/scottfrasso/work/email-parser/data/3_refined/"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    input_filepath = os.path.join(input_dir, filename)
    output_filepath = os.path.join(output_dir, filename)

    # Skip processing if the file has already been refined
    if os.path.exists(output_filepath) and os.path.getsize(output_filepath) > 0:
        print(f"Skipping {input_filepath} as it has already been processed.")
        continue

    # Read the content of the file
    with open(input_filepath, "r", encoding="utf-8") as file:
        text = file.read()

    print(f"Processing {input_filepath}...")

    # Generate a list of job listings
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite-preview-02-05",
        contents=f"Read the following text and generate a list of jobs with their salaries\n\n{text}",
        config={
            "response_mime_type": "application/json",
            "response_schema": list[JobListing],
        },
    )

    jobs = response.parsed

    # Check if jobs is iterable
    if not isinstance(jobs, list):
        print(
            f"Error: The response for {input_filepath} is not a list of job listings."
        )
        continue

    # Write the jobs to the output file
    with open(output_filepath, "w", encoding="utf-8") as file:
        json.dump([job.model_dump() for job in jobs], file, indent=4)
