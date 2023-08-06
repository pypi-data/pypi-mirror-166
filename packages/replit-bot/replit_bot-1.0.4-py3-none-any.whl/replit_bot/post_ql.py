"""file that handles posting to replit grpahql endpoint for queries and mutations"""

import json
from requests import post as _post, get as _get, delete as _delete
from typing import Dict, Any
from .logging import logging

def get_queries() -> Dict[str, Any]:
    return json.load(open('queries.json'))

end = "https://replit.com/graphql"
headers = {
            "X-Requested-With": "replit",
            'Origin': 'https://replit.com',
            'Accept': 'application/json',
            'Referrer': 'https://replit.com',
            'Content-Type': 'application/json',
            'Connection': 'keep-alive',
            'Host': "replit.com",
            "x-requested-with": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0",
        }

def post(connection: str, query: str, vars: Dict[str, Any] = {}):
    """post query with vars to replit graph query language"""
    _headers = headers
    _headers["Cookie"] = f"connect.sid={connection}"
    req = _post(end, json = {
            "query": query,
            "variables": vars,
        }, headers = _headers)
    if (req.status_code == 200):
        logging.success("Successful graphql!", query, vars, sep="\n")
    else:
        logging.error(req, req.text, sep="\n")
    res = json.loads(req.text)
    try:
        _ = list(map(lambda x: x["data"], list(res["data"])))
    except:
        try:
            return res["data"]["data"]
        except:
            return res["data"]