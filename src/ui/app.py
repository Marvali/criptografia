"""Interfaz gráfica mínima con Tkinter."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from src.crypto.kyber_service import KyberRuntimeError, KyberService


class KyberApp:
    """Aplicación Tkinter para cifrado y descifrado de mensajes."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Kyber - Cifrado Académico")
        self.root.geometry("700x500")

        self.service = KyberService()

        self.input_label = tk.Label(root, text="Entrada")
        self.input_label.pack(pady=(10, 0))

        self.input_text = tk.Text(root, height=8, width=90)
        self.input_text.pack(padx=10, pady=5)

        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack(pady=5)

        self.encrypt_button = tk.Button(self.buttons_frame, text="Cifrar", command=self.encrypt)
        self.encrypt_button.pack(side=tk.LEFT, padx=5)

        self.decrypt_button = tk.Button(self.buttons_frame, text="Descifrar", command=self.decrypt)
        self.decrypt_button.pack(side=tk.LEFT, padx=5)

        self.output_label = tk.Label(root, text="Salida")
        self.output_label.pack(pady=(10, 0))

        self.output_text = tk.Text(root, height=12, width=90)
        self.output_text.pack(padx=10, pady=5)

    def encrypt(self) -> None:
        plain_text = self.input_text.get("1.0", tk.END).strip()

        try:
            encrypted = self.service.encrypt_text(plain_text)
            self._set_output(encrypted)
        except KyberRuntimeError as error:
            messagebox.showerror("Error de cifrado", str(error))

    def decrypt(self) -> None:
        package_b64 = self.input_text.get("1.0", tk.END).strip()

        try:
            decrypted = self.service.decrypt_text(package_b64)
            self._set_output(decrypted)
        except KyberRuntimeError as error:
            messagebox.showerror("Error de descifrado", str(error))

    def _set_output(self, content: str) -> None:
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, content)


def run_gui() -> None:
    root = tk.Tk()
    KyberApp(root)
    root.mainloop()
