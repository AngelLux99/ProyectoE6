import ISS_Info, turtle, time, threading, math, socket, sys, pickle


def Envio():
    # Crear socket
    socketAbierto = socket.socket()
     
    # Nombre del equipo (o IP), en blanco para localhost
    # para recibir conexiones externas
    equipo = 'localhost'
    # Puerto de escucha del servidor
    puerto = 2423
     
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
        azMod = str(round(azimut,1))
        elMod = str(round(elevacion,1))
        dato = ([azMod, elMod])
        dato_string = pickle.dumps(dato)
        connection.send(dato_string)
        # Cerrar el socket
        connection.close()

if __name__ == '__main__':
    t = threading.Thread(target=Envio)
    t.start()
    
    screen = turtle.Screen() #Creamos la ventana emergente
    screen.title("ISS TRACKER") #Titulo de la ventana
    screen.setup(720, 360) #Indicamos el tamanio de la ventana dependiendo de la imagen que utilicemos
    screen.colormode(255) #habilitamos para utilizar configuracion RGB
    screen.setworldcoordinates(-180,-90,180,90) #indicamos las coordenadas maximas y minimas de latitud y longitud
    screen.bgpic("world.png") #ponemos la imagen de mapamundi como fondo de la ventana
    screen.register_shape("iss.gif") #indicamos el icono que representara al satelite


    iss = turtle.Turtle() #creamos el icono de satelite
    iss.shape("iss.gif") #ponemos la imagen del satelite como el icono
    iss.penup()

    lonG = math.radians(-90.51327)
    latG = math.radians(14.64072)
    r = 6378
    h = 425


    while True:
        try:
            location = ISS_Info.iss_current_loc() #pedimos los datos de la estacion espacial
            lat = float(location['iss_position']['latitude']) # extraemos la latitud de la cadena de datos que recibimos
            lon = float(location['iss_position']['longitude']) #extraemos la longitud de la cadena de datos
            screen.title("ISS TRACKER: (Latitude: {}, Longitude: {})".format(lat,lon)) #modificamos el titulo agregando latitud y longitud
            iss.goto(float(lon),float(lat)) #movemos el icono a las coordenadas correspondientes
            iss.dot(2, 255, 0, 0) #dejamos trazado el recorrido del satelite
            latRad = math.radians(lat)
            lonRad = math.radians(lon)
            
            if lon >= -100.51327 and lon <= -80.51327 and lat >= 4.64072 and lat <= 24.64072:
                x = latRad - latG
                if x == 0:
                    x = 0.000000001
                y = lonRad - lonG
                
                
                if x >= 0 and y >= 0:
                    azimut = math.degrees(math.atan(y/x))
                elif x <= 0 and y >= 0:
                    azimut = 180 + math.degrees(math.atan(y/x))
                elif x <= 0 and y <= 0:
                    azimut = 180 + math.degrees(math.atan(y/x))
                elif x >= 0 and y <= 0:
                    azimut = 360 + math.degrees(math.atan(y/x))
                print("Azimut: %0.2f" %azimut)
                
                a = math.sin(x/2)**2 + math.cos(latG)*math.cos(latRad)*(math.sin(y/2)**2)
                r2 = 2*r*math.asin(math.sqrt(a))    
                rho = math.sqrt((r2**2)+(h**2))
                
                elevacion = 90 - math.degrees(math.acos(h/rho))    
                print("Elevacion: %0.2f" %elevacion)
                
            else:
                azimut = 0
                elevacion = 0
                print("Fuera de rango")

            
            print("(Latitud: {}, Longitud: {})".format(lat,lon))
            
            time.sleep(5) #repetimos cada 5 segundos
        except Exception as e:
            print(str(e))
            break
        
