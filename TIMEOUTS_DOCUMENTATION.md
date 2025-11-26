# Sistema de Timeouts (Tiempos Muertos) - Documentación

## 📋 Descripción General

Sistema completo de gestión de timeouts de básquetbol integrado en el proyecto Scoreboard Basket. Implementa las reglas oficiales de timeouts por periodo con interfaz visual tanto en el marcador (scoreboard) como en el controlador (control panel).

---

## 🏀 Reglas Oficiales Implementadas

### Disponibilidad de Timeouts por Periodo

| Periodo | Timeouts Disponibles | Descripción |
|---------|---------------------|-------------|
| **1ª Mitad (Q1-Q2)** | 2 timeouts | Compartidos entre ambos cuartos |
| **2ª Mitad (Q3-Q4)** | 3 timeouts | Compartidos entre ambos cuartos |
| **Overtime (Q5+)** | 1 timeout | Por cada periodo extra |

### Características
- ✅ Cada timeout dura 1 minuto (regla oficial)
- ✅ Los timeouts NO se acumulan entre mitades
- ✅ Al cambiar de mitad, los timeouts se reinician automáticamente
- ✅ En overtime, se reinician en cada periodo extra

---

## 🏗️ Arquitectura del Sistema

### Componentes Principales

```
model/
├── timeout_manager.py          # Lógica de gestión de timeouts
└── team.py                     # Integración con Team model

controller/
└── team_controller.py          # Métodos de control de timeouts

gui/scoreboard/ui_components/
├── ui_timeouts_modern.py       # UI de timeouts (diseño moderno)
└── ui_timeouts.py              # UI de timeouts (diseño original)

gui/control_panel/ui_components/
└── ui_timeouts.py              # Controles de timeouts en panel de control
```

---

## 📦 Modelo: TimeoutManager

### Clase Principal

**Archivo:** `model/timeout_manager.py`

```python
class TimeoutManager:
    """
    Gestiona los timeouts de un equipo según las reglas oficiales.
    
    Attributes:
        MAX_DISPLAY_TIMEOUTS = 3  # Siempre se muestran 3 círculos
        used_timeouts: list[bool]  # [False, False, False] = todos disponibles
        current_quarter: int       # Cuarto actual del partido
    """
```

### Métodos Principales

#### Consulta de Estado
- `get_available_count()` → int: Timeouts disponibles
- `get_used_count()` → int: Timeouts usados
- `get_max_allowed_for_period()` → int: Máximo permitido en el periodo actual
- `is_timeout_used(index)` → bool: Si un timeout está usado
- `is_timeout_available(index)` → bool: Si un timeout está disponible
- `get_timeout_states()` → list[bool]: Estado de todos los timeouts

#### Modificación de Estado
- `use_timeout(index)` → bool: Marca un timeout como usado
- `restore_timeout(index)` → bool: Marca un timeout como disponible
- `toggle_timeout(index)` → bool: Alterna el estado (usado ↔ disponible)

#### Gestión de Periodos
- `reset_for_period(new_quarter)`: Actualiza timeouts al cambiar de cuarto
- `reset_all()`: Reinicia completamente (nuevo partido)

#### Información para UI
- `get_display_info()` → dict: Información completa para mostrar
  ```python
  {
      'states': [False, False, True],  # Estado de cada timeout
      'available': 2,                   # Timeouts disponibles
      'used': 1,                        # Timeouts usados
      'max_allowed': 2,                 # Máximo en este periodo
      'can_use_more': True              # Si se pueden usar más
  }
  ```

---

## 🎮 Controlador: Team_controller

### Métodos Agregados

**Archivo:** `controller/team_controller.py`

```python
# Gestión de timeouts
toggle_timeout(timeout_index)           # Alternar estado
use_timeout(timeout_index)              # Marcar como usado
restore_timeout(timeout_index)          # Marcar como disponible
reset_timeouts()                        # Reiniciar todos
update_timeout_quarter(new_quarter)     # Actualizar cuarto
get_timeout_states()                    # Obtener estados
get_timeout_display_info()              # Obtener info completa
```

---

## 🖥️ Vista: Scoreboard (Marcador)

### Diseño Moderno

**Archivo:** `gui/scoreboard/ui_components/ui_timeouts_modern.py`

