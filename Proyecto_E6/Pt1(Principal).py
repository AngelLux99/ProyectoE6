import RPi.GPIO as GPIO
import time, socket, sys, pickle
from multiprocessing import Process, Value

 
in1 = 11
in2 = 12
in3 = 13
in4 = 15
in5 = 31
in6 = 33
in7 = 35
in8 = 37
startaz = 0
startel = 0


    # setting up
GPIO.setwarnings(False)
GPIO.setmode( GPIO.BOARD )
GPIO.setup( in1, GPIO.OUT )
GPIO.setup( in2, GPIO.OUT )
GPIO.setup( in3, GPIO.OUT )
GPIO.setup( in4, GPIO.OUT )
GPIO.setup( in5, GPIO.OUT )
GPIO.setup( in6, GPIO.OUT )
GPIO.setup( in7, GPIO.OUT )
GPIO.setup( in8, GPIO.OUT )

    # initializing
GPIO.output( in1, GPIO.LOW )
GPIO.output( in2, GPIO.LOW )
GPIO.output( in3, GPIO.LOW )
GPIO.output( in4, GPIO.LOW )
GPIO.output( in5, GPIO.LOW )
GPIO.output( in6, GPIO.LOW )
GPIO.output( in7, GPIO.LOW )
GPIO.output( in8, GPIO.LOW )
     


def validar_az(azimut):
    if azimut >= 0 and azimut <= 360:
        return True
    else:
        return False

def validar_el(elevacion):
    if elevacion >= 0 and elevacion <= 90:
        return True
    else:
        return False
    

def Modulo(azMod, elMod):

    # Crear socket
    while True:
        socketConexion = socket.socket()
        
        # Servidor de conexin
        servidor = 'localhost'
        # El puerto a utilizar (el servidor debe estar escuchando en este puerto)
        puerto = 2324


        try:
            # Conectar el socket del cliente con el servidor en el puerto indicado
            socketConexion.connect((servidor, puerto))
        except socket.error as message:
            print("Fallo la conexion con el servidor {} por el puerto {}".format(servidor, puerto))
            print(message)
            sys.exit()  
         
        # Recibir y mostrar el mensaje del servidor
        mensajeServidor = socketConexion.recv(4096)
        dato = pickle.loads(mensajeServidor)
        
        
        azimut = float(dato[0])
        elevacion = float(dato[1])
        azMod.value = azimut
        elMod.value = elevacion

        # Cerrar el socket
        socketConexion.close()
        time.sleep(0.5)
        
def Satelite(azSat, elSat):

    # Crear socket
    while True:
        socketConexion = socket.socket()
        
        # Servidor de conexin
        servidor = 'localhost'
        # El puerto a utilizar (el servidor debe estar escuchando en este puerto)
        puerto = 2423


        try:
            # Conectar el socket del cliente con el servidor en el puerto indicado
            socketConexion.connect((servidor, puerto))
        except socket.error as message:
            print("Fallo la conexion con el servidor {} por el puerto {}".format(servidor, puerto))
            print(message)
            sys.exit()  
         
        # Recibir y mostrar el mensaje del servidor
        mensajeServidor = socketConexion.recv(4096)
        dato = pickle.loads(mensajeServidor)
        
        
        azimut = float(dato[0])
        elevacion = float(dato[1])
        azSat.value = azimut
        elSat.value = elevacion

        # Cerrar el socket
        socketConexion.close()
        time.sleep(0.5)

def MotorEl():
    startel = float(eleMod.value)       
    recoel = abs(elevacion-startel)
#     print('recoel %d' %recoel)
    step_count_el = int(abs(recoel)*(4096/360))
    
    if startel <= elevacion:
        directionel = True 

    elif startel >= elevacion:
        directionel = False 
    
    #configuracion del giro de motor en medio paso
    step_sequence = [[1,0,0,1],
                     [1,0,0,0],
                     [1,1,0,0],
                     [0,1,0,0],
                     [0,1,1,0],
                     [0,0,1,0],
                     [0,0,1,1],
                     [0,0,0,1]]


    #vectores para la sustitucion con respecto a la matriz 
    motor_pins_el = [in5,in6,in7,in8]
    motor_step_counter = 0
    
    try:
        #motor encargado de elevacion
        j = 0
        for j in range(step_count_el):
            for pinel in range(0, len(motor_pins_el)):
                GPIO.output( motor_pins_el[pinel], step_sequence[motor_step_counter][pinel] )
            if directionel==True:
                motor_step_counter = (motor_step_counter - 1) % 8
            elif directionel==False:
                motor_step_counter = (motor_step_counter + 1) % 8
            else: 
                print( "el sentido de la direccion debe ser True o False" )
                
                exit( 1 )
            time.sleep( step_sleep )
     
    except KeyboardInterrupt:
        
        exit( 1 )
    GPIO.output( in5, GPIO.LOW )
    GPIO.output( in6, GPIO.LOW )
    GPIO.output( in7, GPIO.LOW )
    GPIO.output( in8, GPIO.LOW )

def MotorAz():
    global recorrido
    
    startaz = float(aziMod.value)
    recorrido = abs(azimut - startaz)
#     print(recorrido)
    

    distancia = abs(azimut - startaz)
