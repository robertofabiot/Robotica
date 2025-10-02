#Se importan los módulos necesarios para que el programa reconozca el hub y sus puertos
from hub import port
import runloop
import motor_pair
import motor, time

#Se crea una función main. 
async def main():

    #Se define el par de motores. Se le asigna el par 1. En este caso,
    #el puerto C es el izquierdo y el D el derecho.
    motor_pair.pair(motor_pair.PAIR_1, port.C, port.D)

    #Función para subir la garra
    def subir(): 
        motor.run(port.A, 365) #Empieza a girar el motor del puerto A a una velocidad de 365
        time.sleep_ms(365) #Espera durante 365 milisegundos
        motor.stop(port.A) #Detiene el motor

    #Lo mismo del anterior, pero se pone el - a la velocidad para que el motor gire en
    #sentido contrario
    def bajar():
        motor.run(port.A, -365)
        time.sleep_ms(365)
        motor.stop(port.A)
    
    #Gira a la izquierda con el par de motores. Gira durante -200 grados del motor, 
    #con dirección 90 y velocidad de 1000
    def girar_izquierda():
        motor_pair.move_for_degrees(motor_pair.PAIR_1, -200, 90, velocity=1000)

    #Lo mismo que el anterior, pero con grados del motor positivos.
    def girar_derecha():
        motor_pair.move_for_degrees(motor_pair.PAIR_1, 200, 90, velocity=1000)

    #Avanza ambos motores. Recibe como parámetro los grados a avanzar. Su dirección
    #es 0 (va recto) y su velocidad es de 1000.
    def avanzar_grados(grados):
        motor_pair.move_for_degrees(motor_pair.PAIR_1, grados, 0, velocity=1000)

    #Lo mismo que el anterior, pero los grados son negativos.
    def retroceder_grados(grados):
        motor_pair.move_for_degrees(motor_pair.PAIR_1, -grados, 0, velocity=1000)

    #Simplemente da tiempo al robot de parar los motores antes de ejecutar otra acción
    #Espera 2 segundos
    def pausa():
        time.sleep(2)

    #A partir de aquí solo es llamar las funciones ya definidas con los parámetros necesarios
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

#Acá se llama a la función main definida. Sin esto no se ejecuta nada
runloop.run(main())