import os

import config
from api.actions.batch import post_batch, get_batch, delete_batch
from api.actions.design_reference import post_design_references, get_design_references
from api.actions.prints import post_prints, delete_prints
from api.actions.scan_assignment import log_assignments
from libs.resources.model import Model
from libs.resources.tray import Tray

tray_ = Tray(id_="X001")
models_ = [
    Model(
        id_="ring",
        path=os.path.join(config.ROOT, "stls", "ring.stl"),
        units="mm",
        tray_id=tray_.id,
        material_reference_id="SLS",
    )
]


def process(tray: Tray, models: list[Model], to_delete: bool) -> None:
    """Process a tray with models with the AM-Vision.

    In short:
        - Fills models with design references.
        - Uploads each model as a print.
        - Creates a batch by tray name.
        - Waits for assignments and logs these.
        - Stops when all assignments are logged.

    :param tray: a tray object
    :param models: list of model objects
    :param to_delete: delete the prints and batch
    :return: None
    """

    get_design_references(models)
    post_design_references(models)
    post_prints(models)
    batch = get_batch(tray)
    if batch is None:
        post_batch(tray)
    log_assignments(tray, interval_s=5)

    if to_delete:
        delete_batch(tray)
        delete_prints(models)


if __name__ == "__main__":
    process(tray_, models_, to_delete=True)
