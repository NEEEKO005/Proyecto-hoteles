"""Interfaz de línea de comandos para el sistema de administración de hotel."""

from typing import Annotated, Optional

import typer
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from hotel_manager.exceptions import HotelError
from hotel_manager.services import HotelService

app = typer.Typer(
    name="hotel-manager",
    help="🏨 Sistema de administración de habitaciones de hotel.",
    rich_markup_mode="rich",
)

console = Console()
service = HotelService()

# ── Helpers ───────────────────────────────────────────────────────────────────


def _tabla_habitaciones(titulo: str = "Habitaciones") -> Table:
    """Crea y retorna una tabla Rich con columnas predefinidas para habitaciones."""
    tabla = Table(title=titulo, box=box.ROUNDED, header_style="bold cyan")
    tabla.add_column("ID", style="dim", width=5)
    tabla.add_column("Número", justify="center")
    tabla.add_column("Tipo", justify="center")
    tabla.add_column("Precio/Noche", justify="right", style="green")
    tabla.add_column("Disponible", justify="center")
    return tabla


def _fila_habitacion(tabla: Table, h: object) -> None:
    """Agrega una fila de habitación a la tabla Rich."""
    disponible = "✅ Sí" if h.disponible else "❌ No"  # type: ignore[attr-defined]
    tabla.add_row(
        str(h.id),  # type: ignore[attr-defined]
        h.numero,  # type: ignore[attr-defined]
        h.tipo,  # type: ignore[attr-defined]
        f"${h.precio_por_noche:.2f}",  # type: ignore[attr-defined]
        disponible,
    )


def _tabla_reservas(titulo: str = "Reservas") -> Table:
    """Crea y retorna una tabla Rich con columnas predefinidas para reservas."""
    tabla = Table(title=titulo, box=box.ROUNDED, header_style="bold magenta")
    tabla.add_column("ID", style="dim", width=5)
    tabla.add_column("Hab.", justify="center")
    tabla.add_column("Huésped")
    tabla.add_column("Email")
    tabla.add_column("Entrada")
    tabla.add_column("Salida")
    tabla.add_column("Total", justify="right", style="green")
    tabla.add_column("Estado", justify="center")
    return tabla


def _fila_reserva(tabla: Table, r: object) -> None:
    """Agrega una fila de reserva a la tabla Rich."""
    color = "green" if r.estado == "activa" else "yellow"  # type: ignore[attr-defined]
    tabla.add_row(
        str(r.id),  # type: ignore[attr-defined]
        str(r.habitacion_id),  # type: ignore[attr-defined]
        r.nombre_huesped,  # type: ignore[attr-defined]
        r.email_huesped,  # type: ignore[attr-defined]
        r.fecha_entrada,  # type: ignore[attr-defined]
        r.fecha_salida,  # type: ignore[attr-defined]
        f"${r.total:.2f}",  # type: ignore[attr-defined]
        f"[{color}]{r.estado}[/{color}]",  # type: ignore[attr-defined]
    )


# ── Comandos: Habitaciones ────────────────────────────────────────────────────


@app.command("listar-habitaciones")
def listar_habitaciones(
    disponibles: Annotated[
        bool, typer.Option("--disponibles", help="Mostrar solo habitaciones libres.")
    ] = False,
) -> None:
    """Lista todas las habitaciones del hotel."""
    try:
        habitaciones = service.listar_habitaciones(solo_disponibles=disponibles)
        if not habitaciones:
            console.print("[yellow]No hay habitaciones registradas.[/yellow]")
            return
        titulo = "Habitaciones Disponibles" if disponibles else "Todas las Habitaciones"
        tabla = _tabla_habitaciones(titulo)
        for h in habitaciones:
            _fila_habitacion(tabla, h)
        console.print(tabla)
    except HotelError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1) from e


@app.command("agregar-habitacion")
def agregar_habitacion(
    numero: Annotated[str, typer.Argument(help="Número de la habitación (ej: '305').")],
    tipo: Annotated[str, typer.Argument(help="Tipo: simple, doble o suite.")],
    precio: Annotated[float, typer.Argument(help="Precio por noche en USD.")],
) -> None:
    """Registra una nueva habitación en el hotel."""
    try:
        habitacion = service.agregar_habitacion(numero, tipo, precio)
        console.print(
            Panel(
                f"[green]✅ Habitación [bold]{habitacion.numero}[/bold] agregada con ID {habitacion.id}.[/green]",
                title="Éxito",
            )
        )
    except HotelError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1) from e


