from hub import port
import runloop
import motor_pair
import motor, time

async def main():

    motor_pair.pair(motor_pair.PAIR_1, port.C, port.D)

    def subir():
        motor.run(port.A, 365)
        time.sleep_ms(365)
        motor.stop(port.A)

    def bajar():
        motor.run(port.A, -365)
        time.sleep_ms(365)
        motor.stop(port.A)
    
    def girar_izquierda():
        motor_pair.move_for_degrees(motor_pair.PAIR_1, -200, 90, velocity=1000)

    def girar_derecha():
        motor_pair.move_for_degrees(motor_pair.PAIR_1, 200, 90, velocity=1000)

    def avanzar_grados(grados):
        motor_pair.move_for_degrees(motor_pair.PAIR_1, grados, 0, velocity=1000)

    def retroceder_grados(grados):
        motor_pair.move_for_degrees(motor_pair.PAIR_1, -grados, 0, velocity=1000)

    def pausa():
        time.sleep(2)

    avanzar_grados(1900)
    pausa()

    girar_izquierda()
    pausa()

    avanzar_grados(1500)
    pausa()

    bajar()
    pausa()

    retroceder_grados(1300)
    pausa()

    girar_derecha()
    pausa()

    avanzar_grados(1300)
    pausa()

    girar_izquierda()
    pausa()

    avanzar_grados(1300)
    pausa()

    girar_derecha()
    pausa()

    avanzar_grados(700)
    pausa()

    subir()
    pausa()

    retroceder_grados(1000)
    pausa()

runloop.run(main())