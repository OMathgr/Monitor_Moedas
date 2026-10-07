from models.moeda import Moeda
from services.coletor import Coletor
from terminal.dashboard import (
    desenhar_dashboard,
    aguardar_com_contador,
    limpar_tela,
    configurar_alertas
)

# Inicializa as moedas
moedas = [
    Moeda("USD", "Dólar"),
    Moeda("EUR", "Euro"),
    Moeda("GBP", "Libra"),
]


coletor = Coletor(moedas)

def main():
    print("Iniciando monitor...")

    while True:
        try:
            coletor.coletar()
            desenhar_dashboard(moedas)
            aguardar_com_contador(30)

        except ConnectionError as e:
            limpar_tela()
            print(f"[ERRO DE CONEXÃO] {e}")
            print("Tentando novamente em 30s...")
            aguardar_com_contador(30)

        except KeyboardInterrupt:
            print("\n\nOpções:")
            print("1 - Configurar alertas")
            print("2 - Encerrar")
            escolha = input("Escolha: ").strip()

            match escolha:
                case "1":
                    configurar_alertas(moedas)
                case "2" | _:
                    print("Monitor encerrado.")
                    break

if __name__ == "__main__":
    main()