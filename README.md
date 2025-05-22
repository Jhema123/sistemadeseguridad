# 📷 Sistema de Vigilancia Inteligente con IA

Este proyecto implementa un sistema de vigilancia basado en inteligencia artificial que permite monitorear cámaras en tiempo real, detectar personas reales frente a la cámara, generar alertas, grabar evidencia, y gestionar usuarios y configuraciones, todo bajo una arquitectura Modelo-Vista-Controlador (MVC).

## 🧠 Características Principales

- Detección facial con validación anti-spoofing (personas reales vs fotos/objetos)
- Visualización en vivo (LiveView) con múltiples cámaras
- Grabación automática programada por horarios
- Reproducción y gestión de grabaciones
- Generación y configuración de alertas en tiempo real
- Monitoreo del estado de cámaras (activa/inactiva)
- Gestión de usuarios y roles (administrador, cadete, invitado)

## 🗂️ Estructura del Proyecto

```bash
Proyecto/
│
├── controller/           # Controladores de lógica de negocio
│   ├── dashboard_controller.py
│   ├── liveview_controller.py
│   └── ...
│
├── model/                # Acceso a datos y modelos de IA
│   ├── user_model.py
│   ├── camera_model.py
│   ├── spoof_model/      # Modelo de detección de falsificaciones
│   └── ...
│
├── view/                 # Interfaz gráfica con PyQt5
│   ├── dashboard_view.py
│   ├── liveview_view.py
│   └── ...
│
├── database/             # Conexión y configuración de base de datos
│   └── conexion.py
│
├── anti_spoofing_model.h5  # Modelo entrenado para detección facial real/falsa
├── yolov8s.pt              # Modelo YOLOv8 para detección de personas
├── main.py                 # Punto de entrada principal
└── README.md               # Documentación general del sistema
```

## 💻 Requisitos

- Python 3.10+
- OpenCV
- PyQt5
- TensorFlow / Keras
- MongoDB o SQLite
- DeepFace
- torch / ultralytics

Instalación rápida:
```bash
pip install -r requirements.txt
```

## 🛠️ Funcionalidades Implementadas

| Módulo                 | Funcionalidad                                                                 |
|------------------------|------------------------------------------------------------------------------|
| Detección              | Clasificación en tiempo real: REAL, FOTO u OBJETO                            |
| Grabación              | Activación automática por horarios definidos o eventos                       |
| Reproducción           | Lista y visualización de videos grabados                                     |
| Alertas                | Notificaciones visuales y sonoras con configuración personalizada            |
| Estado de cámaras      | Indicadores dinámicos (verde/rojo) y logs de conexión/desconexión            |
| Adición de cámaras     | Detección automática y arrastrar a celdas para transmisión                   |
| Gestión de usuarios    | Crear, modificar, eliminar usuarios y asignar roles                          |

## 📊 Historias de Usuario

- Historia 1: Detector de personas reales, fotos o cosas
- Historia 2: Acceso a grabaciones de cámaras
- Historia 3: Recepción de alertas por intrusos
- Historia 4: Configuración de horarios de grabación
- Historia 5: Personalización del tipo de alertas
- Historia 6: Estado y monitoreo de cámaras
- Historia 7: Integración de nuevas cámaras
- Historia 8: Gestión de usuarios y permisos

## 🚀 Ejecución

```bash
python main.py
```

El sistema abrirá el Dashboard principal desde donde se puede navegar entre módulos.

## 📁 Base de Datos

Este sistema puede utilizar **SQLite o MongoDB**, con modelos de usuario, cámaras, grabaciones, alertas y configuración.

## 🔐 Seguridad

- Acceso controlado por roles
- Registro de actividad
- Validación contra suplantación facial

## 📄 Licencia

Proyecto desarrollado con fines educativos y de investigación en sistemas de seguridad inteligentes.  
© 2025 - [Jhessith Lopez Heredia]