@app.command("actualizar-habitacion")
def actualizar_habitacion(
    habitacion_id: Annotated[int, typer.Argument(help="ID de la habitación.")],
    numero: Annotated[Optional[str], typer.Option(help="Nuevo número.")] = None,
    tipo: Annotated[Optional[str], typer.Option(help="Nuevo tipo.")] = None,
    precio: Annotated[Optional[float], typer.Option(help="Nuevo precio por noche.")] = None,
    disponible: Annotated[Optional[bool], typer.Option(help="Nueva disponibilidad.")] = None,
) -> None:
    """Actualiza los datos de una habitación existente."""
    try:
        hab = service.actualizar_habitacion(habitacion_id, numero, tipo, precio, disponible)
        console.print(f"[green]✅ Habitación [bold]{hab.numero}[/bold] actualizada.[/green]")
    except HotelError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1) from e


@app.command("eliminar-habitacion")
def eliminar_habitacion(
    habitacion_id: Annotated[int, typer.Argument(help="ID de la habitación a eliminar.")],
) -> None:
    """Elimina una habitación del hotel."""
    try:
        service.eliminar_habitacion(habitacion_id)
        console.print(f"[green]✅ Habitación con ID {habitacion_id} eliminada.[/green]")
    except HotelError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1) from e


# ── Comandos: Reservas ────────────────────────────────────────────────────────


@app.command("listar-reservas")
def listar_reservas(
    estado: Annotated[
        Optional[str], typer.Option(help="Filtrar por estado: activa o completada.")
    ] = None,
) -> None:
    """Lista todas las reservas del hotel."""
    try:
        reservas = service.listar_reservas(estado=estado)
        if not reservas:
            console.print("[yellow]No hay reservas registradas.[/yellow]")
            return
        titulo = f"Reservas [{estado}]" if estado else "Todas las Reservas"
        tabla = _tabla_reservas(titulo)
        for r in reservas:
            _fila_reserva(tabla, r)
        console.print(tabla)
    except HotelError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1) from e


@app.command("crear-reserva")
def crear_reserva(
    habitacion_id: Annotated[int, typer.Argument(help="ID de la habitación a reservar.")],
    nombre: Annotated[str, typer.Argument(help="Nombre completo del huésped.")],
    email: Annotated[str, typer.Argument(help="Email del huésped.")],
    entrada: Annotated[str, typer.Argument(help="Fecha de entrada (YYYY-MM-DD).")],
    salida: Annotated[str, typer.Argument(help="Fecha de salida (YYYY-MM-DD).")],
) -> None:
    """Crea una nueva reserva para una habitación disponible."""
    try:
        reserva = service.crear_reserva(habitacion_id, nombre, email, entrada, salida)
        console.print(
            Panel(
                f"[green]✅ Reserva creada con ID [bold]{reserva.id}[/bold].\n"
                f"Huésped: {reserva.nombre_huesped}\n"
                f"Total: [bold]${reserva.total:.2f}[/bold][/green]",
                title="Reserva Confirmada",
            )
        )
    except HotelError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1) from e


@app.command("cancelar-reserva")
def cancelar_reserva(
    reserva_id: Annotated[int, typer.Argument(help="ID de la reserva a cancelar.")],
) -> None:
    """Cancela una reserva activa y libera la habitación."""
    try:
        reserva = service.cancelar_reserva(reserva_id)
        console.print(
            f"[green]✅ Reserva {reserva_id} cancelada. "
            f"Habitación ID {reserva.habitacion_id} liberada.[/green]"
        )
    except HotelError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1) from e


@app.command("ingresos")
def ver_ingresos() -> None:
    """Muestra el total de ingresos por reservas completadas."""
    total = service.calcular_ingresos()
    console.print(
        Panel(
            f"[bold green]💰 Total de ingresos: ${total:.2f} USD[/bold green]",
            title="Ingresos del Hotel",
        )
    )


if __name__ == "__main__":
    app()
