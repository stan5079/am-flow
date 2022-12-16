from api._client import api
from libs.resources.model import Model


def get_design_references(models: list[Model]) -> list[dict]:
    """Get design references.

    The `design_reference_id` will be set on the models.

    :param models: list of model objects
    :return: API response
    """

    assert [x.id for x in models]

    ids = {"id": ",".join([x.id for x in models])}
    resp = api.design_reference.search.post(ids)
    for reference in resp["results"]:
        for model in models:
            if model.id == reference["id"]:
                model.design_reference_id = reference["id"]
    return resp["results"]


def post_design_references(models: list[Model]) -> list[dict]:
    """Post design references.

    Models that already have a `design_reference_id` will be skipped.
    The `design_reference_id` will be set on the models.

    :param models: list of model objects
    :return: API response
    """

    assert [x.id for x in models]
    assert [x.path for x in models]
    assert [x.units for x in models]

    resps = []
    for model in models:
        if model.design_reference_id:
            continue
        with open(model.path, "rb") as stl:
            resp = api.design_reference.post(
                {"id": model.id, "unit": model.units}, files={"stl": stl}
            )
            if resp:
                model.design_reference_id = resp["id"]
            resps.append(resp)
    return resps


if __name__ == "__main__":
    pass
