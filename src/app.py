from fastapi import FastAPI, HTTPException,  Depends, Request
from pydantic import BaseModel
import os
from pathlib import Path
from executor import SafeExecutor, SchemaLoader
from prompt_templates import FEW_SHOT
from llm_loader import LLMLoader
import logging
from auth import verify_api_key
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(name)s — %(message)s"
)
logger = logging.getLogger("text2sql_api")

app = FastAPI(title="Text2Sql Restaurant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
logger.warning(BASE_DIR)
TEMPLATES_DIR = BASE_DIR / "ui" / "templates"

if not TEMPLATES_DIR.exists():
    logger.warning(f"Template directory not found at {TEMPLATES_DIR}")

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    logger.error("DATABASE_URL environment variable not set.")
    raise RuntimeError("DATABASE_URL environment variable is required")

executor =  SafeExecutor(DATABASE_URL)
schema_loader = SchemaLoader(DATABASE_URL)
llm_loader = LLMLoader("google-gemini")

class QueryRequest(BaseModel):
    user_query : str


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def read_root(request: Request):
    """
    Serves the HTML UI.
    """
    return templates.TemplateResponse("index.html", {"request": request})



@app.post("/query")
async def query(request: QueryRequest, api_key: str = Depends(verify_api_key)):
    nl_query = request.user_query
    logger.info(f"Received NL query: {nl_query}")
    llm = llm_loader.get_model()
    schema_text = schema_loader.format_schema_for_llm(schemas=["catalog", "sales", "staff"])
    prompt_with_query = FEW_SHOT.format(user_query=nl_query, full_ddl=schema_text)
    # logger.info("{prompt_with_query}")
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