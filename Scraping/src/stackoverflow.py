import requests
from bs4 import BeautifulSoup


URL = f"https://stackoverflow.com/jobs?q=python"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pages[-2].get_text().strip()
    return int(last_page)


def extract_job(html):
    title = html.find("div", {"class": "fl1"}).find("a")["title"]

    company = html.find("div", {"class": "fl1"}).find("h3").find("span")
    company = " ".join(list(company.stripped_strings))

    location = (
        html.find("div", {"class": "fl1"})
        .find("h3")
        .find_all("span", recursive=False)[-1]
    ).string.strip()

    job_id = html["data-jobid"]

    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"https://stackoverflow.com/jobs/{job_id}",
    }


def get_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scraping page from stackoverflow: {page + 1} / {last_page}")
        result = requests.get(f"{URL}&pg={page + 1}")
        soup = BeautifulSoup(result.text, "html.parser")
        divs = soup.find_all("div", {"class": "-job"})
        for div in divs:
            jobs.append(extract_job(div))
    return jobs


def get_stackoverflow_jobs():
    last_page = get_last_page()
    jobs = get_jobs(last_page)
    return jobs