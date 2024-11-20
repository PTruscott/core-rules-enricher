import requests

cre_base_url = "https://opencre.org/rest/v1/id/"


# do a breadth first search through the CREs until we find an asvs and a nist
# as not every CRE is linked to one
# this really should be multithreaded
def get_asvs_nist_from_cre_ids(
        cre_ids: set, explored_ids: set, related_asvs: set, related_nist: set, confidence: int = 3):
    if confidence <= 0:
        # max depth willing to go
        return related_asvs, related_nist

    next_to_explore = set()

    for cre_id in cre_ids:
        # explored ids as they can refer in loops, so we don't keep going forever
        explored_ids.add(cre_id)

        response = requests.get(cre_base_url+cre_id)
        if response.status_code == 200:
            data = response.json()
            if "links" in data["data"]:
                for link in data["data"]["links"]:
                    doc = link["document"]
                    print(doc)
                    if doc["doctype"] == "CRE" and doc["id"] not in explored_ids:
                        next_to_explore.add(doc["id"])
                        continue
                    if doc["doctype"].lower() == "standard":
                        # found a relevant nist
                        if "NIST 800-53" in doc["name"]:
                            related_nist.add((confidence, doc["hyperlink"]))
                            continue
                        # found a relevant ASVS
                        if "ASVS" in doc["name"]:
                            related_asvs.add((confidence, doc["hyperlink"]))
                            continue

    if related_asvs and related_nist:
        return related_asvs, related_nist

    # recursively dive
    return get_asvs_nist_from_cre_ids(next_to_explore, explored_ids, related_asvs, related_nist, confidence-1)


# get_asvs_nist_from_cre_ids({"683-722", "857-718", "782-234"}, set(), set(), set())

