from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from executor import SafeExecutor
from prompt_templates import FEW_SHOT
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(name)s — %(message)s"
)
logger = logging.getLogger("text2sql_api")

app = FastAPI(title="Text2Sql Restaurant")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    logger.error("DATABASE_URL environment variable not set.")
    raise RuntimeError("DATABASE_URL environment variable is required")

executor =  SafeExecutor(DATABASE_URL)


class QueryRequest(BaseModel):
    user_query : str


@app.post("/query")
async def query(request: QueryRequest):
    nl_query=request.user_query
    print(nl_query)
    sql = """Some place holder"""
    try:
        logger.info("Validating generated SQL")
        validator_ok, reason = executor.validate(sql)
        if not validator_ok:
            logger.warning(f"SQL validation failed: {reason}")
            raise HTTPException(status_code=400, detail=f"Invalid SQL : {reason}")
        logger.info("SQL validated successfully. Executing SQL...")
        result = executor.execute(sql)
        return {"sql":sql, result:result}
    
    except Exception as e:
        logger.exception("Unhandled error during /query processing")
        raise HTTPException(status_code=500, detail="Something went wrong")
    

@app.get("/health")
def health():
    return {"status": "ok"}


