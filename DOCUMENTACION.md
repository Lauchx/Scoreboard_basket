# Documentación - Scoreboard Basket

## Tabla de Contenidos
1. [Descripción General](#descripción-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Instalación y Ejecución](#instalación-y-ejecución)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Modelos de Datos](#modelos-de-datos)
6. [Controladores](#controladores)
7. [Interfaz Gráfica](#interfaz-gráfica)
8. [Sistema de Joystick](#sistema-de-joystick)
9. [Flujo de Datos](#flujo-de-datos)
10. [Características Implementadas](#características-implementadas)
11. [Características Pendientes](#características-pendientes)
12. [Posibles Mejoras](#posibles-mejoras)

---

## Descripción General

**Scoreboard Basket** es una aplicación de escritorio desarrollada en Python que proporciona un sistema de control y visualización de marcadores de baloncesto en tiempo real. La aplicación consta de dos ventanas principales:

1. **Panel de Control**: Interfaz para operar el marcador, gestionar equipos, tiempo y estadísticas
2. **Marcador Público**: Visualización a pantalla completa para mostrar el estado del partido

El sistema soporta control tanto por mouse/teclado como por joystick/gamepad, con un sistema avanzado de mapeo de botones que se adapta automáticamente a diferentes tipos de controladores (Xbox, PlayStation).

---

## Arquitectura del Sistema

El proyecto sigue el patrón de arquitectura **Model-View-Controller (MVC)**:

### Capa de Modelo (`model/`)
- Contiene las entidades de datos principales
- Gestiona el estado del partido, equipos, jugadores y tiempo
- Implementa un sistema abstracto para el manejo de joysticks

### Capa de Controlador (`controller/`)
- Implementa la lógica de negocio
- Coordina las operaciones entre los modelos
- Maneja las interacciones del usuario y del joystick

### Capa de Vista (`gui/`)
- Interfaz de usuario construida con Tkinter
- Separación clara entre panel de control y marcador público
- Diseño modular con componentes reutilizables

---

## Instalación y Ejecución

### Requisitos del Sistema
- Python 3.7 o superior
- Sistema operativo Windows (recomendado)
- Joystick/Gamepad (opcional)

### Dependencias Principales
- `tkinter` - Interfaz gráfica (incluido en Python)
- `pygame` - Manejo de joysticks
- `pillow` - Procesamiento de imágenes
- Múltiples librerías multimedia (ver requirements.txt completo)

### Instalación
```bash
# Clonar el repositorio
git clone <URL_DEL_REPOSITORIO>
cd Scoreboard_basket

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecución
```bash
python main.py
# o
py main.py
```

---

## Estructura del Proyecto

```
Scoreboard_basket/
├── main.py                           # Punto de entrada de la aplicación
├── styles.py                         # Estilos globales de Tkinter
├── requirements.txt                  # Dependencias del proyecto
├── CLAUDE.md                         # Instrucciones para desarrollo
├── model/                           # Modelos de datos (MVC)
│   ├── match_state.py               # Estado central del partido
│   ├── team.py                      # Entidad de equipo
│   ├── player.py                    # Entidad de jugador
│   ├── time/                        # Modelos de tiempo
│   │   ├── match_time.py            # Tiempo del partido
│   │   └── possession_time.py       # Tiempo de posesión
│   ├── joystick_types.py            # Enums y tipos de joystick
│   ├── button_mapping.py            # Mapeo abstracto de botones
│   └── joystick_config.py           # Configuración por defecto
├── controller/                      # Controladores (MVC)
│   ├── match_state_controller.py    # Controlador principal del partido
│   ├── team_controller.py           # Controlador de equipos
│   ├── player_controller.py         # Controlador de jugadores
│   └── joystick_controller.py       # Controlador de joysticks
├── gui/                            # Interfaz gráfica (Vista)
│   ├── control_panel/              # Panel de control
│   │   ├── gui_control_panel.py    # Ventana principal de control
│   │   └── ui_components/          # Componentes UI modulares
│   └── scoreboard/                 # Marcador público
│       ├── gui_scoreboard.py       # Ventana del marcador
│       ├── styles_scoreboard.py    # Estilos del marcador
│       └── ui_components/          # Componentes del marcador
└── interfaces/                     # Interfaces abstractas
    └── timer.py                    # Interfaz para temporizadores
```

---

## Modelos de Datos

### Match_state
Modelo central que contiene el estado completo del partido:

```python
class Match_state:
    def __init__(self, home_team, away_team, seconds_match_time, seconds_time_left, possession, quarter):
        self.home_team = home_team                    # Equipo local
        self.away_team = away_team                    # Equipo visitante
        self.seconds_match_time = seconds_match_time  # Tiempo total del partido
        self.seconds_time_left = seconds_time_left    # Tiempo restante
        self.possession = possession                  # Posesión actual ("Home"/"Away")
        self.quarter = quarter                        # Número de cuarto
```

### Team
Entidad que representa a cada equipo:

```python
class Team:
    def __init__(self, logo, name, fouls, points, players, timeouts):
        self.logo = logo                    # Logo del equipo (imagen)
        self.name = name                    # Nombre del equipo
        self.fouls = fouls                  # Contador de faltas
        self.points = points                # Puntuación actual
        self.players = players              # Lista de jugadores
        self.timeouts = timeouts            # Tiempos muertos restantes
```

### Player
Entidad que representa a cada jugador:

```python
class Player:
    def __init__(self, name, jersey_number, is_active):
        self.name = name                    # Nombre del jugador
        self.jersey_number = jersey_number  # Número de camiseta
        self.point = 0                      # Puntos del jugador (sin implementar)
        self.foul = 0                       # Faltas del jugador (sin implementar)
        self.is_active = is_active          # Estado en cancha
```

### Modelos de Tiempo
Los modelos de tiempo implementan la interfaz abstracta `Time`:

- **Match_time**: Gestiona el tiempo del partido (incompleto)
- **Possession_time**: Gestiona el tiempo de posesión (incompleto)

---

## Controladores

### Match_state_controller
Controlador principal que coordina el estado compartido:

```python
class Match_state_controller:
    def __init__(self, home_team_controller, away_team_controller, seconds_match_time, seconds_time_left, possession, quarter):
        self.home_team_controller = home_team_controller
        self.away_team_controller = away_team_controller
        self.possession = possession
        # Crea el modelo compartido
        self.match_state = Match_state(...)
```

**Responsabilidades:**
- Crear y mantener el estado compartido entre ventanas
- Coordinar los controladores de equipos
- Gestionar el estado global del partido

### Team_controller
Controlador que gestiona las operaciones de equipos:

```python
class Team_controller:
    def __init__(self, team):
        self.team = team

    def add_point(self):                  # Sumar punto
    def substract_point(self):            # Restar punto
    def change_name(self, name):          # Cambiar nombre
    def change_logo(self, logo):          # Cambiar logo
    def add_player_in_team(self, player): # Agregar jugador
    def show_team_players(self):          # Mostrar jugadores (debug)
```

### JoystickController
Controlador avanzado para manejo de joysticks con sistema abstracto:

**Características principales:**
- **Detección automática**: Reconoce Xbox/PlayStation por nombre
- **Sistema abstracto**: Botones lógicos independientes del hardware
- **Threading**: Escucha en hilo separado sin bloquear UI
- **Configuración dinámica**: Permite reconfigurar mapeos

---

## Interfaz Gráfica

### Gui_control_panel
Ventana principal de control con las siguientes secciones:

- **Notebook de pestañas**: Organiza diferentes funciones
- **Sección de equipos**: Gestión de nombres, logos, jugadores
- **Sección de tiempo**: Controles del cronómetro del partido
- **Sección de joystick**: Configuración y prueba de controles
- **Sección de posesión**: Cambio de posesión del balón

### Gui_scoreboard
Ventana de visualización pública con las siguientes características:

- **Diseño a pantalla completa**: Optimizado para visualización a distancia
- **No se puede cerrar**: Muestra mensaje informativo si se intenta
- **Actualización en tiempo real**: Se sincroniza con el estado compartido
- **Estilo oscuro**: Fondo negro con texto brillante para visibilidad

### Sistema de Actualización
El marcador se actualiza mediante métodos específicos llamados desde el control:

```python
# Métodos de actualización del marcador
def update_points_labels(self)        # Actualiza puntuación
def update_time_labels(self)          # Actualiza tiempo
def update_team_names_labels(self)    # Actualiza nombres
def update_possession_labels(self)    # Actualiza posesión
def update_quarter_labels(self)       # Actualiza cuarto
```

---

## Sistema de Joystick

El sistema de joystick es una de las características más avanzadas del proyecto:

### Arquitectura Abstracta

#### AbstractButton (Enum)
Define botones lógicos independientes del hardware:
- **LEFT_BUMPER/RIGHT_BUMPER**: Botones superiores
- **ACTION_BOTTOM/RIGHT/LEFT/TOP**: Botones de acción principales
- **START/SELECT**: Botones de sistema
- **DPAD_***: Direcciones de la cruceta

#### ControllerType (Enum)
Tipos de controladores soportados:
- **XBOX**: Controladores Xbox/XInput
- **PLAYSTATION**: Controladores PlayStation/DualShock
- **UNKNOWN**: Controladores no reconocidos

#### ButtonMapping
Modelo de datos puro que mapea botones abstractos a físicos:

```python
# Ejemplo de mapeo Xbox
XBOX_MAPPINGS = {
    AbstractButton.LEFT_BUMPER: 4,     # LB
    AbstractButton.RIGHT_BUMPER: 5,    # RB
    AbstractButton.ACTION_BOTTOM: 0,   # A
    AbstractButton.START: 7,           # Start
    # ...
}
```

### Configuración por Defecto

```python
DEFAULT_SCOREBOARD_ACTIONS = {
    'home_add_point': AbstractButton.LEFT_BUMPER,      # LB/L1
    'away_add_point': AbstractButton.RIGHT_BUMPER,     # RB/R1
    'home_subtract_point': AbstractButton.ACTION_LEFT, # X/□
    'away_subtract_point': AbstractButton.ACTION_TOP,  # Y/△
    'manage_timer': AbstractButton.ACTION_BOTTOM,       # A/X
    'pause_timer': AbstractButton.SELECT,              # Back/Share
    'resume_timer': AbstractButton.START,              # Start/Options
}
```

### Flujo del Joystick

1. **Detección**: Pygame detecta el hardware conectado
2. **Identificación**: El sistema identifica el tipo por nombre
3. **Mapeo**: Se aplica el mapeo correspondiente al tipo
4. **Escucha**: Hilo separado escucha eventos sin bloquear UI
5. **Ejecución**: Los callbacks ejecutan acciones en el controlador

---

## Flujo de Datos

### Comunicación entre Ventanas

El sistema utiliza un patrón de **estado compartido**:

```python
# Flujo de datos
User Input → Controller → Match_state → Scoreboard Updates
    ↓
Joystick → JoystickController → Callbacks → TeamControllers → Match_state
```

### Ejemplo de Flujo Completo

1. **Usuario presiona LB** (joystick)
2. **Pygame detecta** el evento en el hilo de escucha
3. **JoystickController** mapea botón 4 → AbstractButton.LEFT_BUMPER
4. **Sistema busca** acción: LEFT_BUMPER → 'home_add_point'
5. **Ejecuta callback**: `self.home_team_controller.add_point()`
6. **Controlador modifica**: `self.team.points += 1`
7. **Control panel actualiza**: Llama a `scoreboard_window.update_points_labels()`
8. **Scoreboard refleja**: Nuevo valor en pantalla

---

## Características Implementadas

### ✅ Funcionalidades Completas

#### Gestión del Partido
- **Puntuación**: Sumar/restar puntos para ambos equipos
- **Posesión**: Cambiar posesión del balón con indicadores visuales
- **Cuartos**: Gestión básica de número de cuarto
- **Tiempo**: Cronómetro con controles de inicio/pausa (básico)

#### Gestión de Equipos
- **Nombres**: Editar nombres de equipos en tiempo real
- **Jugadores**: Agregar jugadores con número y nombre
- **Estado de jugadores**: Activar/desactivar jugadores en cancha
- **Logos**: Sistema preparado para carga de logos (no implementado)

#### Sistema de Joystick
- **Detección automática** de tipo de controlador
- **Mapeo abstracto** de botones
- **Configuración dinámica** desde la UI
- **Modo prueba** para identificar botones
- **Threading no bloqueante**
- **Callbacks configurables**

#### Interfaz de Usuario
- **Diseño modular** con componentes reutilizables
- **SimpleNamespace pattern** para organización
- **Estilos consistentes** entre ventanas
- **Actualización en tiempo real**
- **Prevención de cierre** del marcador público

---

## Características Pendientes

### ⚠️ Funcionalidades Incompletas o sin Implementar

#### Sistema de Tiempo
- **Match_time**: Lógica incompleta, solo estructura básica
- **Possession_time**: Sin implementación funcional
- **Cronómetro avanzado**: Sin gestión de períodos complejos

#### Estadísticas de Jugadores
- **Puntos por jugador**: Campo definido pero sin gestión
- **Faltas por jugador**: Campo definido pero sin gestión
- **Tiempo de juego**: No implementado
- **Estadísticas avanzadas**: No consideradas

#### Gestión de Equipos
- **Carga de logos**: Referenciada pero sin implementación
- **Faltas de equipo**: Campo definido pero sin gestión en UI
- **Timeouts**: Estructura definida pero sin controles
- **Sustituciones**: Gestión básica pero incompleta

#### Sistema de Audio
- **Alertas sonoras**: No implementadas
- **Señales de fin de período**: No implementadas
- **Notificaciones de faltas**: No implementadas

#### Persistencia
- **Guardado de partidos**: No implementado
- **Configuración persistente**: No implementada
- **Historial de partidos**: No implementado

---

## Posibles Mejoras

### Arquitectura y Patrones
1. **Observer Pattern**: Implementar updates automáticos del marcador
2. **Factory Pattern**: Para creación de componentes UI
3. **Command Pattern**: Para deshacer/rehacer acciones
4. **Dependency Injection**: Para mejor testabilidad

### Funcionalidades
1. **Sistema de sonido** para alertas y notificaciones
2. **Gestión completa** de estadísticas de jugadores
3. **Sistema de persistencia** para guardar partidos
4. **Interfaz web** para visualización remota
5. **Modo replay** para revisar jugadas
6. **Sistema de reportes** de estadísticas

### Técnica
1. **Testing unitario** para componentes críticos
2. **Logging** para debugging y auditoría
3. **Validaciones** en la entrada de datos
4. **Manejo de errores** más robusto
5. **Optimización** de rendimiento

### Experiencia de Usuario
1. **Atajos de teclado** para operaciones frecuentes
2. **Personalización** de colores y estilos
3. **Modos de visualización** diferentes (estadísticas, simple, etc.)
4. **Tutorial interactivo** para primer uso
5. **Sistema de ayuda** contextual

---

## Notas Técnicas

### Patrones de Diseño Utilizados
- **MVC**: Separación de responsabilidades
- **Singleton implícito**: Estado compartido entre ventanas
- **Strategy Pattern**: Diferentes mapeos de joystick
- **Template Method**: Componentes UI modulares
- **Abstract Factory**: Sistema de tipos abstractos

### Consideraciones de Rendimiento
- **Threading**: El joystick corre en hilo separado para no bloquear UI
- **SimpleNamespace**: Organización eficiente de componentes
- **Updates manuales**: Control preciso de cuándo se actualiza la UI

### Seguridad y Estabilidad
- **Manejo de excepciones** en control de joystick
- **Limpieza de recursos** al cerrar la aplicación
- **Prevención de cierre** accidental del marcador
- **Validación de estado** antes de operaciones

---

## Conclusión

Scoreboard Basket es un proyecto bien estructurado con una arquitectura sólida y un sistema de joystick especialmente robusto. Aunque algunas funcionalidades del core de baloncesto están incompletas, la base arquitectónica es excelente y permite fácilmente añadir nuevas características.

El sistema de joystick abstracto es particularmente notable, ya que permite una flexibilidad excepcional para diferentes tipos de controladores y configura un estándar alto para el resto del proyecto.

---

*Documentación generada el 30 de octubre de 2025 basada en el análisis del código fuente existente.*