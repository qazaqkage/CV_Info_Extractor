import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta


def scrape_jobs_from_web(query, location, output_file="jobs.csv"):
    """
    Scrape job postings from Indeed based on query and location.
    Save results as a CSV file.

    Args:
        query (str): Job title or keywords to search for.
        location (str): Desired job location.
        output_file (str): Path to save the job postings CSV.

    Returns:
        str: Path to the output CSV file.
    """
    url = f"https://www.indeed.com/jobs?q={query}&l={location}&fromage=7"  # Filter by last 7 days
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch jobs. HTTP Status: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    for job_card in soup.find_all('div', class_='job_seen_beacon'):
        # Extract job title
        title_tag = job_card.find('h2', {'class': 'jobTitle'})
        title = title_tag.text.strip() if title_tag else "N/A"

        # Extract company name
        company_tag = job_card.find('span', {'class': 'companyName'})
        company = company_tag.text.strip() if company_tag else "N/A"

        # Extract location
        location_tag = job_card.find('div', {'class': 'companyLocation'})
        job_location = location_tag.text.strip() if location_tag else "N/A"

        # Extract posting date (handle relative dates like "2 days ago")
        date_posted_tag = job_card.find('span', {'class': 'date'})
        if date_posted_tag:
            date_text = date_posted_tag.text.strip()
            if "day" in date_text:
                days_ago = int(date_text.split()[0])
                date_posted = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
            else:
                date_posted = datetime.now().strftime("%Y-%m-%d")  # Default to today if not clear
        else:
            date_posted = "N/A"

        jobs.append({
            'title': title,
            'company': company,
            'location': job_location,
            'date_posted': date_posted
        })

    # Save jobs to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['title', 'company', 'location', 'date_posted']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(jobs)

    print(f"Saved {len(jobs)} jobs to {output_file}")
    return output_file
