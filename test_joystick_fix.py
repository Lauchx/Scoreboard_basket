#!/usr/bin/env python3
"""
Script de prueba para verificar que el sistema de mapeo de botones funciona correctamente
después de las correcciones para controladores PlayStation.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controller.button_mapper import ButtonMapper, ControllerType, AbstractButton, DEFAULT_SCOREBOARD_ACTIONS, create_button_mapper

def test_button_mapping():
    print("=== PRUEBA DE MAPEO DE BOTONES ===\n")

    # Probar con controlador Xbox
    print("1. Probando mapeo para XBOX:")
    xbox_mapper = create_button_mapper(controller_type=ControllerType.XBOX)

    print(f"   Tipo: {xbox_mapper.controller_type.value}")
    print(f"   Botones mapeados: {len(xbox_mapper.current_mapping)}")

    # Probar botones principales
    for abstract_btn in [AbstractButton.LEFT_BUMPER, AbstractButton.RIGHT_BUMPER,
                         AbstractButton.ACTION_BOTTOM, AbstractButton.ACTION_RIGHT]:
        physical_btn = xbox_mapper.get_physical_button(abstract_btn)
        display_name = xbox_mapper.get_display_name(abstract_btn)
        print(f"   {abstract_btn.value}: {display_name} -> botón físico {physical_btn}")

    # Probar mapeo de acciones
    xbox_action_mapping = xbox_mapper.create_action_mapping(DEFAULT_SCOREBOARD_ACTIONS)
    print(f"   Mapeo de acciones: {len(xbox_action_mapping)} acciones configuradas")

    print("\n" + "="*50 + "\n")

    # Probar con controlador PlayStation
    print("2. Probando mapeo para PLAYSTATION:")
    ps_mapper = create_button_mapper(controller_type=ControllerType.PLAYSTATION)

    print(f"   Tipo: {ps_mapper.controller_type.value}")
    print(f"   Botones mapeados: {len(ps_mapper.current_mapping)}")

    # Probar botones principales
    for abstract_btn in [AbstractButton.LEFT_BUMPER, AbstractButton.RIGHT_BUMPER,
                         AbstractButton.ACTION_BOTTOM, AbstractButton.ACTION_RIGHT]:
        physical_btn = ps_mapper.get_physical_button(abstract_btn)
        display_name = ps_mapper.get_display_name(abstract_btn)
        print(f"   {abstract_btn.value}: {display_name} -> botón físico {physical_btn}")

    # Probar mapeo de acciones
    ps_action_mapping = ps_mapper.create_action_mapping(DEFAULT_SCOREBOARD_ACTIONS)
    print(f"   Mapeo de acciones: {len(ps_action_mapping)} acciones configuradas")

    print("\n" + "="*50 + "\n")

    # Verificar que los botones físicos son diferentes entre Xbox y PlayStation
    print("3. Verificación de diferencias entre controladores:")

    for abstract_btn in [AbstractButton.LEFT_BUMPER, AbstractButton.RIGHT_BUMPER]:
        xbox_btn = xbox_mapper.get_physical_button(abstract_btn)
        ps_btn = ps_mapper.get_physical_button(abstract_btn)

        print(f"   {abstract_btn.value}:")
        print(f"     Xbox: {xbox_btn}")
        print(f"     PlayStation: {ps_btn}")
        print(f"     [OK] Diferentes: {xbox_btn != ps_btn}")

    print("\n" + "="*50 + "\n")

    # Probar detección automática (si hay joysticks conectados)
    print("4. Probando detección de joysticks:")
    try:
        import pygame
        pygame.init()
        pygame.joystick.init()

        joystick_count = pygame.joystick.get_count()
        print(f"   Joysticks detectados: {joystick_count}")

        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            controller_name = joystick.get_name()

            # Probar detección automática
            test_mapper = ButtonMapper()
            detected_type = test_mapper.detect_controller_type(controller_name)

            print(f"   Joystick {i}: {controller_name}")
            print(f"     Tipo detectado: {detected_type.value}")

        pygame.quit()

    except Exception as e:
        print(f"   Error en detección de joysticks: {e}")

    print("\n=== FIN DE LA PRUEBA ===")

if __name__ == "__main__":
    test_button_mapping()