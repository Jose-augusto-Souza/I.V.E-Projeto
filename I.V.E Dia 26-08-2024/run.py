 

import multiprocessing

# Inicia  a I.V.E
def iniciar_IVE():
        # Codigo para processo 1
        print("Processo 1 está funcionando")
        from main import start
        start()

# Inicia o hotword
def ouvirHotword():
        # Codigo para processo 2
        print("Processo 2 está funcionando.")
        from engine.features import hotword
        hotword()


    # inícia ambos os processos
if __name__ == '__main__':
        p1 = multiprocessing.Process(target=iniciar_IVE)
        p2 = multiprocessing.Process(target=ouvirHotword)
        p1.start()
        p2.start()
        p1.join()

        if p2.is_alive():
            p2.terminate()
            p2.join()

        print("Sistema parar")