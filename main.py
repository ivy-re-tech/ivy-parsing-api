import logging.config
import os

import uvicorn
import yaml
from fastapi import FastAPI

import address
import name

DEBUG = bool(os.environ.get("DEBUG", False))


app = FastAPI(debug=DEBUG)


with open("log-config.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
logger = logging.getLogger("App")


@app.get("/")
async def root():
    return "pong"


@app.get("/address/{addr}", response_model=address.Address)
async def addr_parse(addr: str):
    parsed = address.multiparse(addr)
    return parsed


@app.get("/name/{fullname}", response_model=name.NameResponse)
async def name_parse(fullname: str):
    parsed = name.run_parse(fullname)
    return parsed


if __name__ == "__main__":
    logger.info(f"Starting server... Debug: {DEBUG}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
