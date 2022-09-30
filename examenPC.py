import threading
import time



palillos = []
cant_personas = 8;

def estadoPalillo(persona):
    

    palillo_izq = palillos[persona]                       #Asignamos el palillo correspondiete de cada persona
    palillo_der = palillos[(persona - 1) % cant_personas] #al compartir el palillo se hace de una manera circular

    palillo_izq.acquire()

    if palillo_der.acquire(blocking=False):               #si se obtienen los dos palillos se desbloquea el palillo derecho
        print(f"Persona {persona} tiene ambos palillos")
        return True
    else:
        palillo_izq.release()
        print(f"Persona {persona} comparte palillo")      #el palillo izquierdo se debe compartir para que otra persona coma
        return False


def liberarPalillos(persona):

    palillos[persona].release()
    palillos[(persona - 1) % cant_personas].release()    #Se libera ambos palillos cuando una persona dejo de comer 
    print(f"Persona {persona} libero palillos")

def iniciarComida(persona):
   
    tiempo_comiendo = 0

    while tiempo_comiendo < 10:
        if estadoPalillo(persona):                        #verificamos el estado de los palillos para proceder a comer y/o esperar
            
            tiempo_comer = min(4, 10 - tiempo_comiendo)
            tiempo_comiendo += tiempo_comer
            print(f"Persona {persona} comiendo")
            time.sleep(tiempo_comiendo)
            liberarPalillos(persona)

            
          
            print(f"Persona {persona} termino de comer.")
            time.sleep(5)
        else:            
            
            print(f"Persona {persona} esperando ")
            time.sleep(3)
        



if __name__ == '__main__':
   
   
    for _ in range(cant_personas):
        palillos.append(threading.Lock()) #inicializar los palillos con lock, para poder ser trabajado por 
                                          #por los hilos
    hilos = []
    for i in range(cant_personas):
        nuevo_hilo = threading.Thread(target=iniciarComida, args=(i,))
        hilos.append(nuevo_hilo)
    
   
    for hilo in hilos:
        hilo.start()

    
    for hilo in hilos:
        hilo.join()
