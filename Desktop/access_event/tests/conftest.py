import os
import tempfile
from pathlib import Path

import pytest

# ВАЖНО: всё это должно выполниться ДО "from app import app",
# потому что config.py читает переменные окружения при импорте.
_tmp_dir = tempfile.mkdtemp(prefix="accessevent_tests_")
_db_file = Path(_tmp_dir, "test.db").as_posix()

os.environ["TESTING"] = "1"
os.environ["USE_SQLITE"] = "0"
os.environ["DATABASE_URL"] = "sqlite:///" + _db_file

from app import app, db  # noqa: E402


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        with app.app_context():
            db.create_all()
            yield c
            db.session.remove()
            db.drop_all()