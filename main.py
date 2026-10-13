
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from upstash_redis import Redis

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

redis_client = Redis(
    url=os.environ["UPSTASH_REDIS_REST_URL"],
    token=os.environ["UPSTASH_REDIS_REST_TOKEN"],
)


@app.get("/healthz")
async def healthz():
    try:
        redis_client.ping()
        return {"status": "ok", "redis": "up"}
    except Exception:
        raise HTTPException(status_code=503, detail="Redis unavailable")


@app.post("/hit/{key}")
async def hit(key: str):
    try:
        count = redis_client.incr(f"hits:{key}")
        return {"key": key, "count": int(count)}
    except Exception:
        raise HTTPException(status_code=503, detail="Redis unavailable")


@app.get("/count/{key}")
async def count(key: str):
    try:
        value = redis_client.get(f"hits:{key}")
        return {"key": key, "count": int(value) if value is not None else 0}
    except Exception:
        raise HTTPException(status_code=503, detail="Redis unavailable")
