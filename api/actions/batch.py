from slumber.exceptions import HttpNotFoundError

from api._client import api
from api._exceptions import ManyResults
from libs.resources.tray import Tray


def get_batch(tray: Tray) -> dict | None:
    """Get a batch.

    The `batch_id` will be set on the tray.

    :param tray: a tray object
    :return: API response
    """

    assert tray.id

    resp = api.batch.get(id=tray.id)
    if resp["count"] == 1:
        batch = resp["results"][0]
        tray.batch_id = batch["id"]
        return batch
    elif resp["count"] > 1:
        raise ManyResults


def post_batch(tray: Tray) -> dict:
    """Post a batch.

    The `batch_id` will be set on the tray.

    :param tray: a tray object
    :return: API response
    """

    assert tray.id

    batch = api.batch.post(
        {"id": tray.id, "title": tray.id, "query": f"tray={tray.id}"}
    )
    if batch:
        tray.batch_id = batch["id"]
    return batch


def delete_batch(tray: Tray) -> bool | dict:
    """Delete a batch.

    The `batch_id` will be removed from the tray.

    :param tray: a tray object
    :return: API response
    """

    assert tray.batch_id

    try:
        resp = api.batch(tray.batch_id).delete()
    except HttpNotFoundError:
        resp = False
    if resp:
        tray.batch_id = None
    return resp


if __name__ == "__main__":
    pass