#### Componentes Visuales
- **3 círculos** debajo del puntaje de cada equipo
- **Color rojo (#FF0000)**: Timeout disponible
- **Color gris oscuro (#404040)**: Timeout usado
- **Borde blanco (2px)**: Alrededor de cada círculo
- **Tamaño**: 20px de diámetro
- **Espaciado**: 8px entre círculos

#### Funciones Principales
```python
create_timeout_indicators_modern(team_frame, team_labels, modern_style)
update_timeout_indicators_modern(team_labels, timeout_states)
setup_timeout_ui_modern(scoreboard_instance)
update_timeout_display(scoreboard_instance)
```

### Diseño Original

**Archivo:** `gui/scoreboard/ui_components/ui_timeouts.py`

Similar al diseño moderno pero con colores adaptados:
- **Color rojo (#FF0000)**: Timeout disponible
- **Color gris (#808080)**: Timeout usado
- **Fondo negro**: Compatible con diseño original

---

## 🎛️ Vista: Control Panel (Consola de Control)

### Controles de Timeouts

**Archivo:** `gui/control_panel/ui_components/ui_timeouts.py`

#### Componentes por Equipo

Cada equipo tiene un **LabelFrame** con:

1. **3 Checkbuttons** (TO 1, TO 2, TO 3)
   - Marcado = Timeout usado
   - Desmarcado = Timeout disponible
   - Al hacer clic: alterna el estado y actualiza el scoreboard

2. **Botón "Reiniciar Todos"**
   - Restaura todos los timeouts a disponibles
   - Actualiza inmediatamente el scoreboard

3. **Etiqueta informativa**
   - Muestra el periodo actual
   - Indica timeouts disponibles/máximo permitido
   - Ejemplo: "1ª mitad (Q1): 2/2 disponibles"

#### Funciones Principales
```python
setup_timeout_controls(parent, team_namespace, team_controller, column)
toggle_timeout(timeout_index, team_controller, parent)
reset_all_timeouts(team_controller, parent, team_namespace)
update_timeout_controls_for_quarter(parent, new_quarter)
sync_timeout_checkbuttons(parent)
```

---

## 🔄 Sincronización Control Panel ↔ Scoreboard

### Flujo de Actualización

```
Usuario hace clic en checkbutton (Control Panel)
    ↓
toggle_timeout() actualiza el modelo (TimeoutManager)
    ↓
parent.scoreboard_window.update_timeout_labels()
    ↓
update_timeout_indicators_modern() actualiza círculos (Scoreboard)
    ↓
Cambio visual inmediato en el marcador
```

### Métodos de Sincronización

**En Gui_scoreboard:**
```python
def update_timeout_labels(self):
    """Actualiza indicadores de timeout para ambos equipos"""
    if USE_MODERN_DESIGN:
        update_timeout_indicators_modern(...)
    else:
        update_timeout_indicators(...)
```

---

## 🔄 Cambio de Cuarto

### Comportamiento Automático

Cuando el operador cambia de cuarto (botones +/-):

1. **Se actualiza el cuarto** en `match_state.quarter`
2. **Se llama a** `update_timeouts_for_quarter_change()`
3. **Se actualiza el TimeoutManager** de ambos equipos
4. **Se reinician los timeouts** según las reglas:
   - Q1 → Q2: Timeouts NO se reinician (misma mitad)
   - Q2 → Q3: Timeouts SE REINICIAN (nueva mitad, 3 disponibles)
   - Q3 → Q4: Timeouts NO se reinician (misma mitad)
   - Q4 → Q5: Timeouts SE REINICIAN (overtime, 1 disponible)
5. **Se sincronizan los checkbuttons** con el nuevo estado
6. **Se actualiza el scoreboard** automáticamente

**Archivo:** `gui/control_panel/ui_components/ui_quarter.py`

---

## 🎨 Integración con Estilos

### Colores en Modern Style

**Archivo:** `gui/scoreboard/modern_style.py`

```python
COLORS = {
    ...
    'timeout_available': '#FF0000',  # Rojo brillante
    'timeout_used': '#404040',       # Gris oscuro
    'bg_team_info': '#1a1a2e',       # Fondo info equipo
}
```

---

## 📍 Ubicación Visual

### En el Scoreboard

```
┌─────────────────────────────────────┐
│  EQUIPO LOCAL                       │
│  Logo    Nombre                     │
│          Puntaje: 75                │
│          ● ● ○  ← Timeouts          │
│                                     │
│  Jugadores:                         │
│  ...                                │
└─────────────────────────────────────┘
```

- **Fila 3, Columna 1** del frame del equipo
- Debajo del puntaje
- Centrados horizontalmente

### En el Control Panel

```
┌─────────────────────────────────────┐
│  Pestaña: Equipos                   │
│                                     │
│  [Nombre del Equipo]                │
│  [Logo]                             │
│                                     │
│  Tiempos Muertos - Equipo Local     │
│  Marcar timeouts usados:            │
│  ☑ TO 1  ☑ TO 2  ☐ TO 3  [Reiniciar]│
│  1ª mitad (Q1): 1/2 disponibles     │
└─────────────────────────────────────┘
```

- **Fila 2** de `frames.teams`
- Debajo de los controles de jugadores

---

## 🧪 Casos de Uso

### Caso 1: Usar un Timeout en Q1

1. Operador marca "TO 1" en el control panel
2. Checkbutton se marca ✅
3. Círculo 1 en scoreboard cambia de rojo a gris
4. Etiqueta muestra: "1ª mitad (Q1): 1/2 disponibles"

### Caso 2: Intentar Usar 3er Timeout en Q1

1. Operador intenta marcar "TO 3"
2. Sistema detecta que solo se permiten 2 en 1ª mitad
3. Checkbutton NO se marca
4. Mensaje en consola: "⚠️ No se pudo cambiar el estado del timeout 3"
5. Círculo 3 permanece rojo (disponible pero no usable)

### Caso 3: Cambio de Q2 a Q3

1. Operador hace clic en "+" para cambiar cuarto
2. Sistema detecta cambio de mitad
3. Todos los timeouts se reinician automáticamente
4. Checkbuttons se desmarcan
5. Círculos vuelven a rojo
6. Etiqueta muestra: "2ª mitad (Q3): 3/3 disponibles"

### Caso 4: Reiniciar Timeouts Manualmente

1. Operador hace clic en "Reiniciar Todos"
2. Todos los checkbuttons se desmarcan
3. Todos los círculos vuelven a rojo
4. Scoreboard se actualiza inmediatamente

---

## 🔧 Mantenimiento y Extensión

### Agregar Más Timeouts

Si en el futuro se necesitan más de 3 timeouts:

1. Cambiar `MAX_DISPLAY_TIMEOUTS` en `TimeoutManager`
2. Ajustar el loop en `create_timeout_indicators_modern()`
3. Ajustar el loop en `setup_timeout_controls()`

### Cambiar Reglas de Timeouts

Modificar `get_max_allowed_for_period()` en `TimeoutManager`:

```python
def get_max_allowed_for_period(self):
    if self.current_quarter <= 2:
        return 2  # Cambiar aquí para 1ª mitad
    elif self.current_quarter <= 4:
        return 3  # Cambiar aquí para 2ª mitad
    else:
        return 1  # Cambiar aquí para overtime
```

### Agregar Sonido al Usar Timeout

En `toggle_timeout()` de `ui_timeouts.py`:

```python
if success:
    # Reproducir sonido
    play_timeout_sound()
    parent_instance.scoreboard_window.update_timeout_labels()
```

---

## ✅ Checklist de Funcionalidades

- [x] Modelo TimeoutManager con reglas oficiales
- [x] Integración en Team model
- [x] Métodos en Team_controller
- [x] UI de círculos en scoreboard moderno
- [x] UI de círculos en scoreboard original
- [x] Controles en control panel (checkbuttons)
- [x] Botón de reinicio
- [x] Sincronización bidireccional
- [x] Actualización automática al cambiar cuarto
- [x] Validación de límites por periodo
- [x] Etiquetas informativas
- [x] Colores según estado (rojo/gris)
- [x] Compatibilidad con ambos diseños

---

## 🐛 Solución de Problemas

### Los círculos no aparecen en el scoreboard

**Solución:** Verificar que `create_timeout_indicators_modern()` se llama en `apply_modern_design.py`

### Los checkbuttons no sincronizan con el scoreboard

**Solución:** Verificar que `parent_instance.scoreboard_window.update_timeout_labels()` se llama en `toggle_timeout()`

### No se pueden usar 3 timeouts en Q1

**Comportamiento esperado:** En Q1-Q2 solo se permiten 2 timeouts según las reglas oficiales

### Los timeouts no se reinician al cambiar de cuarto

**Solución:** Verificar que `update_timeouts_for_quarter_change()` se llama en `add_quarter()` y `substract_quarter()`

---

## 📝 Notas Técnicas

- **SimpleNamespace:** Se usa para organizar los componentes UI
- **Canvas:** Se usa para dibujar los círculos (mejor control que Labels)
- **BooleanVar:** Se usa para los checkbuttons (sincronización automática)
- **Callbacks:** Todas las actualizaciones usan callbacks para mantener sincronización
- **Encapsulación:** Toda la lógica está en TimeoutManager, no dispersa en la UI

---

**Fecha de creación:** 2025-11-13  
**Versión:** 1.0  
**Autor:** Sistema de Timeouts - Scoreboard Basket

