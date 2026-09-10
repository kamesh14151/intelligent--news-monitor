import time, uuid
from contextlib import contextmanager
from app.db.session import SessionLocal
from app.db.models import AgentRunRow

@contextmanager
def agent_audit(run_id: str, agent_name: str):
    start = time.perf_counter(); status = "success"
    try:
        yield
    except Exception:
        status = "error"
        raise
    finally:
        db = SessionLocal()
        try:
            db.add(AgentRunRow(id=uuid.uuid4().hex, run_id=run_id, agent_name=agent_name, status=status, latency_ms=(time.perf_counter()-start)*1000))
            db.commit()
        except Exception:
            db.rollback()
        finally:
            db.close()
