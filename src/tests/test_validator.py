from executor import SafeExecutor
import os

EXECUTOR = SafeExecutor(os.getenv("DATABASE_URL"))

def test_valid_select():
    ok, reason = EXECUTOR.validate_sql("SELECT 1")
    assert ok is True

def test_reject_update():
    ok, reason = EXECUTOR.validate_sql("UPDATE table SET x=1")
    assert ok is False

def test_reject_delete():
    ok, reason = EXECUTOR.validate_sql("DELETE FROM table")
    assert ok is False

def test_reject_empty():
    ok, reason = EXECUTOR.validate_sql("")
    assert ok is False
