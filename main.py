from fastapi import FastAPI
from tinydb import TinyDB, Query

from asvs_nist_loader import get_asvs_nist_from_cre_ids

# TinyDB is a small self-contained nosql database, with syntax similar to mongodb or the like
db = TinyDB('db.json')

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!  Please navigate to /rule_info/{your_rule_id}"}


@app.get("/rule_info/{rule_id}")
async def get_rule_info(rule_id: str) -> dict:
    entries = {
        "message": "",
        "ASVS": [],
        "NIST": [],
        "rule_info": None,
    }

    query = Query()
    rule = db.search((query.id == rule_id) & (query.type == "core_rule"))

    if rule:
        rule = rule[0]
    else:
        return {"message": "rule not found"}

    if rule["capecs"]:
        capecs = db.search((query.id.test(lambda s: s in rule["capecs"]) & (query.type == "capec")))
        rule["linked_capecs"] = capecs

        cres = set()

        for capec in capecs:
            if capec["cres"]:
                cres.update(capec["cres"])

        rule["linked_cres"] = cres

        asvs, nist = get_asvs_nist_from_cre_ids(cres, set(), set(), set())

        for confidence, a in asvs:
            entries["ASVS"].append({
                "confidence": confidence,
                "entry": a
            })

        for confidence, n in nist:
            entries["NIST"].append({
                "confidence": confidence,
                "entry": n
            })

        if asvs and nist:
            entries["message"] = "ASVS and NIST found via CAPEC and CRE match"

    if not entries["message"]:
        entries["message"] = "Could not find matching ASVS and NIST"

    entries["rule_info"] = rule

    return entries


@app.get("/rules/{rule_id}")
async def get_core_rules(rule_id: str) -> dict:
    core_rule = Query()
    rule = db.search((core_rule.id == rule_id) & (core_rule.type == "core_rule"))

    if rule:
        return rule[0]
    else:
        return {"message": "rule not found"}


@app.get("/capecs/{capec_id}")
async def get_capecs(capec_id: str) -> dict:
    capec = Query()
    capec = db.search((capec.id == capec_id) & (capec.type == "capec"))

    if capec:
        return capec[0]
    else:
        return {"message": "capec not found"}

