# Explicación técnica breve

## 1. Enfoque criptográfico
Este proyecto utiliza **ML-KEM-512 (Kyber)** a través de la librería `pqcrypto`. Kyber es un algoritmo de encapsulación de claves (KEM), no un cifrador directo de mensajes largos.

Por ello, se aplica un enfoque híbrido simplificado:
1. Se genera un secreto compartido con ML-KEM (`encrypt` y `decrypt`).
2. A partir de ese secreto compartido y un `nonce`, se deriva un flujo pseudoaleatorio con SHA-256.
3. El mensaje se cifra/descifra aplicando XOR entre el texto y ese flujo.

Este diseño permite demostrar el uso de Kyber en un contexto académico sin introducir complejidad excesiva.

## 2. Flujo de cifrado
1. El usuario introduce un mensaje.
2. El servicio realiza encapsulación KEM con la clave pública y obtiene:
   - `kem_ct`: ciphertext KEM.
   - `shared_secret`: secreto compartido.
3. Se genera `nonce` aleatorio de 16 bytes.
4. Se deriva un keystream y se aplica XOR al mensaje.
5. Se empaqueta todo en JSON (`kem_ct`, `nonce`, `msg_ct`) y se codifica en Base64.

## 3. Flujo de descifrado
1. El usuario aporta el paquete Base64.
2. Se recuperan `kem_ct`, `nonce` y `msg_ct`.
3. Se decapsula `kem_ct` con la clave privada para recuperar `shared_secret`.
4. Se deriva el mismo keystream y se aplica XOR inverso.
5. Se devuelve el texto UTF-8 original.

## 4. Justificación académica
- Se mantiene una arquitectura clara (`src/crypto`, `src/ui`, `docs`, `examples`).
- Se separa lógica criptográfica de interfaz.
- El código es breve, legible y ejecutable.
- Incluye limitaciones explícitas, tal como se espera en un trabajo universitario serio.
