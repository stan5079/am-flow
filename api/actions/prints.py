import uuid

from slumber.exceptions import HttpNotFoundError

from api._client import api
from libs.resources.model import Model


def post_prints(models: list[Model]) -> list[dict]:
    """Post prints.

    The `print_id` will be set on the models.

    :param models: list of model objects
    :return: API response
    """

    assert [x.id for x in models]
    assert [x.design_reference_id for x in models]
    assert [x.material_reference_id for x in models]
    assert [x.tray_id for x in models]

    resps = []
    for model in models:
        print_ = [
            {
                "id": str(uuid.uuid4()),
                "title": model.id.title(),
                "copies": 1,
                "design_reference": model.design_reference_id,
                "material_reference": model.material_reference_id,
                "attributes": {
                    "tray": model.tray_id,
                },
            }
        ]
        resp = api.print.post(print_)
        if resp:
            model.print_id = resp[0]["id"]
        resps.append(resp)
    return resps


def delete_prints(models: list[Model]) -> list[bool | dict]:
    """Delete prints.

    Models that don't have a `print_id` will be skipped.
    The `print_id` will be removed from the models.

    :param models: list of model objects
    :return: API response
    """

    assert [x.print_id for x in models]

    resps = []
    for model in models:
        try:
            resp = api.print(model.print_id).delete()
        except HttpNotFoundError:
            resp = False
        if resp is True:
            model.batch_id = None
        resps.append(resp)
    return resps


if __name__ == "__main__":
    pass
