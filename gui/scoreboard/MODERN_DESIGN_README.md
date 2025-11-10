# 🎨 Diseño Moderno del Scoreboard - Guía de Uso

## 📋 Descripción

Este módulo implementa un **diseño visual moderno y profesional** para el scoreboard de básquet, inspirado en tableros digitales de **NBA/FIBA**. El diseño incluye:

- ✨ **Paleta de colores profesional**: Fondo oscuro (negro/azul oscuro) con acentos en neón, celeste, rojo y verde
- ⏱️ **Fuente digital profesional**: Reloj con tipografía tipo display LED de 7 segmentos (Orbitron/Consolas)
- 📏 **Sistema responsive**: Todos los elementos se escalan proporcionalmente al redimensionar la ventana
- 🎯 **Efectos visuales modernos**: Bordes sutiles, colores diferenciados por equipo, textos con estilo deportivo
- 🔧 **Sin alterar funcionalidad**: Solo mejora la apariencia visual, toda la lógica permanece intacta

---

## 🚀 Cómo Activar/Desactivar el Diseño Moderno

### Activar el Diseño Moderno

1. Abrir el archivo `gui/scoreboard/gui_scoreboard.py`
2. En las primeras líneas, encontrarás esta configuración:

```python
# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE DISEÑO
# ═══════════════════════════════════════════════════════════════════════════
# Cambiar a True para activar el diseño moderno profesional tipo NBA/FIBA
# Cambiar a False para usar el diseño original
USE_MODERN_DESIGN = True
# ═══════════════════════════════════════════════════════════════════════════
```

3. Asegurarse de que `USE_MODERN_DESIGN = True`
4. Ejecutar la aplicación: `python main.py`

### Volver al Diseño Original

1. Cambiar `USE_MODERN_DESIGN = False` en `gui/scoreboard/gui_scoreboard.py`
2. Ejecutar la aplicación

---

## 🎨 Características del Diseño Moderno

### Paleta de Colores

| Elemento | Color | Descripción |
|----------|-------|-------------|
| **Fondo principal** | `#0A0E27` | Azul oscuro casi negro |
| **Panel central** | `#0d1117` | Negro azulado |
| **Equipo local** | `#1a0f0f` | Rojo muy oscuro |
| **Equipo visitante** | `#0f1a1a` | Verde azulado oscuro |
| **Tiempo/Reloj** | `#00d9ff` | Cian brillante (tipo LED) |
| **Puntajes** | `#ffffff` | Blanco puro |
| **Posesión** | `#00ff41` | Verde neón |
| **Cuarto** | `#ff6b35` | Naranja |
| **Jugadores activos** | `#00ff41` | Verde neón |
| **Jugadores inactivos** | `#6b7a8f` | Gris medio |

### Fuentes Profesionales

El diseño utiliza fuentes cuidadosamente seleccionadas para lograr un aspecto profesional:

