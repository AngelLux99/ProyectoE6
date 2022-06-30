# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# LSM303DLHC
# This code is designed to work with the LSM303DLHC_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/products
 
import smbus, time, math, turtle, socket, sys, pickle, threading


def Modulo():
    # Crear socket
    socketAbierto = socket.socket()
     
    # Nombre del equipo (o IP), en blanco para localhost
    # para recibir conexiones externas
    equipo = 'localhost'
    # Puerto de escucha del servidor
    puerto = 2324
     
    try:
    #     """
    #     El método bind conecta el socket en una tupla que especifica
    #     una dirección y un puerto
    #     """
        socketAbierto.bind((equipo, puerto))
    except socket.error as message:
        print("Falló la escucha por el puerto ", puerto)
        print(message)
        sys.exit()
    # Iniciamos la escucha
    socketAbierto.listen()
    print("Escuchando en el puerto: ", puerto)
    
    while True:
        # A la espera de una conexión de un cliente
        connection,address = socketAbierto.accept()
    #     print("Cliente ", address[0],address[1], " conectado")
        # Enviar un mensaje al cliente conectado
        azMod = str(round(az,1))
        elMod = str(round(el,1))
        dato = ([azMod, elMod])
        dato_string = pickle.dumps(dato)
        connection.send(dato_string)
        # Cerrar el socket
        connection.close()



if __name__ == '__main__':
    az = 0
    el = 0
    
    Modulo = threading.Thread(target = Modulo)
    Modulo.start()
    
    screen = turtle.Screen()
    screen.title("AZIMUT, ELEVACION")
    screen.setup(520, 320)
    screen.colormode(255)
    screen.bgpic("brujula1.png")


    flecha = turtle.Turtle()
    flecha.pencolor(255, 0, 0)
    flecha.turtlesize(2,3,3)
    flecha.penup()
    
    flecha2 = turtle.Turtle()
    flecha2.pencolor(0, 255, 0)
    flecha2.turtlesize(2,3,3)
    flecha2.penup()
    

    

    

         
    while True:
    # Get I2C bus
        bus = smbus.SMBus(1)
         
        # LSM303DLHC Accl address, 0x19(25)
        # Select control register1, 0x20(32)
        #		0x27(39)	Acceleration data rate = 10Hz, Power ON, X, Y, Z axis enabled
        bus.write_byte_data(0x19, 0x20, 0x27)
        # LSM303DLHC Accl address, 0x19(25)
        # Select control register4, 0x23(35)
        #		0x00(00)	Continuos update, Full scale selection = +/-2g,
        bus.write_byte_data(0x19, 0x23, 0x00)
         
        time.sleep(0.5)
         
        # LSM303DLHC Accl address, 0x19(25)
        # Read data back from 0x28(40), 2 bytes
        # X-Axis Accl LSB, X-Axis Accl MSB
        data0 = bus.read_byte_data(0x19, 0x28)
        data1 = bus.read_byte_data(0x19, 0x29)
         
        # Convert the data
        xAccl = data1 * 256 + data0
        if xAccl > 32767 :
            xAccl -= 65536
         
        # LSM303DLHC Accl address, 0x19(25)
        # Read data back from 0x2A(42), 2 bytes
        # Y-Axis Accl LSB, Y-Axis Accl MSB
        data0 = bus.read_byte_data(0x19, 0x2A)
        data1 = bus.read_byte_data(0x19, 0x2B)
         
        # Convert the data
        yAccl = data1 * 256 + data0
        if yAccl > 32767 :
            yAccl -= 65536
         
        # LSM303DLHC Accl address, 0x19(25)
        # Read data back from 0x2C(44), 2 bytes
        # Z-Axis Accl LSB, Z-Axis Accl MSB
        data0 = bus.read_byte_data(0x19, 0x2C)
        data1 = bus.read_byte_data(0x19, 0x2D)
         
        # Convert the data
        zAccl = data1 * 256 + data0
        if zAccl > 32767 :
            zAccl -= 65536
         
        # LSM303DLHC Mag address, 0x1E(30)
        # Select MR register, 0x02(02)
        #		0x00(00)	Continous conversion mode
        bus.write_byte_data(0x1E, 0x02, 0x00)
        # LSM303DLHC Mag address, 0x1E(30)
        # Select CRA register, 0x00(00)
        #		0x10(16)	Temperatuer disabled, Data output rate = 15Hz
        bus.write_byte_data(0x1E, 0x00, 0x10)
        # LSM303DLHC Mag address, 0x1E(30)
        # Select CRB register, 0x01(01)
        #		0x20(32)	Gain setting = +/- 1.3g
        bus.write_byte_data(0x1E, 0x01, 0x20)
         
        time.sleep(0.5)
         
        # LSM303DLHC Mag address, 0x1E(30)
        # Read data back from 0x03(03), 2 bytes
        # X-Axis Mag MSB, X-Axis Mag LSB
        data0 = bus.read_byte_data(0x1E, 0x03)
        data1 = bus.read_byte_data(0x1E, 0x04)
         
        # Convert the data
        xMag = data0 * 256 + data1
        if xMag > 32767 :
            xMag -= 65536
        elif xMag == 0:
            xMag = 0.0000000001
         
        # LSM303DLHC Mag address, 0x1E(30)
        # Read data back from 0x05(05), 2 bytes
        # Y-Axis Mag MSB, Y-Axis Mag LSB
        data0 = bus.read_byte_data(0x1E, 0x07)
        data1 = bus.read_byte_data(0x1E, 0x08)
         
        # Convert the data
        yMag = data0 * 256 + data1
        if yMag > 32767 :
            yMag -= 65536
         
        # LSM303DLHC Mag address, 0x1E(30)
        # Read data back from 0x07(07), 2 bytes
        # Z-Axis Mag MSB, Z-Axis Mag LSB
        data0 = bus.read_byte_data(0x1E, 0x05)
        data1 = bus.read_byte_data(0x1E, 0x06)
         
        # Convert the data
        zMag = data0 * 256 + data1
        if zMag > 32767 :
            zMag -= 65536
         
        az = math.degrees(math.atan(yMag/xMag))

        
        if xMag >= 0 and yMag >= 0:
            az = az
            
        elif xMag <= 0 and yMag >= 0:
            az = 180 + az
            
        elif xMag <= 0 and yMag <= 0:
            az = 180 + az
            
        elif xMag >= 0 and yMag <= 0:
            az = az + 360
        
        

        el = math.degrees(math.atan(xAccl/math.sqrt(yAccl**2 + zAccl**2)))
        

        print ("AZIMUT: %d, ELEVACION: %d" %(az, el))


        orien = 90 - az
        radio = 135
        teta = math.radians(az)
        xVec = radio*math.sin(teta)
        yVec = radio*math.cos(teta)
        

        flecha.seth(orien)
        flecha.goto(xVec, yVec)
        
        orienEl = el
        radioEl = 80
        tetaEl = math.radians(el)
        yVecEl = radioEl*math.sin(tetaEl)
        xVecEl = radioEl*math.cos(tetaEl)
        screen.title("AZIMUT: %d, ELEVACION: %d" %(az, el))

        flecha2.seth(orienEl)
        flecha2.goto(xVecEl, yVecEl)
         
        time.sleep(0.002)

GraficaAz.join()
GraficaEl.join()



