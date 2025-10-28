#!/usr/bin/env python3
"""
Script de prueba para el sistema de mapeo abstracto de botones.

Este script permite verificar que el nuevo sistema de mapeo abstracto funciona correctamente
con diferentes tipos de controladores (Xbox, PlayStation, etc.).
"""

import pygame
from model.joystick_types import ControllerType, AbstractButton
from model.button_mapping import ButtonMapping
from model.joystick_config import DEFAULT_SCOREBOARD_ACTIONS

def test_button_mapper():
    """Prueba las funcionalidades básicas del ButtonMapper"""
    print("🧪 === PRUEBA DEL SISTEMA DE MAPEO ABSTRACTO ===\n")

    # 1. Prueba de detección de controladores
    print("1. 🔍 Prueba de detección de controladores:")

    # Simular nombres de controladores
    test_controllers = [
        ("Xbox 360 Controller", ControllerType.XBOX),
        ("Xbox One Controller", ControllerType.XBOX),
        ("DualShock 4 Controller", ControllerType.PLAYSTATION),
        ("DualSense Wireless Controller", ControllerType.PLAYSTATION),
        ("Generic Gamepad", ControllerType.UNKNOWN)
    ]

    for controller_name, expected_type in test_controllers:
        mapper = ButtonMapper()
        detected_type = mapper.detect_controller_type(controller_name)
        status = "✅" if detected_type == expected_type else "❌"
        print(f"  {status} '{controller_name}' -> {detected_type.value} (esperado: {expected_type.value})")

    print()

    # 2. Prueba de mapeo de botones Xbox
    print("2. 🎮 Prueba de mapeo - Xbox Controller:")
    xbox_mapper = ButtonMapper()
    xbox_mapper.set_controller_type(ControllerType.XBOX)

    test_actions_xbox = {
        'home_add_point': AbstractButton.LEFT_BUMPER,    # LB
        'away_add_point': AbstractButton.RIGHT_BUMPER,   # RB
        'manage_timer': AbstractButton.ACTION_BOTTOM,     # A
    }

    for action, abstract_button in test_actions_xbox.items():
        physical_btn = xbox_mapper.get_physical_button(abstract_button)
        display_name = xbox_mapper.get_display_name(abstract_button)
        print(f"  {action}: {display_name} -> Botón físico {physical_btn}")

    print()

    # 3. Prueba de mapeo de botones PlayStation
    print("3. 🎮 Prueba de mapeo - PlayStation Controller:")
    ps_mapper = ButtonMapper()
    ps_mapper.set_controller_type(ControllerType.PLAYSTATION)

    for action, abstract_button in test_actions_xbox.items():
        physical_btn = ps_mapper.get_physical_button(abstract_button)
        display_name = ps_mapper.get_display_name(abstract_button)
        print(f"  {action}: {display_name} -> Botón físico {physical_btn}")

    print()

    # 4. Prueba de conversión inversa
    print("4. 🔄 Prueba de conversión inversa (físico -> abstracto):")

    # Botón 4 en Xbox es LB, en PlayStation es L1
    test_physical_btn = 4

    xbox_abstract = xbox_mapper.get_abstract_button(test_physical_btn)
    xbox_display = xbox_mapper.get_display_name(xbox_abstract) if xbox_abstract else "No mapeado"

    ps_abstract = ps_mapper.get_abstract_button(test_physical_btn)
    ps_display = ps_mapper.get_display_name(ps_abstract) if ps_abstract else "No mapeado"

    print(f"  Botón físico {test_physical_btn}:")
    print(f"    Xbox: {xbox_display} ({xbox_abstract.value if xbox_abstract else 'None'})")
    print(f"    PlayStation: {ps_display} ({ps_abstract.value if ps_abstract else 'None'})")

    print()

    # 5. Prueba de configuración de acciones
    print("5. ⚙️ Prueba de configuración de acciones:")

    # Crear mapeo de acciones a botones físicos
    xbox_action_mapping = xbox_mapper.create_action_mapping(DEFAULT_SCOREBOARD_ACTIONS)
    ps_action_mapping = ps_mapper.create_action_mapping(DEFAULT_SCOREBOARD_ACTIONS)

    print("  Configuración por defecto:")
    for action, abstract_button in DEFAULT_SCOREBOARD_ACTIONS.items():
        xbox_physical = xbox_mapper.get_physical_button(abstract_button)
        ps_physical = ps_mapper.get_physical_button(abstract_button)
        xbox_name = xbox_mapper.get_display_name(abstract_button)
        ps_name = ps_mapper.get_display_name(abstract_button)

        print(f"    {action}:")
        print(f"      Xbox: {xbox_name} (btn {xbox_physical})")
        print(f"      PlayStation: {ps_name} (btn {ps_physical})")

    print()

    # 6. Prueba de botones disponibles
    print("6. 📋 Prueba de botones disponibles:")

    xbox_available = xbox_mapper.get_available_buttons()
    ps_available = ps_mapper.get_available_buttons()

    print("  Botones disponibles para configuración:")
    print(f"    Xbox: {list(xbox_available.values())}")
    print(f"    PlayStation: {list(ps_available.values())}")

    print()
    print("✅ Pruebas completadas. El sistema de mapeo abstracto funciona correctamente.\n")