- **Reloj Digital**: Fuente **Orbitron** (moderna, tipo digital) con fallback a **Consolas** y **Courier New**
  - Color: Cian brillante (#00d9ff)
  - Tamaño: 110px (escalable)
  - Estilo: Bold para máxima legibilidad
  - Formato: MM:SS

- **Puntajes**: Fuente **Impact** / **Arial Black** para números grandes y contundentes
  - Color: Blanco puro (#ffffff)
  - Tamaño: 120px (escalable)

- **Nombres de Equipos**: Fuente **Segoe UI Semibold** / **Arial Narrow** para nombres compactos
  - Color: Blanco puro (#ffffff)
  - Tamaño: 48px (escalable)

- **Textos Generales**: Fuente **Segoe UI** / **Arial** para información adicional
  - Colores variables según contexto

### Sistema Responsive

El scoreboard se adapta automáticamente al tamaño de la ventana:

- **Tamaño mínimo**: 1000x600 píxeles
- **Escalado**: Todos los elementos (fuentes, espaciados) se escalan proporcionalmente
- **Rango de escala**: 0.6x a 2.0x del tamaño base
- **Ventana redimensionable**: Puedes ajustar el tamaño según tus necesidades

---

## 📁 Estructura de Archivos

### Archivos Nuevos Creados

```
gui/scoreboard/
├── modern_style.py                      # Clase principal de estilos modernos
├── apply_modern_design.py               # Integración con el scoreboard existente
├── MODERN_DESIGN_README.md              # Esta guía
└── ui_components/
    ├── ui_teams_modern.py               # Componentes UI modernos para equipos
    ├── ui_time_modern.py                # Componente UI moderno para el reloj digital
    ├── ui_match_modern.py               # Componentes UI modernos para partido
    └── ui_players_modern.py             # Componente UI moderno para jugadores
```

### Archivos Modificados

- `gui/scoreboard/gui_scoreboard.py`: Agregado sistema de activación/desactivación del diseño moderno

### Archivos Originales (Sin Modificar)

- `gui/scoreboard/styles_scoreboard.py`: Estilos originales (se usan cuando `USE_MODERN_DESIGN = False`)
- `gui/scoreboard/ui_components/ui_*.py`: Componentes UI originales (se usan cuando `USE_MODERN_DESIGN = False`)

---

## 🔧 Personalización

### Cambiar Colores

Editar el diccionario `COLORS` en `gui/scoreboard/modern_style.py`:

```python
COLORS = {
    'bg_primary': '#0A0E27',        # Tu color de fondo
    'display_time': '#00d9ff',      # Tu color para el reloj
    # ... etc
}
```

### Cambiar Tamaños de Fuente

Editar el diccionario `BASE_SIZES` en `gui/scoreboard/modern_style.py`:

```python
BASE_SIZES = {
    'font_team_name': 48,    # Tamaño del nombre del equipo
    'font_score': 120,       # Tamaño del puntaje
    'font_time': 80,         # Tamaño del reloj
    # ... etc
}
```

### Cambiar Fuentes

Editar el diccionario `FONTS` en `gui/scoreboard/modern_style.py`:

```python
FONTS = {
    'digital': ('Orbitron', 'Consolas', 'Courier New', 'monospace'),
    'score': ('Impact', 'Arial Black', 'Helvetica', 'bold'),
    'display': ('Segoe UI', 'Roboto', 'Arial', 'Helvetica', 'sans-serif'),
    'condensed': ('Segoe UI Semibold', 'Arial Narrow', 'Arial', 'sans-serif'),
}
```

**Nota**: Las fuentes tienen fallbacks automáticos. Si no tienes instalada la primera fuente, se usará la siguiente en la lista.

---

## 🎯 Ventajas del Diseño Moderno

1. **Profesional**: Aspecto similar a tableros reales de NBA/FIBA
2. **Legible**: Colores de alto contraste para fácil lectura a distancia
3. **Responsive**: Se adapta a diferentes tamaños de pantalla
4. **Modular**: Fácil de personalizar sin tocar la lógica
5. **Reversible**: Puedes volver al diseño original en cualquier momento
6. **Mantenible**: Código limpio y bien documentado

---

## 🐛 Solución de Problemas

### El reloj no se ve con fuente digital

**Problema**: El reloj se muestra con fuente normal en lugar de fuente digital tipo LED.

**Solución**:
1. Asegúrate de que `USE_MODERN_DESIGN = True` en `gui/scoreboard/gui_scoreboard.py`
2. La fuente digital usa **Orbitron** (incluida en Windows 10+) o **Consolas** como fallback
3. Si no te gusta la fuente, puedes cambiarla en `modern_style.py` en el diccionario `FONTS`

### El scoreboard se ve muy pequeño/grande

**Problema**: Los elementos son demasiado pequeños o grandes.

**Solución**: 
- Redimensionar la ventana manualmente (arrastrar bordes)
- O ajustar `BASE_SIZES` en `modern_style.py` para cambiar tamaños base

### Los colores no se ven bien en mi pantalla

**Problema**: Los colores oscuros no se distinguen bien.

**Solución**: Editar la paleta `COLORS` en `modern_style.py` para usar colores más claros o con más contraste.

---

## 📝 Notas Técnicas

- **Compatibilidad**: Funciona con Tkinter estándar, no requiere librerías adicionales
- **Rendimiento**: El sistema responsive tiene un umbral de actualización (5% de cambio) para evitar actualizaciones excesivas
- **Tema base**: Usa el tema 'clam' de ttk como base por ser más personalizable
- **Sin dependencias**: No requiere ttkbootstrap ni customtkinter (aunque son compatibles)

---

## 👨‍💻 Desarrollo Futuro

Posibles mejoras que se pueden agregar:

- [ ] Efectos de glow/sombra con Canvas
- [ ] Animaciones de transición para cambios de puntaje
- [ ] Temas predefinidos (NBA, FIBA, Euroliga, etc.)
- [ ] Configuración de colores desde archivo JSON
- [ ] Modo oscuro/claro
- [ ] Efectos de sonido sincronizados con cambios visuales

---

## 📄 Licencia

Este módulo de diseño es parte del proyecto Scoreboard Basket y sigue la misma licencia del proyecto principal.

---

**¡Disfruta del nuevo diseño profesional de tu scoreboard! 🏀✨**

