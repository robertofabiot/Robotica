from hub import port
import runloop
import motor_pair
import motor
import color_sensor
import color
from hub import light_matrix, sound
import time

# --- 1. DEFINICIÓN DE PUERTOS Y CONSTANTES ---
motor_izquierda = port.C
motor_derecha = port.D
puerto_garra = port.B

# CONSTANTES FÍSICAS (clave para la clase de conversiones)
CIRCUNFERENCIA_RUEDA = 17.58 # float
GRADOS_POR_ROTACION = 360 # int

# --- 2. FUNCIÓN DE CONVERSIÓN ---
def cm_a_grados(cm: float) -> int:
    """Convierte centímetros a grados de motor usando la circunferencia de la rueda."""
    # Fórmula: (Distancia * 360) / Circunferencia
    grados_float = (cm * GRADOS_POR_ROTACION) / CIRCUNFERENCIA_RUEDA
    return round(grados_float)

# --- 3. FUNCIONES PARA GARRA ---
async def subir_garra() -> None:
    """Sube la garra."""
    motor.run(puerto_garra, 365) #Empieza a girar el motor del puerto A a una velocidad de 365
    await pausa(0.4) #Espera durante 365 milisegundos
    motor.stop(puerto_garra) #Detiene el motor

async def bajar_garra() -> None:
    """Baja la garra."""
    motor.run(puerto_garra, -365)
    await pausa(0.4)
    motor.stop(puerto_garra)

# --- 4. FUNCIONES PARA GIROS ---
# Usan el par de motores para giros más controlados (giro en arco o sobre el eje).
async def girar_derecha_fase(grados: int = 210, direccion: int = 100, velocidad: int = 1000) -> None:
    """Gira en fase a la derecha según grados de motor."""
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, grados, direccion, velocity=velocidad)

async def girar_izquierda_fase(grados: int = 210, direccion: int = 100, velocidad: int = 1000) -> None:
    """Gira en fase según grados de motor."""
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -grados, direccion, velocity=velocidad)

# Funciones de giro en desfase (giro sobre una rueda)
# Pendiente por ajustar grados
async def girar_derecha_desfase(grados: int = 90, velocidad: int = 500) -> None:
    """Gira a la derecha moviendo solo el motor izquierdo (desfase)."""
    motor.run(motor_izquierda, -500)
    await pausa(0.8)
    motor.stop(motor_izquierda, stop=motor.BRAKE)

async def girar_izquierda_desfase(grados: int = 90, velocidad: int = 500) -> None:
    """Gira a la izquierda moviendo solo el motor derecho (desfase)."""
    motor.run(motor_derecha, 500)
    await pausa(0.8)
    motor.stop(motor_derecha, stop=motor.BRAKE)


# --- 5. FUNCIONES DE AVANCE (usan la conversión a float) ---
async def avanzar_cm(cm: float, velocidad: int = 500) -> None:
    """Avanza recto la cantidad de cm especificada, usando la fórmula de conversión."""
    grados = cm_a_grados(cm)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, grados, 0, velocity=velocidad)

async def retroceder_cm(cm: float, velocidad: int = 500) -> None:
    """Retrocede recto la cantidad de cm especificada."""
    grados = cm_a_grados(cm)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -grados, 0, velocity=velocidad)

async def avanzar_grados(grados: int, velocidad: int = 500) -> None:
    """Avanza recto la cantidad de grados de motor especificada."""
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, grados, 0, velocity=velocidad)

async def retroceder_grados(grados: int, velocidad: int = 500) -> None:
    """Retrocede recto la cantidad de grados de motor especificada (valor negativo)."""
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -grados, 0, velocity=velocidad)

async def avanzar_rotaciones(rotaciones: int, velocidad: int = 500) -> None:
    """Avanza recto la cantidad de rotaciones especificadas."""
    grados = GRADOS_POR_ROTACION * rotaciones
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, grados, 0, velocity=velocidad)

async def retroceder_rotaciones(rotaciones: int, velocidad: int = 500) -> None:
    """Retrocede recto la cantidad de rotaciones especificadas."""
    grados = GRADOS_POR_ROTACION * rotaciones
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -grados, 0, velocity=velocidad)

# Funciones de Avance/Retroceso Indefinido (No son awaitable)
def avanzar_indefinidamente(velocidad: int = 500) -> None:
    """Avanza recto indefinidamente (usar stop para detener)."""
    motor_pair.move(motor_pair.PAIR_1, 0, velocity=velocidad)

def retroceder_indefinidamente(velocidad: int = 500) -> None:
    """Retrocede recto indefinidamente (usar stop para detener)."""
    motor_pair.move(motor_pair.PAIR_1, 0, velocity=-velocidad)

# --- 6. FUNCIÓN PAUSA ---
async def pausa(segundos: float = 2) -> None:
    """Pausa asíncrona no bloqueante. Por defecto, 2 segundos."""
    await runloop.sleep_ms(int(segundos * 1000))

async def emote():
    motor.run(motor_derecha, 1000)
    light_matrix.show_image(light_matrix.IMAGE_HAPPY)
    sound.beep(440, 10000, 100)
    await pausa(10)
    motor.stop(motor_derecha)

# --- FUNCIÓN PRINCIPAL Y EJECUCIÓN ---
async def main():
    # Inicialización del par de motores
    motor_pair.pair(motor_pair.PAIR_1, motor_izquierda, motor_derecha)

    light_matrix.show_image(light_matrix.IMAGE_GHOST)

    #Detectar color
    await avanzar_cm(50)
    await pausa()

    await girar_izquierda_fase()
    await pausa()

    await avanzar_cm(48)
    await pausa()

    await girar_derecha_fase()
    await pausa()

    while color_sensor.color(port.A) != color.GREEN:
        avanzar_indefinidamente()
        runloop.sleep_ms(1)
    motor_pair.stop(motor_pair.PAIR_1)
    await pausa()

    #Recoger bloque1
    await retroceder_cm(72)
    await pausa()

    await girar_derecha_fase()
    await pausa()

    await avanzar_cm(20)
    await pausa()

    await bajar_garra()
    await pausa()

    #Dejar bloque1
    await retroceder_cm(35)
    await pausa()

    await girar_izquierda_fase()
    await pausa()

    await avanzar_cm(70)
    await pausa()

    await girar_derecha_fase()
    await pausa()

    await avanzar_cm(15)
    await pausa()

    await subir_garra()
    await pausa()
    #FUNCIONÓ HASTA AQUÍ

    #Recoger bloque2
    await retroceder_cm(10)
    await pausa()

    await girar_izquierda_fase()
    await pausa()

    await avanzar_cm(30)
    await pausa()

    await girar_derecha_fase()
    await pausa()

    await avanzar_cm(10)
    await pausa()



    await bajar_garra()
    await pausa()


    #Dejar bloque2
    await avanzar_cm(50)
    await pausa()

    await subir_garra()
    await pausa()

    #Emote
    await retroceder_cm(10)
    await pausa()

    await emote()



# Acá se llama a la función main definida.
runloop.run(main())