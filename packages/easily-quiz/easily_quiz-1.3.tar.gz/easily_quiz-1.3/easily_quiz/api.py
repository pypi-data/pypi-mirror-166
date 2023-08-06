# Created by Pina#8985 (562454496572342288)
from colorama import init, Fore, Style


class Quiz:
    """Sistema de preguntas con varias respuestas"""
    init()

    def __init__(self, pregunta, correctas, *respuestas):
        """Variables de inicializacion:\nPregunta (Pon aqui la pregunta que quieres realizar),\nCorrectas (Haz un array poniendo el numero de las respuestas correctas ejem: [1, 3]),\nRespuestas (Aca podes poner infinitamente respuestas)"""
        if type(pregunta) != str or type(correctas) != list:
            return print(Fore.RED + Style.BRIGHT + "Error 1, Bad initialization in 'Quiz'.")
        self.pregunta = pregunta
        self.correctas = correctas
        self.respuestas = respuestas

    def iniciar(self, answerInput="> "):
        """Imprime la pregunta con las respuestas y tomara la entrada de la respuesta, despues de introducir la respuesta retornara true si se ha dicho la respuesta correcta y al revez con false,\nOpcionalmente puedes cambiar el mensaje del input de respuesta"""
        print(Fore.GREEN + self.pregunta)
        pregunta = 0
        for i in self.respuestas:
            pregunta += 1
            print(f"{pregunta}.{Style.BRIGHT} {i}")
        entrada = input(answerInput)
        try:
            val = int(entrada)
            if val > len(self.respuestas):
                print(Fore.RED + Style.BRIGHT + "Error 5, The number entered in the input must be less than the number of questions. Restarting quiz...")
                self.iniciar(answerInput)
        except ValueError:
            print(Fore.RED + Style.BRIGHT + "Error 2, Input must be int. Restarting quiz...")
            self.iniciar(answerInput)
        for i in self.correctas:
            try:
                i = int(i)
            except ValueError:
                return print(Fore.RED + Style.BRIGHT + "Error 3, Variable option in 'Correctas' must be int.")
            if val == i:
                return True
        return False
            
class trueFalse:
    def __init__(self, pregunta, respuesta):
        """Variables de inicializacion:\nPregunta (Pon aqui la pregunta que quieres realizar),\nRespuesta (True o False)"""
        if type(pregunta) != str or type(respuesta) != bool:
            return print(Fore.RED + Style.BRIGHT + "Error 1, Bad initialization in 'True or false'.")
        self.pregunta = pregunta
        self.respuesta = respuesta
    def iniciar(self, answerInput="> "):
        """Imprime la pregunta con dos posibles respuestas y tomara la entrada de la respuesta, despues de introducir la respuesta retornara true si se ha dicho la respuesta correcta y al revez con false,\nOpcionalmente puedes cambiar el mensaje del input de respuesta"""
        print(Fore.GREEN + self.pregunta)
        print(f"{Fore.CYAN}1.{Style.BRIGHT} Verdadero")
        print(f"{Fore.CYAN}2.{Style.BRIGHT} Falso")
        entrada = input(answerInput)
        try:
            val = int(entrada)
            if val == int(self.respuesta):
                return True
            else:
                return False
        except ValueError:
            print(Fore.RED + Style.BRIGHT + "Error 2, Input must be int. Restarting true or false...")
            self.iniciar(answerInput)
        if val <= 0 or val >= 3:
            print(Fore.RED + Style.BRIGHT + "Error 4, Answer only can be 1 or 2. Restarting true or false...")
            self.iniciar(answerInput)
        
        

