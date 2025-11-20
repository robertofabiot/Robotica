from hub import port
import runloop
import motor_pair
import motor
import color_sensor
import color
from hub import light_matrix, sound
import distance_sensor

# --- 1. DEFINICIÓN DE PUERTOS Y CONSTANTES ---
motor_izquierda = port.A
motor_derecha = port.C
#puerto_garra = port.A
puerto_sensor_color = port.B
#puerto_sensor_ultrasonico = port.C

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
async def subir_garra(grados: int = 90, velocidad: int = 365) -> None:
    """Sube la garra. Usa grados positivos."""
    await motor.run_for_degrees(puerto_garra, grados, velocidad)

async def bajar_garra(grados: int = 90, velocidad: int = 365) -> None:
    """Baja la garra. El valor de grados ingresado debe ser positivo."""
    await motor.run_for_degrees(puerto_garra, -grados, velocidad)

# --- 4. FUNCIONES PARA GIROS ---
# Usan el par de motores para giros más controlados (giro en arco o sobre el eje).
async def girar_derecha_fase(grados: int = 200, direccion: int = 90, velocidad: int = 1000) -> None:
    """Gira en fase a la derecha según grados de motor."""
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, grados, direccion, velocity=velocidad)

async def girar_izquierda_fase(grados: int = 200, direccion: int = 90, velocidad: int = 1000) -> None:
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

# --- 7. FUNCIONES SENSOR DE COLOR ---
async def avanzar_hasta_detectar_color(color) -> None:
    while color_sensor.color(puerto_sensor_color) != color:
        avanzar_indefinidamente()
        runloop.sleep_ms(1)
    motor_pair.stop(motor_pair.PAIR_1)

# --- 8. FUNCIONES SENSOR ULTRASÓNICO ---
async def avanzar_hasta_distancia(distancia_obj_mm: int) -> None:
    while True:
        distancia_actual_mm = distance_sensor.distance(puerto_sensor_ultrasonico)

        if distancia_actual_mm <= distancia_obj_mm:
            motor_pair.stop(motor_pair.PAIR_1)
            await pausa()
            break
        await runloop.sleep_ms(50)

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

    await avanzar_cm(5)
    while True:
        if(color_sensor.color(puerto_sensor_color) == color.BLACK):
            motor.run(motor_izquierda, -600)
            motor.run(motor_derecha, 400)
        if(color_sensor.color(puerto_sensor_color) == color.WHITE):
            motor.run(motor_izquierda, -400)
            motor.run(motor_derecha, 600)
        if(color_sensor.color(puerto_sensor_color) == color.RED):
            break
        await runloop.sleep_ms(1)
    motor.stop(motor_derecha)
    motor.stop(motor_izquierda)

# Acá se llama a la función main definida.
runloop.run(main())