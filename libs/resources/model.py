class Model:
    def __init__(
        self,
        id_: str,
        path: str,
        units: str,
        tray_id: str,
        design_reference_id: str = None,
        material_reference_id: str = None,
        print_id: str = None,
    ) -> None:
        self.id = id_
        self.path = path
        self.units = units
        self.tray_id = tray_id

        self.design_reference_id = design_reference_id
        self.material_reference_id = material_reference_id
        self.print_id = print_id
