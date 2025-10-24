# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Scoreboard Basket is a Python desktop application for real-time basketball scoreboard control and display. It's built with Tkinter for the GUI and includes Pygame integration for joystick control. The application consists of two main windows: a control panel and a scoreboard display.

## Development Commands

### Running the Application
```bash
python main.py
# or
py main.py
```

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### Testing
No specific test framework is currently configured. The project runs directly from the main entry point.

## Architecture Overview

### MVC Architecture Pattern
The application follows a Model-View-Controller pattern:

**Models (`model/`)**:
- `match_state.py`: Central state container holding home/away teams, time, possession, quarter
- `team.py`: Team entity with logo, name, fouls, points, players, timeouts
- `player.py`: Player entity with jersey number, name, active status
- `time/match_time.py`: Match timing logic
- `time/possession_time.py`: Possession timing logic

**Controllers (`controller/`)**:
- `match_state_controller.py`: Manages match state and coordinates between teams
- `team_controller.py`: Handles team operations (points, players, logos)
- `player_controller.py`: Manages player active/inactive status
- `joystick_controller.py`: Handles joystick input with threading for real-time control

**Views (`gui/`)**:
- `control_panel/`: Control interface with tabs for teams and match management
- `scoreboard/`: Public display showing teams, scores, time, possession
- Both use component-based UI with separate files for different UI sections

### Key Architectural Patterns

**Shared State Management**: The `Match_state` object is shared between the control panel and scoreboard display, ensuring both windows show identical data.

**SimpleNamespace Pattern**: Extensive use of `SimpleNamespace` for organizing UI components and controllers, providing clean dot notation access to nested elements.

**Component-Based UI**: UI elements are separated into logical components (teams, time, players, etc.) with dedicated setup functions.

**Joystick Integration**: Real-time joystick control using Pygame with threading to avoid blocking the main UI.

## File Structure

```
├── main.py                           # Application entry point
├── styles.py                         # Global Tkinter style configuration
├── controller/                       # MVC controllers
├── model/                           # Data models
├── gui/
│   ├── control_panel/               # Control interface
│   │   ├── gui_control_panel.py    # Main control window
│   │   └── ui_components/          # UI component modules
│   └── scoreboard/                  # Public display
│       ├── gui_scoreboard.py       # Main scoreboard window
│       └── ui_components/          # UI component modules
├── interfaces/                      # Interface definitions
└── requirements.txt                 # Python dependencies
```

## Key Classes and Relationships

**Gui_control_panel**: Main application controller that initializes:
- Two team controllers (home/away)
- Match state controller
- Joystick controller with configurable button mappings
- Scoreboard window (separate Tkinter Toplevel)

**Match_state_controller**: Central coordinator that maintains shared state between control panel and scoreboard display.

**Joystick Integration**: Uses Pygame with callback system for real-time control. Button mappings are configurable through the `button_config` dictionary.

## Development Notes

- **Threading**: Joystick controller runs on separate threads to avoid UI blocking
- **Window Management**: Scoreboard window cannot be closed independently (shows info dialog instead)
- **Styling**: Uses Tkinter's `xpnative` theme with custom styles for scoreboard components
- **State Synchronization**: All UI updates flow through the shared `Match_state` object
- **Component Organization**: UI components are modular with clear separation between control panel and scoreboard displays

## Dependencies

Core dependencies from requirements.txt:
- `tkinter` (built-in) - Main GUI framework
- `pygame` - Joystick input handling
- `pillow` - Image processing for team logos
- Additional multimedia libraries for enhanced functionality

## Current Development Branch

Working on `Improve-juan` branch with recent refactoring work on:
- ComboBox implementation improvements
- Button configuration for play/Xbox controls
- Timer management functionality