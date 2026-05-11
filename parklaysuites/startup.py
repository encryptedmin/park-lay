import logging
import os

from django.core.management import call_command
from django.db import connection

logger = logging.getLogger(__name__)

ADVISORY_LOCK_ID = 72858111


def initialize_render_database():
    if not os.environ.get("RENDER"):
        return
    if os.environ.get("SKIP_RENDER_AUTO_INIT", "").lower() in {"1", "true", "yes", "on"}:
        return
    if os.environ.get("PARK_LAY_RENDER_INIT_DONE"):
        return

    os.environ["PARK_LAY_RENDER_INIT_DONE"] = "1"

    if connection.vendor == "postgresql":
        with connection.cursor() as cursor:
            logger.info("Waiting for Render database initialization lock.")
            cursor.execute("SELECT pg_advisory_lock(%s)", [ADVISORY_LOCK_ID])
            try:
                run_initialization()
            finally:
                cursor.execute("SELECT pg_advisory_unlock(%s)", [ADVISORY_LOCK_ID])
        return

    run_initialization()


def run_initialization():
    logger.info("Applying database migrations.")
    call_command("migrate", interactive=False, verbosity=1)

    logger.info("Initializing seed data and media.")
    call_command("init_render", verbosity=1)
