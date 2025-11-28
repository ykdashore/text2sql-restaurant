import psycopg2
import psycopg2.extras
import sqlparse
import logging
import time
import psycopg2
import logging
from typing import Dict, List
import os

ALLOWED_STATEMENTS = {"select"}

logger = logging.getLogger(__name__)

class SafeExecutor:
    def __init__(self, dsn: str):
        self.dsn = dsn or os.getenv("DATABASE_URL")

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
            sql = sql.replace(";",'')
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


class SchemaLoader:
    """Load and cache database schema information."""
    
    def __init__(self, dsn: str):
        self.dsn = dsn
        self._schema_cache = None
    
    def get_schema(self, schemas: List[str] = None) -> Dict:
        """
        Get database schema information.
        
        Args:
            schemas: List of schema names to include (e.g., ['catalog', 'sales', 'staff'])
                    If None, loads all non-system schemas.
        
        Returns:
            Dict with structure:
            {
                "schema_name": {
                    "table_name": {
                        "columns": [{"name": "col", "type": "varchar", "nullable": bool}],
                        "primary_keys": ["id"],
                        "foreign_keys": [{"column": "ref_id", "references": "other_table(id)"}]
                    }
                }
            }
        """
        if self._schema_cache is not None:
            return self._schema_cache
        
        logger.info("Loading database schema...")
        
        try:
            conn = psycopg2.connect(self.dsn)
            cur = conn.cursor()
            
            # build schema filter
            schema_filter = ""
            if schemas:
                schema_list = ", ".join(f"'{s}'" for s in schemas)
                schema_filter = f"AND table_schema IN ({schema_list})"
            else:
                schema_filter = "AND table_schema NOT IN ('pg_catalog', 'information_schema')"
            
            # get tables and columns
            query = f"""
                SELECT 
                    table_schema,
                    table_name,
                    column_name,
                    data_type,
                    is_nullable,
                    column_default FROM information_schema.columns
                WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
                {schema_filter}
                ORDER BY table_schema, table_name, ordinal_position;
            """
            cur.execute(query)
            rows = cur.fetchall()
            
            schema_info = {}
            for row in rows:
                schema_name, table_name, col_name, data_type, nullable, default = row
                
                if schema_name not in schema_info:
                    schema_info[schema_name] = {}
                
                if table_name not in schema_info[schema_name]:
                    schema_info[schema_name][table_name] = {
                        "columns": [],
                        "primary_keys": [],
                        "foreign_keys": []
                    }
                
                schema_info[schema_name][table_name]["columns"].append({
                    "name": col_name,
                    "type": data_type,
                    "nullable": nullable == "YES",
                    "default": default
                })
            
            # Get primary keys
            pk_query = f"""
                SELECT 
                    kcu.table_schema,
                    kcu.table_name,
                    kcu.column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                    ON tc.constraint_name = kcu.constraint_name
                    AND tc.table_schema = kcu.table_schema
                WHERE tc.constraint_type = 'PRIMARY KEY'
                {schema_filter.replace('table_schema', 'tc.table_schema')}
                ORDER BY kcu.table_schema, kcu.table_name, kcu.ordinal_position;
            """
            
            cur.execute(pk_query)
            for schema_name, table_name, col_name in cur.fetchall():
                if schema_name in schema_info and table_name in schema_info[schema_name]:
                    schema_info[schema_name][table_name]["primary_keys"].append(col_name)
            
            # Get foreign keys
            fk_query = f"""
                SELECT
                    tc.table_schema,
                    tc.table_name,
                    kcu.column_name,
                    ccu.table_schema AS foreign_schema,
                    ccu.table_name AS foreign_table,
                    ccu.column_name AS foreign_column
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                    ON tc.constraint_name = kcu.constraint_name
                    AND tc.table_schema = kcu.table_schema
                JOIN information_schema.constraint_column_usage ccu
                    ON ccu.constraint_name = tc.constraint_name
                WHERE tc.constraint_type = 'FOREIGN KEY'
                {schema_filter.replace('table_schema', 'tc.table_schema')}
                ORDER BY tc.table_schema, tc.table_name;
            """
            
            cur.execute(fk_query)
            for schema_name, table_name, col_name, fk_schema, fk_table, fk_col in cur.fetchall():
                if schema_name in schema_info and table_name in schema_info[schema_name]:
                    schema_info[schema_name][table_name]["foreign_keys"].append({
                        "column": col_name,
                        "references": f"{fk_schema}.{fk_table}({fk_col})"
                    })
            
            cur.close()
            conn.close()
            
            self._schema_cache = schema_info
            logger.info(f"Schema loaded: {len(schema_info)} schemas, "
                       f"{sum(len(tables) for tables in schema_info.values())} tables")
            
            return schema_info
        
        except Exception as e:
            logger.exception("Failed to load schema")
            raise
    
    def format_schema_for_llm(self, schemas: List[str] = None) -> str:
        """Format schema as a string suitable for LLM context, basically schema description."""

        schema_info = self.get_schema(schemas)
        lines = ["# Database Schema\n"]
        for schema_name, tables in schema_info.items():
            lines.append(f"\n## Schema: {schema_name}\n")
            
            for table_name, table_info in tables.items():
                lines.append(f"### {schema_name}.{table_name}")
                
                # Columns
                for col in table_info["columns"]:
                    nullable = "NULL" if col["nullable"] else "NOT NULL"
                    pk_marker = " (PK)" if col["name"] in table_info["primary_keys"] else ""
                    lines.append(f"  - {col['name']}: {col['type']} {nullable}{pk_marker}")
                
                # Foreign keys
                if table_info["foreign_keys"]:
                    lines.append("  Foreign Keys:")
                    for fk in table_info["foreign_keys"]:
                        lines.append(f"    - {fk['column']} → {fk['references']}")
                
                lines.append("")
        
        return "\n".join(lines)
    
    def get_table_sample_data(self, schema: str, table: str, limit: int = 3) -> List[Dict]:
        """Get sample rows from a table for better context."""
        try:
            conn = psycopg2.connect(self.dsn)
            cur = conn.cursor()
            
            cur.execute(f'SELECT * FROM "{schema}"."{table}" LIMIT {limit};')
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return [dict(zip(columns, row)) for row in rows]
        
        except Exception as e:
            logger.warning(f"Could not fetch sample data for {schema}.{table}: {e}")
            return []