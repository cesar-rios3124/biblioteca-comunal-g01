
class ListarDetallesPrestamo:
    def __init__(self, detalle_repository):
        self.detalle_repository = detalle_repository

    def ejecutar(self, id_prestamo: int):
        return self.detalle_repository.listar_por_prestamo(id_prestamo)
