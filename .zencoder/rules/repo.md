---
description: Repository Information Overview
alwaysApply: true
---

# Scoreboard Basket Information

## Summary

Scoreboard Basket is a Python desktop application for real-time basketball scoreboard control and display. The application consists of two main windows: a control panel for managing game state and a scoreboard display. Built with Tkinter for the GUI and Pygame for joystick control, it follows an MVC architecture pattern.

## Structure

The project is organized into the following main directories:

- **`controller/`**: MVC controllers including `match_state_controller.py`, `team_controller.py`, `player_controller.py`, and `joystick_controller.py` for handling joystick input with threading
- **`model/`**: Data models for match state, teams, players, fouls, and timeouts; also contains timing logic in `time/` subdirectory
- **`gui/`**: User interface components split into `control_panel/` (management interface) and `scoreboard/` (public display)
- **`interfaces/`**: Interface definitions
- **`assets/`**: Images and digital fonts for UI rendering

## Language & Runtime

**Language**: Python  
**Version**: 3.10+ (tested with 3.13.3)  
**Build System**: Standard Python module system  
**Package Manager**: pip

## Dependencies

**Main Dependencies**:
- `tkinter` (built-in) - GUI framework
- `pygame==2.6.1` - Joystick input handling
- `pillow==11.3.0` - Image processing for team logos
- `numpy==2.3.2` - Numerical computations
- `scipy==1.16.1` - Scientific computing utilities

**Additional Dependencies**:
- `av==13.1.0`, `pydub==0.25.1` - Audio/video processing
- `moderngl==5.12.0`, `pyglet==2.1.6` - Graphics rendering
- `beautifulsoup4==4.13.4` - Data parsing
- Complete list in `requirements.txt`

## Build & Installation

```bash
pip install -r requirements.txt
```

## Main Entry Point

**File**: `main.py`  
**Description**: Application entry point that initializes the main Tkinter window, applies styling, and launches the control panel with scoreboard display.

**Run Command**:
```bash
python main.py
```
or
```bash
py main.py
```

## Architecture Overview

**MVC Pattern Implementation**:
- **Models** (`model/`): Central `Match_state` object maintains shared state between control panel and scoreboard
- **Controllers** (`controller/`): Coordinate between UI and data models; joystick controller runs on separate threads to avoid blocking UI
- **Views** (`gui/`): Component-based architecture with separate UI modules for different scoreboard sections

**Key Features**:
- Real-time score and time management with configurable timers
- Joystick support with button configuration for game control
- Foul tracking and timeout management per team
- Player roster management with active/inactive status
- Two-window system (control panel + full-screen display)

## Testing

No formal testing framework is configured. The application runs directly from the main entry point. Test files are not present in the project structure.

## Additional Configuration

**Styling**: `styles.py` contains Tkinter theme configuration using the `xpnative` theme with custom styling for scoreboard components.

**Documentation**: 
- `CLAUDE.md` - Development guidelines
- `DOCUMENTACION.md` - Detailed project documentation
- `TIMEOUTS_DOCUMENTATION.md` - Timeout system documentation
