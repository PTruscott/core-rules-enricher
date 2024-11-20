import requests
from tinydb import TinyDB

# A file for scraping and parsing the capecs to be loaded in the database
# Ideally this would be batched so the rules would be able to remain up to date with changes without manual intervention

# you have to navigate via pages, even the pageless url only returns the first page
capec_url = "https://opencre.org/rest/v1/standard/CAPEC?page="

db = TinyDB('db.json')


def get_capecs():

    page = 1
    max_pages = 1

    capecs = []

    while page <= max_pages:
        response = requests.get(capec_url+str(page))
        if response.status_code == 200:
            data = response.json()
            if page == 1:
                # get the total number of pages that we need to load
                max_pages = data['total_pages']

            for capec in data["standards"]:
                capecs.append(parse_capecs(capec))
        else:
            print("Unable to fetch capecs")
        page += 1

    db.insert_multiple(capecs)


def parse_capecs(capec: dict) -> dict:
    cres = []
    if "links" in capec:
        for cre in capec["links"]:
            cres.append(cre["document"]["id"])

    new_capec = {
        "type": "capec",
        "id": capec["sectionID"],
        "name": capec["section"],
        "link": capec["hyperlink"],
        "cres": cres
    }

    print(new_capec)

    return new_capec

get_capecs()