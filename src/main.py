"""Interfaz de consola para cifrar y descifrar texto con Kyber."""

from __future__ import annotations

from src.crypto.kyber_service import KyberRuntimeError, KyberService


def run_cli() -> None:
    service = KyberService()

    print("=== Proyecto Académico: Cifrado con Kyber (ML-KEM) ===")
    print("1) Cifrar mensaje")
    print("2) Descifrar mensaje")
    option = input("Selecciona una opción (1/2): ").strip()

    if option == "1":
        plain_text = input("Introduce el texto en claro: ").strip()
        try:
            encrypted = service.encrypt_text(plain_text)
            print("\nMensaje cifrado (Base64):")
            print(encrypted)
        except KyberRuntimeError as error:
            print(f"Error: {error}")
        return

    if option == "2":
        package = input("Introduce el paquete cifrado (Base64): ").strip()
        try:
            decrypted = service.decrypt_text(package)
            print("\nMensaje descifrado:")
            print(decrypted)
        except KyberRuntimeError as error:
            print(f"Error: {error}")
        return

    print("Opción no válida. Finalizando programa.")


if __name__ == "__main__":
    run_cli()
