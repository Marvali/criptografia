"""Punto de entrada principal del proyecto."""

from __future__ import annotations

import argparse

from src.main import run_cli
from src.ui.app import run_gui


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Cifrado y descifrado de texto usando Kyber (ML-KEM).")
    parser.add_argument(
        "--ui",
        action="store_true",
        help="Ejecuta la interfaz gráfica en Tkinter. Si no se indica, se usa modo consola.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.ui:
        run_gui()
    else:
        run_cli()


if __name__ == "__main__":
    main()