#     print(distancia)  

    if distancia <= 180:
        recorrido = distancia
    else:
        recorrido = 360 - distancia
    
    if distancia <= 180:   
        if startaz <= azimut:    
            directionaz = False 

        elif startaz >= azimut:
            directionaz = True 

    elif distancia >= 180:
        if startaz <= azimut:    
            directionaz = True 

        elif startaz >= azimut:
            directionaz = False 

    step_count_az = int(abs(2)*(4096/360)) #conversion de dato ingresado en grados a numero de pasos

    #configuracion del giro de motor en medio paso
    step_sequence = [[1,0,0,1],
                     [1,0,0,0],
                     [1,1,0,0],
                     [0,1,0,0],
                     [0,1,1,0],
                     [0,0,1,0],
                     [0,0,1,1],
                     [0,0,0,1]]


    #vectores para la sustitucion con respecto a la matriz 
    motor_pins_az = [in1,in2,in3,in4]
    motor_step_counter = 0
    
    try:
        #motor encargado del azimut
        i = 0
        for i in range(step_count_az): #dura la cantidad de pasos (grados) que se hayan ingresado
            for pinaz in range(0, len(motor_pins_az)): 
                GPIO.output( motor_pins_az[pinaz], step_sequence[motor_step_counter][pinaz] ) #seleccionamos el pin y el elemento de la matriz 
            if directionaz==True:
                motor_step_counter = (motor_step_counter - 1) % 8 #indicamos si se iniciara de la fila 0 a 7 o de la 7 a 0
                
            elif directionaz==False:
                motor_step_counter = (motor_step_counter + 1) % 8
                
            else: 
                print( "el sentido de la direccion debe ser True o False" )
                cleanup()
                exit( 1 )
            time.sleep( step_sleep )   
    
    except KeyboardInterrupt:
        
        exit( 1 )
    

     
    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.output( in3, GPIO.LOW )
    GPIO.output( in4, GPIO.LOW )


if __name__ == '__main__':
    
    aziMod = Value('f')
    eleMod = Value('f')
    aziSat = Value('f')
    eleSat = Value('f')
    
    datosMod = Process(target = Modulo, args = (aziMod, eleMod,))
    datosMod.start()
    datosSat = Process(target = Satelite, args = (aziSat, eleSat,))
    datosSat.start()
    
    
    
    while True:
        
        
        elMod = eleMod.value
        azMod = aziMod.value
        valido1 = False
        valido2 = False
        
        step_sleep = 0.002
        while True:    
            try:
                seleccion = int(input('Ingrese 0-Reposo, 1-Posicion Manual o 2-Seguimiento del satelite : '))
            except ValueError:
                print('Unicamente se admiten numeros')
                continue
                
            if seleccion == 1:    
                #etapa de ingreso de grados de azimut y elevacion    
                while not valido1:
                    try:
                        azimut = float(input('Ingrese azimut entre 0 & 360: '))# 5.625*(1/64), 4096 pasos son 360°
                    except ValueError:
                        print('Unicamente se admiten numeros')
                        continue
                    valido1 = validar_az(azimut)
                    if not valido1:
                        print('Ingreso un dato incorrecto, porfavor ingresee azimut entre 0 & 360: ')
                
                
                
                while not valido2:
                    try:
                        elevacion = float(input('Ingrese elevacion entre 0 & 90: '))
                    except ValueError:
                        print('Unicamente se admiten numeros')
                        continue
                    valido2 = validar_el(elevacion)
                    if not valido2:
                        print('Ingreso un dato incorrecto, porfavor ingresee elevacion entre 0 & 180: ')
                
                MotorAz()
                MotorEl()
                while recorrido >= 3:
                    MotorAz()
                    time.sleep(0.4)                   
                break
                
            elif seleccion == 0:
                azimut = 0
                elevacion = 0
                MotorEl()
                MotorAz()
                while recorrido >= 3:
                    MotorAz()
                    time.sleep(0.4)                   
                break
        
            elif seleccion == 2:
                elevacion = eleSat.value
                azimut= aziSat.value
                while elevacion == 0:
                    elevacion = eleSat.value
                    azimut= aziSat.value
                    MotorEl()
                    MotorAz()
                    while recorrido >= 3:
                        MotorAz()
                        time.sleep(0.4)                   
                    try:
                        espera = int(input('El satelite se encuentra fuera de rango. Desea seguir esperando? 0-No 1-Si: '))
                    except ValueError:
                        print('Solo se admiten numeros')
                    time.sleep(5)
                    if espera == 1:
                        continue
                    elif espera == 0:
                        break
                    else:
                        print('Ingrese un numero valido')
                        continue
                while elevacion != 0 or azimut != 0:
                    elevacion = eleSat.value
                    azimut= aziSat.value
                    MotorEl()
                    MotorAz()
                    while recorrido >= 3:
                        MotorAz()
                        time.sleep(0.4)
                    print('Se encuentra en seguimiento del satelite')
#                     print('Posicion del satelite: AZIMUT: %d, ELEVACION: %d' %(azimut, elevacion))
#                     print('Posicion de antena: AZIMUT: %d, ELEVACION: %d' %(azMod, elMod))
                    time.sleep(5)
            else:
                print('Ingrese una opcion correcta')
                continue

    exit( 0 )
