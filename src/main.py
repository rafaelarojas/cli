import inquirer
import pydobot
from yaspin import yaspin
from serial.tools import list_ports
from colorama import Fore, Style, init

init(autoreset=True)

class RoboInterface:
    def __init__(self, porta_escolhida):
        self.robo = pydobot.Dobot(port=porta_escolhida, verbose=False)
        self.spinner = yaspin(text="Carregando...", color="blue")

    def home(self):
        self.spinner.start()
        self.robo.move_to(200, 0, 0, 0, wait=True)
        self.spinner.stop()
        print(Fore.YELLOW + "🏠 Home")

    def ligar_ferramenta(self):
        self.spinner.start()
        self.robo.suck(True)
        self.robo.wait(200)
        self.spinner.stop()
        print(Fore.GREEN + "Ferramenta ligada.")

    def desligar_ferramenta(self):
        self.spinner.start()
        self.robo.suck(False)
        self.robo.wait(200)
        self.spinner.stop()
        print(Fore.RED + "Ferramenta desligada.")

    def mover(self, eixo, distancia):
        if eixo.lower() == 'x':
            self.spinner.start()
            self.robo.move_to(self.robo.pose()[0] + distancia, 0, 0, 0, wait=True)
            self.spinner.stop()
            print(Fore.GREEN + f"Movido {distancia} unidades no eixo X.")
        if eixo.lower() == 'y':
            self.spinner.start()
            self.robo.move_to(self.robo.pose()[0] + 0, distancia, 0, 0, wait=True)
            self.spinner.stop()
            print(Fore.GREEN + f"Movido {distancia} unidades no eixo Y.")
        if eixo.lower() == 'z':
            self.spinner.start()
            self.robo.move_to(self.robo.pose()[0] + 0, 0, distancia, 0, wait=True)
            self.spinner.stop()
            print(Fore.GREEN + f"Movido {distancia} unidades no eixo Z.")

    def atual(self):
        posicao_atual = self.robo.pose()
        print(Fore.MAGENTA + f"Posição atual: {posicao_atual}")

    def run(self):
        while True:
            comando = input(Fore.LIGHTBLUE_EX + f"--------------------------------------------------------------- \n🤖 Digite um comando ('home', 'ligar ferramenta', 'desligar ferramenta', 'mover', 'atual', 'sair'): ")
            if comando == 'sair':
                break
            elif comando == 'home':
                self.home()
            elif comando == 'ligar ferramenta':
                self.ligar_ferramenta()
            elif comando == 'desligar ferramenta':
                self.desligar_ferramenta()
            elif comando.startswith('mover'):
                _, eixo, distancia = comando.split()
                self.mover(eixo, int(distancia))
            elif comando == 'atual':
                self.atual()

        self.robo.close()

if __name__ == "__main__":
    available_ports = inquirer.prompt([
        inquirer.List("porta", message="Escolha a porta serial", choices=[x.device for x in list_ports.comports()])
    ])["porta"]

    interface = RoboInterface(available_ports)

    interface.run()
