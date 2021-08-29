# 🧊 Blocky Protocol

Blocky Protocol es una simple implementación de un servidor HTTP creado en Python 3.9 y Bottle que permite subir archivos, descargarlos, removerlos y listarlos.

### Endpoints

- GET    `/ping` – Permite ver el estado del servidor
- DELETE `/remove/<filename>` – Permite remover un archivo
- GET    `/download/<filename>` - Permite descargar un archivo
- GET    `/list` - Permite listar los archivos
- POST   `/upload` - Permite subir un archivo

### Desarrolladores
- Abraham M. Lora (ToxicSSJ)
- Yoban