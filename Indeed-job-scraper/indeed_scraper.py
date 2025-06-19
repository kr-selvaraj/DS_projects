import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Configuration
SEARCH = "software+engineer"
LOCATION = "India"
PAGES = 3  # How many pages to scrape

# Updated headers to avoid 403 errors
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Connection": "keep-alive"
}

# Data lists
job_titles = []
companies = []
locations = []

for page in range(PAGES):
    url = f"https://in.indeed.com/jobs?q={SEARCH}&l={LOCATION}&start={page*10}"
    print(f"Scraping Page {page+1}: {url}")
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 403:
        print("403 Forbidden — Try reducing request frequency or switching IP.")
        break

    soup = BeautifulSoup(response.text, "html.parser")
    job_cards = soup.find_all("div", class_="job_seen_beacon")

    if not job_cards:
        print("No job cards found — structure may have changed.")
        continue

    for job in job_cards:
        title_elem = job.find("h2", class_="jobTitle")
        company_elem = job.find("span", class_="companyName")
        location_elem = job.find("div", class_="companyLocation")

        job_titles.append(title_elem.text.strip() if title_elem else "N/A")
        companies.append(company_elem.text.strip() if company_elem else "N/A")
        locations.append(location_elem.text.strip() if location_elem else "N/A")

    time.sleep(2)  # Polite wait between requests

# Build DataFrame
df = pd.DataFrame({
    "Job Title": job_titles,
    "Company": companies,
    "Location": locations
})

# Remove duplicates and save
df.drop_duplicates(inplace=True)
df.to_csv("indeed_jobs_mar2024.csv", index=False)
print("Scraping complete. Saved to indeed_jobs_mar2024.csv")
