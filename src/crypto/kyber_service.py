"""Servicio de cifrado de texto usando un esquema híbrido con ML-KEM (Kyber)."""

from __future__ import annotations

import base64
import hashlib
import json
import secrets
from dataclasses import dataclass

try:
    from pqcrypto.kem.ml_kem_512 import decrypt, encrypt, generate_keypair
except ModuleNotFoundError as exc:  # pragma: no cover - validación de entorno
    raise ModuleNotFoundError(
        "No se pudo importar 'pqcrypto'. Instala dependencias con: pip install -r requirements.txt"
    ) from exc


class KyberRuntimeError(Exception):
    """Error de ejecución para operaciones de cifrado/descifrado."""


@dataclass(frozen=True)
class KyberKeyPair:
    """Par de claves de ML-KEM (Kyber)."""

    public_key: bytes
    secret_key: bytes


class KyberService:
    """Encapsula utilidades para cifrar y descifrar texto con un enfoque académico."""

    def __init__(self) -> None:
        public_key, secret_key = generate_keypair()
        self._keys = KyberKeyPair(public_key=public_key, secret_key=secret_key)

    @property
    def public_key_b64(self) -> str:
        """Representación Base64 de la clave pública (útil para mostrar en interfaz)."""
        return base64.b64encode(self._keys.public_key).decode("utf-8")

    def encrypt_text(self, plain_text: str) -> str:
        """Cifra texto UTF-8 y devuelve un paquete JSON serializado en Base64."""
        if not plain_text:
            raise KyberRuntimeError("El mensaje de entrada no puede estar vacío.")

        kem_ciphertext, shared_secret = encrypt(self._keys.public_key)
        nonce = secrets.token_bytes(16)
        plain_bytes = plain_text.encode("utf-8")

        stream = self._derive_keystream(shared_secret=shared_secret, nonce=nonce, length=len(plain_bytes))
        encrypted_data = bytes(a ^ b for a, b in zip(plain_bytes, stream))

        payload = {
            "alg": "ML-KEM-512 + XOR-Stream",
            "kem_ct": base64.b64encode(kem_ciphertext).decode("utf-8"),
            "nonce": base64.b64encode(nonce).decode("utf-8"),
            "msg_ct": base64.b64encode(encrypted_data).decode("utf-8"),
        }
        return base64.b64encode(json.dumps(payload).encode("utf-8")).decode("utf-8")

    def decrypt_text(self, package_b64: str) -> str:
        """Descifra el paquete producido por ``encrypt_text``."""
        try:
            payload_raw = base64.b64decode(package_b64.encode("utf-8"))
            payload = json.loads(payload_raw.decode("utf-8"))

            kem_ciphertext = base64.b64decode(payload["kem_ct"])
            nonce = base64.b64decode(payload["nonce"])
            encrypted_data = base64.b64decode(payload["msg_ct"])
        except (ValueError, KeyError, json.JSONDecodeError) as exc:
            raise KyberRuntimeError("El paquete cifrado no tiene un formato válido.") from exc

        shared_secret = decrypt(self._keys.secret_key, kem_ciphertext)
        stream = self._derive_keystream(shared_secret=shared_secret, nonce=nonce, length=len(encrypted_data))
        plain_bytes = bytes(a ^ b for a, b in zip(encrypted_data, stream))

        try:
            return plain_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise KyberRuntimeError(
                "No se pudo decodificar el mensaje. Puede que las claves no correspondan al cifrado."
            ) from exc

    @staticmethod
    def _derive_keystream(*, shared_secret: bytes, nonce: bytes, length: int) -> bytes:
        """Deriva un flujo pseudoaleatorio simple a partir del secreto compartido."""
        blocks: list[bytes] = []
        counter = 0

        while len(b"".join(blocks)) < length:
            counter_bytes = counter.to_bytes(4, "big")
            digest = hashlib.sha256(shared_secret + nonce + counter_bytes).digest()
            blocks.append(digest)
            counter += 1

        return b"".join(blocks)[:length]
