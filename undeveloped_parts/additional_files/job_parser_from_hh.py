import requests

# HeadHunter API Constants
BASE_URL = "https://api.hh.ru/vacancies"
HEADERS = {"User-Agent": "JobParser/1.0"}


# Function to fetch vacancies
def fetch_vacancies(area, per_page=10):
    """
    Fetch 10 vacancies from the specified area.
    """
    params = {
        "area": area,
        "per_page": per_page,
        "page": 0
    }
    response = requests.get(BASE_URL, headers=HEADERS, params=params)
    if response.status_code == 200:
        return response.json()["items"]
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")


# Parse vacancies
def parse_vacancies(vacancies):
    """
    Parse the fetched vacancies to extract essential fields.
    """
    parsed = []
    for vacancy in vacancies:
        parsed.append({
            "id": vacancy["id"],
            "title": vacancy["name"],
            "company": vacancy["employer"]["name"] if "employer" in vacancy else "Unknown",
            "location": vacancy["area"]["name"] if "area" in vacancy else "Unknown",
            "published_at": vacancy.get("published_at", "Unknown"),
            "description": vacancy.get("snippet", {}).get("responsibility", "No description provided"),
            # Job description
            "experience": vacancy.get("experience", {}).get("name", "Not specified"),
            "skills": ", ".join(skill["name"] for skill in vacancy.get("key_skills", []))
        })
    return parsed


# Main
if __name__ == "__main__":
    # CIS region area code (e.g., Russia: 113)
    AREA_CODE = 113

    print("Fetching 10 vacancies...")
    vacancies = fetch_vacancies(area=AREA_CODE, per_page=10)
    parsed_vacancies = parse_vacancies(vacancies)

    # Print parsed vacancies
    for vacancy in parsed_vacancies:
        print(f"ID: {vacancy['id']}")
        print(f"Title: {vacancy['title']}")
        print(f"Company: {vacancy['company']}")
        print(f"Location: {vacancy['location']}")
        print(f"Published At: {vacancy['published_at']}")
        print(f"Description: {vacancy['description']}")
        print(f"Experience: {vacancy['experience']}")
        print(f"Skills: {vacancy['skills']}")
        print("-" * 50)