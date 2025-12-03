from fastapi import FastAPI, HTTPException,  Depends
from pydantic import BaseModel
import os
from executor import SafeExecutor, SchemaLoader
from prompt_templates import FEW_SHOT
from llm_loader import LLMLoader
import logging
from auth import verify_api_key


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
schema_loader = SchemaLoader(DATABASE_URL)
llm_loader = LLMLoader("google-gemini")

class QueryRequest(BaseModel):
    user_query : str


@app.post("/query")
async def query(request: QueryRequest, api_key: str = Depends(verify_api_key)):
    nl_query = request.user_query
    logger.info(f"Received NL query: {nl_query}")
    llm = llm_loader.get_model()
    prompt_with_query = FEW_SHOT.format(user_query=nl_query)
    response = llm.invoke(prompt_with_query)
    sql = response.content.strip()
    if sql.startswith("```sql"):
        sql = sql.replace("```sql", "").replace("```", "").strip()

    try:
        logger.info("Validating generated SQL")
        validator_ok, reason = executor.validate_sql(sql)
        if not validator_ok:
            logger.warning(f"SQL validation failed: {reason}")
            raise HTTPException(status_code=400, detail=f"Invalid SQL: {reason}")

        logger.info("SQL validated successfully. Executing SQL...")
        result = executor.execute_sql(sql)
        return {"sql": sql, "result": result}

    except HTTPException:
        raise

    except Exception as e:
        logger.exception("Unhandled error during /query processing")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/health")
def health():
    return {"status": "ok"}

# adding for better understanding and debugging
@app.get("/schema")
async def get_schema():
    """View the database schema."""
    schema_text = schema_loader.format_schema_for_llm(schemas=["catalog", "sales", "staff"])
    # print(schema_text)
    return {"schema": schema_text}