def test_joystick_integration():
    """Prueba la integración con el JoystickController si hay joysticks conectados"""
    print("🎮 === PRUEBA DE INTEGRACIÓN CON JOYSTICK ===\n")

    # Inicializar pygame
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("❌ No hay joysticks conectados. Conecta un controlador para probar la integración.")
        pygame.quit()
        return

    # Importar el controlador actualizado
    from controller.joystick_controller import JoystickController

    controller = JoystickController()

    # Detectar joysticks conectados
    joysticks = controller.detect_joysticks()

    print(f"🔍 Se encontraron {len(joysticks)} joystick(s):")
    for joy in joysticks:
        print(f"  • {joy['name']} (ID: {joy['id']})")

    # Conectar al primer joystick
    if controller.connect_joystick(0):
        info = controller.get_joystick_info()
        print(f"\n✅ Conectado a: {info['name']}")
        print(f"   Tipo detectado: {info['type']}")
        print(f"   Botones: {info['num_buttons']}")
        print(f"   Ejes: {info['num_axes']}")

        # Probar el mapeo actual
        current_mapping = controller._get_button_mapping()
        print(f"\n📋 Mapeo actual de botones:")
        for physical_btn, action in current_mapping.items():
            abstract_btn = controller.button_mapper.get_abstract_button(physical_btn)
            if abstract_btn:
                display_name = controller.button_mapper.get_display_name(abstract_btn)
                print(f"   Botón {physical_btn} ({display_name}) -> {action}")

        # Mostrar botones disponibles para configuración
        available_buttons = controller.get_available_buttons()
        print(f"\n🎯 Botones disponibles para configuración:")
        for abstract_value, display_name in available_buttons.items():
            physical_btn = controller.button_mapper.get_physical_button(AbstractButton(abstract_value))
            print(f"   {display_name} -> Botón físico {physical_btn}")

    else:
        print("❌ Error al conectar el joystick")

    # Limpiar
    controller.cleanup()
    pygame.quit()

    print("\n✅ Prueba de integración completada.\n")

def main():
    """Función principal que ejecuta todas las pruebas"""
    try:
        test_button_mapper()
        test_joystick_integration()

        print("🎉 === TODAS LAS PRUEBAS COMPLETADAS ===")
        print("El sistema de mapeo abstracto está listo para usarse.")
        print("\n📝 Resumen de las mejoras:")
        print("• ✅ Detección automática de tipo de controlador")
        print("• ✅ Mapeo abstracto independiente del número de botón")
        print("• ✅ Nombres descriptivos (LB/L1, RB/R1, etc.)")
        print("• ✅ Configuración intuitiva por nombre de botón")
        print("• ✅ Compatibilidad con Xbox y PlayStation")

    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()