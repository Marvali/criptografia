# Proyecto Académico: Cifrado y Descifrado de Texto con Kyber (ML-KEM)

## Descripción
Este repositorio contiene una aplicación sencilla en Python para **cifrar y descifrar mensajes de texto** usando el algoritmo **Kyber** (estandarizado como **ML-KEM**).

El enfoque está diseñado para un trabajo universitario de 4º de Ingeniería Informática: solución limpia, profesional y sin complejidad innecesaria.

## Objetivos
- Implementar un flujo funcional de cifrado/descifrado basado en Kyber.
- Mantener una arquitectura clara y fácil de revisar por el profesorado.
- Incluir documentación académica y estructura lista para GitHub.

## Tecnologías usadas
- **Python 3.11+**
- **pqcrypto** (implementación de algoritmos post-cuánticos, incluyendo ML-KEM)
- **Tkinter** (incluido en Python estándar, para interfaz opcional)

## Estructura del repositorio
```text
project-name/
│
├── src/
│   ├── main.py
│   ├── crypto/
│   │   ├── kyber_service.py
│   │   └── __init__.py
│   ├── ui/
│   │   ├── app.py
│   │   └── __init__.py
│   └── __init__.py
│
├── docs/
│   └── technical_explanation.md
│
├── examples/
│   └── example_usage.txt
│
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
└── run.py
```

## Instalación
1. Clonar el repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd project-name
   ```

2. Crear y activar entorno virtual (recomendado):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\\Scripts\\activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución
### Modo consola (recomendado para evaluación)
```bash
python run.py
```

### Modo interfaz gráfica Tkinter (opcional)
```bash
python run.py --ui
```

La interfaz contiene únicamente:
- Área de entrada.
- Botón **Cifrar**.
- Botón **Descifrar**.
- Área de salida.

## Ejemplo de uso
Ver archivo: `examples/example_usage.txt`.

Flujo básico:
1. Ejecutar `python run.py`.
2. Elegir opción de cifrado.
3. Copiar el paquete cifrado en Base64.
4. Elegir opción de descifrado y pegar el paquete.
5. Verificar recuperación del texto original.

## Explicación resumida del funcionamiento
Kyber (ML-KEM) es un **mecanismo de encapsulación de claves**, no un cifrador directo de texto.

Por ello, la solución usa un esquema híbrido simplificado:
1. Se encapsula un secreto compartido con ML-KEM.
2. Se deriva un flujo pseudoaleatorio mediante SHA-256.
3. Se cifra el mensaje aplicando XOR con ese flujo.
4. Para descifrar, se regenera el mismo flujo y se aplica XOR inverso.

Este planteamiento es adecuado para fines didácticos y para demostrar integración de Kyber de forma simple.

## Limitaciones del proyecto
- Es una implementación **académica** y simplificada, no un producto listo para producción.
- Se utiliza XOR con flujo derivado para mantener el código minimalista; en sistemas reales se recomienda un esquema autenticado consolidado.
- La clave pública/privada se genera al iniciar la aplicación y no se persiste.
- El cifrado/descifrado está orientado a texto UTF-8 y pruebas locales.
- La disponibilidad de `pqcrypto` puede variar según sistema operativo, arquitectura o versión de Python.

## Posibles mejoras futuras
- Persistencia segura de pares de claves.
- Inclusión de pruebas automatizadas (`pytest`).
- Uso de un esquema de cifrado autenticado más robusto en la capa simétrica.
- Intercambio de claves entre dos usuarios/procesos diferenciados.

## Autor
Trabajo académico de ejemplo para Ingeniería Informática (4º curso).

## Licencia
Este proyecto se distribuye bajo **MIT License**. Consulta el archivo `LICENSE`.
