Historia 1: Detección de personas reales, fotos u objetos
Descripción del Proceso:
Cuando el sistema está en funcionamiento, cada cuadro capturado por las cámaras es enviado al módulo de análisis facial. Este módulo procesa la imagen utilizando algoritmos de visión artificial para clasificarla como "REAL", "FOTO" u "OBJETO".
Si se detecta una persona real, el sistema genera una alerta inmediata (sonora y/o visual), muestra un marcador sobre la imagen (“REAL”), y registra el evento en la base de datos. Si se detecta una foto u objeto, no se genera alerta, pero se puede registrar la clasificación para fines de auditoría.

Historia 2: Acceso a grabaciones de cámaras
Descripción del Proceso:
El usuario ingresa al módulo de reproducción desde el Dashboard. Selecciona la cámara y la fecha de interés. El sistema consulta la base de datos de grabaciones, obtiene los archivos correspondientes y los muestra en la interfaz.
El usuario puede reproducir el video, pausar, avanzar, retroceder o, si lo desea, descargar o cortar un segmento específico del material. Toda la interacción se realiza desde una interfaz intuitiva que permite revisar eventos pasados de forma eficiente.

Historia 3: Recepción de alertas por intrusos
Descripción del Proceso:
Durante el análisis en vivo, si el sistema clasifica una imagen como "REAL", automáticamente se activa un flujo de alerta. Esto incluye la reproducción de un sonido (ej. alert.mp3), la aparición de una notificación en la interfaz y el registro del evento en la base de datos con detalles como la hora, fecha y cámara involucrada.
El personal de seguridad visualiza la alerta desde el panel de notificaciones (Alerts.xaml) y puede actuar de forma inmediata.

Historia 4: Configuración de horarios de grabación
Descripción del Proceso:
El usuario accede al módulo de configuración de grabación y selecciona la cámara, el horario de inicio y la duración deseada. Estos parámetros son almacenados y utilizados por el sistema para activar automáticamente la grabación en los momentos definidos.
El sistema usa temporizadores para verificar constantemente si una cámara está dentro de un horario activo. Si lo está, se inicia la grabación y se guarda el archivo resultante en una ruta específica, además de registrar la información en la base de datos.

Historia 5: Configuración del tipo de alertas
Descripción del Proceso:
Desde la vista de configuración de alertas, el usuario define el tipo de notificación que desea recibir ante eventos: solo visual, solo sonora o ambas. También puede seleccionar el archivo de sonido que quiere reproducir.
El sistema guarda estas preferencias y las aplica automáticamente cuando se genera una alerta, asegurando que el comportamiento del sistema se adapte a las necesidades del entorno o del usuario.

Historia 6: Estado de las cámaras
Descripción del Proceso:
El sistema ejecuta de forma periódica un escaneo de las cámaras conectadas. Cada una es representada con un indicador visual: verde si está operativa, rojo si no responde.
Si una cámara deja de enviar señal, su estado cambia automáticamente y se registra un evento de desconexión. Al volver a estar disponible, su estado se actualiza a verde. Esta información es visible desde el Dashboard para monitoreo continuo.

Historia 7: Adición de nuevas cámaras
Descripción del Proceso:
Cuando el usuario accede a la vista LiveView, el sistema detecta automáticamente todas las cámaras disponibles en el sistema. Estas se listan en una barra lateral como disponibles para usar.
El usuario puede arrastrar una de estas cámaras a cualquier celda del visor. Al soltarla, el sistema inicia automáticamente la transmisión en vivo de dicha cámara en la celda asignada.

Historia 8: Gestión de usuarios y roles
Descripción del Proceso:
El administrador accede a la vista de gestión de usuarios. Desde allí puede registrar un nuevo usuario, asignarle un nombre, contraseña y rol (administrador, cadete, invitado).
También puede editar usuarios existentes o eliminarlos. Cuando un usuario inicia sesión, el sistema valida su rol y activa o restringe las funcionalidades que tiene permitidas en la interfaz, garantizando el cumplimiento de políticas de acceso seguro.
