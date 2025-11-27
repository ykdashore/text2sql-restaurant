import psycopg2
import psycopg2.extras
import sqlparse
import logging
import time

ALLOWED_STATEMENTS = {"select"}

logger = logging.getLogger(__name__)

class SafeExecutor:
    def __init__(self, dsn: str):
        self.dsn = dsn

    def validate_sql(self, sql: str):
        logger.info("Validating SQL")
        
        parsed = sqlparse.parse(sql)
        if not parsed:
            logger.warning("Validation failed: unparsable SQL")
            return False, "Empty or unparsable SQL"

        stmt_type = parsed[0].get_type().lower()
        if stmt_type not in ALLOWED_STATEMENTS:
            logger.warning(f"Validation failed: {stmt_type} not allowed")
            return False, f"Only SELECT allowed (found {stmt_type})"

        lowered = sql.lower()
        forbidden = ["insert ", "update ", "delete ", "drop ", "truncate ", "alter ", ";"]

        for token in forbidden:
            if token in lowered and not lowered.strip().startswith("select"):
                logger.warning(f"Validation failed: forbidden token '{token}'")
                return False, f"Forbidden token {token}"

        return True, "ok"

    def execute_sql(self, sql: str, timeout_seconds=5, row_limit=200):
        start = time.time()

        try:
            conn = psycopg2.connect(self.dsn)
            conn.autocommit = False
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            timeout_ms = int(timeout_seconds * 1000)
            cur.execute(f"SET statement_timeout = {timeout_ms};")
            cur.execute(f"{sql} LIMIT {row_limit};")
            rows = cur.fetchall()
            latency = time.time() - start
            logger.info(f"Query executed successfully in {latency:.4f}s")
            cur.close()
            conn.close()
            return {"rows": rows, "latency": latency}

        except Exception:
            logger.exception("SQL execution error")
            raise
