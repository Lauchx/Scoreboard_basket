# 🏀 Scoreboard Basket
![Last Commit](https://img.shields.io/github/last-commit/Lauchx/Scoreboard_basket?style=flat&logo=git&logoColor=white&color=0080ff)
![Top Language](https://img.shields.io/github/languages/top/Lauchx/Scoreboard_basket?style=flat&color=0080ff)
![Language Count](https://img.shields.io/github/languages/count/Lauchx/Scoreboard_basket?style=flat&color=0080ff)
![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)

**Scoreboard Basket** es una aplicación de escritorio profesional desarrollada en Python para la gestión y visualización de tableros de baloncesto en tiempo real. Diseñada con una arquitectura MVC, ofrece un panel de control completo para el operador y una ventana de marcador público con estética moderna tipo FIBA.

---

## 📑 Tabla de Contenidos (Accesos Directos)

- [✨ Características Principales](#-características-principales)
- [📸 Capturas y Diseño](#-capturas-y-diseño)
- [🚀 Instalación y Requisitos](#-instalación-y-requisitos)
- [🎮 Control con Joystick](#-control-con-joystick)
- [⚙️ Configuración y Personalización](#-configuración-y-personalización)
- [📂 Estructura del Proyecto](#-estructura-del-proyecto)
- [🛠 Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [📄 Licencia](#-licencia)

---

## ✨ Características Principales

### 📺 Visualización Profesional
* **Diseño Moderno:** Interfaz oscura con colores de alto contraste y fuentes digitales (Digital-7) para máxima legibilidad.
* **Modo Compacto:** Opción para reducir el tamaño de la ventana manteniendo la proporción de elementos vitales.
* **Diseño Responsivo:** Los elementos se escalan automáticamente al redimensionar la ventana.
* **Indicadores Visuales:**
    * **BONUS:** Indicadores automáticos (LED rojo) al alcanzar el límite de faltas por cuarto.
    * **Timeouts:** Indicadores visuales (3 círculos) del estado de tiempos muertos disponibles.
    * **Posesión:** Flecha indicadora de posesión alternable.

### ⏱ Gestión de Tiempo Precisa
* **Cronómetro de Partido:** Control total de minutos y segundos.
* **Precisión de Último Minuto:** Cambio automático de formato a `SS.ms` (décimas/centésimas) cuando resta menos de un minuto de juego.
* **Bocina Automática:** Reproducción de sonido y alerta visual (fondo rojo) al finalizar el tiempo.

### 🎛 Panel de Control Avanzado
* **Gestión de Equipos:** Personalización de nombres y carga de logotipos.
* **Gestión de Jugadores:**
    * Alta/Baja de jugadores con número de dorsal.
    * Marcado de titulares vs suplentes.
    * Conteo de faltas individuales con indicador de suspensión automática a la 5ta falta.
* **Reglas FIBA:**
    * Gestión de cuartos (1-4 y Overtime).
    * Lógica de Timeouts por mitades (reset inteligente en el entretiempo).
    * Faltas de equipo acumulables con lógica de Bonus.

---

## 📸 Capturas y Diseño

<div align="center">
  <img width="1373" height="760" alt="image" src="https://github.com/user-attachments/assets/f120ac97-b906-451b-a5fe-6f8bcc824ed7" />
  <p>
    <em>Foto de muestra, pantalla principal de la consola de control.</em>
  </p>
</div>
<div align="center">
  <img width="1242" height="700" alt="image" src="https://github.com/user-attachments/assets/8ad2e267-2ae6-40d0-ab98-12aafe5d2d00" />
  <p>
    <em>Tablero de basket con colores predeterminados.</em>
  </p>
</div>


---

## 🚀 Instalación y Requisitos

### Prerrequisitos
* **Python 3.10** o superior.
* Sistema Operativo: Windows, macOS o Linux.

### Pasos de Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/Lauchx/Scoreboard_basket.git](https://github.com/Lauchx/Scoreboard_basket.git)
    cd Scoreboard_basket
    ```

2.  **Crear entorno virtual (Recomendado):**
    ```bash
    python -m venv venv
    # En Windows:
    venv\Scripts\activate
    # En Mac/Linux:
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    Asegúrate de instalar las librerías necesarias listadas en `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecutar la aplicación:**
    Inicia la aplicación desde el punto de entrada principal:
    ```bash
    python main.py
    ```

---

## 🎮 Control con Joystick

El sistema integra `pygame` para permitir el control remoto del marcador mediante un gamepad. Soporta reconexión en caliente y detección automática.

### Mapeo de Botones por Defecto
La  predeterminada está diseñada para mandos estilo Xbox/PlayStation:

| Acción | Botón Xbox | Botón PlayStation |
| :--- | :---: | :---: |
| **Sumar Punto (Local)** | `LB` | `L1` |
| **Sumar Punto (Visitante)** | `RB` | `R1` |
| **Restar Punto (Local)** | `X` | `□` |
| **Restar Punto (Visitante)** | `Y` | `△` |
| **Pausar/Reanudar Reloj** | `Start` | `Options` |
| **Cambiar Posesión** | `Select` | `Share` |
| **Falta Equipo Local** | `D-Pad Izq` | `D-Pad Izq` |
| **Falta Equipo Visita** | `D-Pad Der` | `D-Pad Der` |

> 💡 **Nota:** Puedes ver el estado de conexión y probar los botones en la pestaña "Ajustes" -> "Configuración de Joystick" del panel de control.

---

## ⚙️ Configuración y Personalización

Desde el **Panel de Control**, puedes acceder a pestañas dedicadas para adaptar el sistema a las necesidades de cada partido:

### 1. Gestión de Equipos (Pestaña Equipos)
Permite la configuración completa de los equipos **Local** y **Visitante**:
* **Nombre del Equipo:** Campo de texto editable para actualizar el nombre en tiempo real.
* **Logotipo:** Botón "Cargar Logo" para subir imágenes (se redimensionan automáticamente).
* **Plantilla de Jugadores:**
    * **Alta:** Ingresa nombre y número de dorsal.
    * **Estado:** Marca jugadores como "Titular" (se muestran en verde/resaltados) o suplentes.
    * **Baja:** Elimina jugadores de la lista.

### 2. Personalización Visual (Pestaña Ajustes)
Adapta la estética del tablero a los colores del club o la iluminación del estadio en tiempo real:
* **Fondos:** Personaliza el color de fondo principal, paneles de equipo y área central.
* **Textos y Números:** Ajusta el color del reloj, los puntajes y los nombres de los equipos.
* **Indicadores:** Define colores específicos para:
    * Jugadores activos (por defecto verde neón).
    * Jugadores inactivos (banca).
    * Flecha de posesión.
* **Restaurar:** Botón para volver a los colores por defecto del tema "Moderno".

### 3. Configuración de Entrada (Joystick)
Dentro de la pestaña de ajustes, encontrarás la sección de **Configuración de Joystick**:
* **Estado:** Verifica si el mando está conectado o desconectado.
* **Tipo de Mando:** Alterna manualmente entre esquemas de **Xbox** o **PlayStation** si la detección automática falla.
* **Mapeo de Botones:** (En desarrollo) Visualiza la asignación actual de botones para las acciones principales (Puntos, Reloj, Faltas).

---

## 📂 Estructura del Proyecto

El proyecto sigue una arquitectura **MVC (Modelo-Vista-Controlador)** para mantener el código organizado y escalable:

```text
Scoreboard_basket/
├── 📁 assets/              # Recursos: Fuentes (Digital-7), sonidos (bocina)
├── 📁 controller/          # Lógica de control (Joystick, MatchState, Team)
├── 📁 gui/
│   ├── 📁 control_panel/   # Interfaz del operador (Botones, Inputs, Configuración)
│   └── 📁 scoreboard/      # Ventana de visualización pública (Diseño Moderno)
├── 📁 interfaces/          # Clases abstractas (Timer)
├── 📁 model/               # Datos y Reglas (Player, FoulManager, TimeoutManager)
├── main.py                 # Punto de entrada de la aplicación
├── requirements.txt        # Lista de dependencias
└── styles.py               # Estilos globales de Tkinter
```
---
## 🛠 Tecnologías Utilizadas

* **Python:** Lenguaje principal.
* **Tkinter:** Framework para la interfaz gráfica de usuario.
* **Pygame:** Manejo de entrada de joystick y reproducción de sonido (bocina).
* **Pillow (PIL):** Procesamiento y redimensionado de imágenes para logotipos.
---
## 📄 Licencia

Este proyecto se distribuye bajo la licencia **Apache 2.0**. Consulta el archivo `LICENSE` para más detalles.
