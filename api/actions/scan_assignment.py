import time
from datetime import datetime

from api._client import api, log
from api.actions.batch import get_batch
from libs.resources.tray import Tray


def log_assignments(tray: Tray, interval_s: int) -> None:
    """Log assignments from a tray.

    Assignments will only be logged once. When all assignments are logged,
    the function will stop iterating.

    :param tray: a tray object
    :param interval_s: polling interval in seconds
    :return: None
    """

    assert tray.id
    assert tray.batch_id

    logged_uuids = []

    while True:
        # Scan for new assignments
        resp = api.scan_assignment.get(batch=tray.batch_id)
        for assignment in resp["results"]:

            # Skip logged assignments.
            uuid = assignment["uuid"]
            if uuid in logged_uuids:
                continue

            # Log the assignment.
            created = assignment["created"]
            timestamp = datetime.fromisoformat(created).strftime("%c")
            log.debug(f"tray {tray.id}, scan assignment at {timestamp}")
            logged_uuids.append(uuid)

        # Stop iterating as soon as the batch is completed.
        batch = get_batch(tray)
        prints = batch["summary"]["prints"]
        assigned = batch["summary"]["assigned"]
        if prints == assigned:
            log.debug(f"tray {tray.id}, scan assignments completed")
            break

        # Wait to avoid too many requests.
        time.sleep(interval_s)


if __name__ == "__main__":
    pass
