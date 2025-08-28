# 🏀 Scoreboard Basket

**Scoreboard Basket** es una aplicación de escritorio en Python que permite controlar y mostrar el marcador de un partido de básquet en tiempo real.  
El proyecto fue desarrollado como trabajo final de facultad, utilizando **Tkinter** para la interfaz gráfica y **Pygame** para la integración con joystick.

---

## ✨ Características

- 🎛 **Panel de control**  
  Configuración de equipos (nombre y logo), botones para sumar/restar puntos y gestión de jugadores.

- 📺 **Marcador en pantalla**  
  Muestra nombres, logotipos, puntuación, cronómetro, cuarto y posesión.

- ⏱ **Cronómetro configurable**  
  Ajuste de minutos/segundos, inicio, pausa y reinicio del tiempo.

- 🎮 **Soporte para joystick (en desarrollo)**  
  Integración con `pygame.joystick` para controlar marcador, tiempo y posesión con un mando.

---

## 📦 Requisitos

- Python **3.10+**
- Librerías:
  - `tkinter` (incluido en Python)
  - `Pillow` → para manejo de imágenes
  - `pygame` → para joystick
  - (Opcional) `ttkbootstrap` o `ttkthemes` → para mejorar estética

Instala dependencias:

```bash
pip install -r requirements.txt
```

---

## ▶️ Uso

1. Clona el repositorio:

   ```bash
   git clone https://github.com/Lauchx/Scoreboard_basket.git
   cd Scoreboard_basket
   ```

2. Elije una de las dos opciones para ejecutar el programa:

   ```bash
   python main.py
   ```
   ```bash
   py main.py
   ```

3. Se abrirán dos ventanas:
   - **Panel de control** → gestiona equipos, tiempo y posesión.  
   - **Marcador** → vista principal a pantalla completa.

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**.  
