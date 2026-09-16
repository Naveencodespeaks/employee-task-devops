"""
Minimal structured-ish logging setup.

Kept intentionally simple: one call configures the root logger so every
module can just do `logging.getLogger(__name__)`. In AWS this output is
picked up automatically by CloudWatch Logs when the container writes to
stdout/stderr (which Python's logging does by default).
"""
import logging
import sys


def configure_logging(environment: str) -> None:
    level = logging.DEBUG if environment == "local" else logging.INFO
    logging.basicConfig(
        level=level,
        stream=sys.stdout,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
