from executor import SafeExecutor
import os 

EXECUTOR = SafeExecutor(os.getenv("DATABASE_URL"))

def test_execute_basic_select():
    result = EXECUTOR.execute_sql("SELECT 1 AS value")
    assert "rows" in result
    assert result["rows"][0]["value"] == 1
