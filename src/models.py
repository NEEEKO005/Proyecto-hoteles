

from dataclasses import dataclass, field


@dataclass
class Habitacion:
    """Representa una habitación del hotel."""

    id: int
    numero: str
    tipo: str
    precio_por_noche: float
    disponible: bool = True

    def to_dict(self) -> dict:
        """Convierte la habitación a un diccionario serializable en JSON."""
        return {
            "id": self.id,
            "numero": self.numero,
            "tipo": self.tipo,
            "precio_por_noche": self.precio_por_noche,
            "disponible": self.disponible,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Habitacion":
        """Crea una instancia de Habitacion a partir de un diccionario."""
        return cls(
            id=data["id"],
            numero=data["numero"],
            tipo=data["tipo"],
            precio_por_noche=data["precio_por_noche"],
            disponible=data["disponible"],
        )


@dataclass
class Reserva:
    """Representa una reserva realizada por un huésped."""

    id: int
    habitacion_id: int
    nombre_huesped: str
    email_huesped: str
    fecha_entrada: str
    fecha_salida: str
    total: float
    estado: str = field(default="activa")

    def to_dict(self) -> dict:
        """Convierte la reserva a un diccionario serializable en JSON."""
        return {
            "id": self.id,
            "habitacion_id": self.habitacion_id,
            "nombre_huesped": self.nombre_huesped,
            "email_huesped": self.email_huesped,
            "fecha_entrada": self.fecha_entrada,
            "fecha_salida": self.fecha_salida,
            "total": self.total,
            "estado": self.estado,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Reserva":
        """Crea una instancia de Reserva a partir de un diccionario."""
        return cls(
            id=data["id"],
            habitacion_id=data["habitacion_id"],
            nombre_huesped=data["nombre_huesped"],
            email_huesped=data["email_huesped"],
            fecha_entrada=data["fecha_entrada"],
            fecha_salida=data["fecha_salida"],
            total=data["total"],
            estado=data["estado"],
        )