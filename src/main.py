import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI

import application

logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)s %(filename)s %(funcName)s: %(message)s",
    level=logging.INFO,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan event handler."""
    await application.startup()
    logging.info("FastAPI startup")
    yield
    await application.shutdown()
    logging.info("FastAPI shutdown")

app = application.initialize(lifespan=lifespan)
