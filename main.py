import os
import time
from datetime import datetime
from models.moeda import Moeda
from services.cotacao import buscar_cotacoes
from data.banco import BancoMoedas

# Inicializa as moedas
moedas = [
    Moeda("USD", "Dólar"),
    Moeda("EUR", "Euro"),
    Moeda("GBP", "Libra"),
]


banco = BancoMoedas()

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def aguardar_com_contador(segundos=30):
    for i in range(segundos, 0, -1):
        print(f"\r  Próxima atualização em {i}s — Ctrl+C para opções  ", end="", flush=True)
        time.sleep(1)
    print()

def configurar_alertas(moedas):
    print("\n--- Configurar Alertas ---")
    
    for i, moeda in enumerate(moedas):
        print(f"{i + 1} - {moeda.nome}")
    print("0 - Voltar")

    try:
        escolha = int(input("\nEscolha a moeda: "))
        
        if escolha == 0:
            return
        
        if escolha < 1 or escolha > len(moedas):
            print("[ERRO] Opção inválida.")
            return

        moeda = moedas[escolha - 1]
        if moeda.valor_atual is None:
            print("[ERRO] Ainda não há uma cotação disponível para essa moeda.")
            return

        print(f"\n--- Alertas para {moeda.nome} ---")
        print(f"Valor atual: R${moeda.valor_atual:.4f}")
        print(f"Alerta acima:  R${moeda.alerta_acima:.2f}" if moeda.alerta_acima else "Alerta acima:  não definido")
        print(f"Alerta abaixo: R${moeda.alerta_abaixo:.2f}" if moeda.alerta_abaixo else "Alerta abaixo: não definido")

        print("\n1 - Definir alerta acima")
        print("2 - Definir alerta abaixo")
        print("3 - Definir ambos")
        print("4 - Remover alertas")
        print("0 - Voltar")

        tipo = input("\nEscolha: ").strip()

        match tipo:
            case "1":
                valor = float(
                    input(f"Valor acima para alertar ({moeda.nome}): ")
                    .replace(",", ".")
                )

                if valor <= moeda.valor_atual:
                    print("[ERRO] O valor do alerta acima deve ser maior que a cotação atual.")
                    return

                moeda.alerta_acima = round(valor, 2)
                moeda.alerta_acima_personalizado = True
                print(f"  Alerta definido: acima de R${moeda.alerta_acima:.2f}")

            case "2":
                valor = float(
                    input(f"Valor abaixo para alertar ({moeda.nome}): ")
                    .replace(",", ".")
                )

                if valor >= moeda.valor_atual:
                    print("[ERRO] O valor do alerta abaixo deve ser menor que a cotação atual.")
                    return

                moeda.alerta_abaixo = round(valor, 2)
                moeda.alerta_abaixo_personalizado = True
                print(f"  Alerta definido: abaixo de R${moeda.alerta_abaixo:.2f}")

            case "3":
                acima = float(
                    input(f"Valor acima ({moeda.nome}): ").replace(",", ".")
                )

                abaixo = float(
                    input(f"Valor abaixo ({moeda.nome}): ").replace(",", ".")
                )

                if acima <= moeda.valor_atual:
                    print(
                        "[ERRO] O valor do alerta acima "
                        "deve ser maior que a cotação atual."
                    )
                    return

                if abaixo >= moeda.valor_atual:
                    print(
                        "[ERRO] O valor do alerta abaixo "
                        "deve ser menor que a cotação atual."
                    )
                    return

                if abaixo >= acima:
                    print(
                        "[ERRO] O valor abaixo deve ser menor "
                        "que o valor acima."
                    )
                    return

                moeda.alerta_acima = round(acima, 2)
                moeda.alerta_abaixo = round(abaixo, 2)
                moeda.alerta_acima_personalizado = True
                moeda.alerta_abaixo_personalizado = True

                print(
                    f"  Alertas definidos: "
                    f"abaixo de R${moeda.alerta_abaixo:.2f} "
                    f"ou acima de R${moeda.alerta_acima:.2f}"
                )

            case "4":
                moeda.alerta_acima = None
                moeda.alerta_abaixo = None
                moeda.alerta_acima_personalizado = False
                moeda.alerta_abaixo_personalizado = False
                print(f"  Alertas de {moeda.nome} removidos.")

            case "0":
                return

            case _:
                print("[ERRO] Opção inválida.")

    except ValueError:
        print("[ERRO] Digite apenas números.")

def desenhar_dashboard(moedas):
    limpar_tela()
    largura = min(os.get_terminal_size().columns - 2, 60)
    linha = "═" * largura

    print(f"╔{linha}╗")
    print(f"║{'MONITOR DE COTAÇÕES':^{largura}}║")
    print(f"║{datetime.now().strftime('%d/%m/%Y  %H:%M:%S'):^{largura}}║")
    print(f"╠{linha}╣")

    for moeda in moedas:
        if moeda.valor_atual is None:
            linha_moeda = f"  {moeda.nome:<8} aguardando dados..."
        else:
            linha_moeda = (
                f"  {moeda.nome:<8} "
                f"R$ {moeda.valor_atual:>7.4f}  "
                f"{moeda.simbolo_variacao} {moeda.variacao:+.4f} "
                f"({moeda.variacao_percentual:+.2f}%)"
            )
        print(f"║{linha_moeda:<{largura}}║")



    # Alertas
    alertas = [m for m in moedas if m.alerta_disparado]
    if alertas:
        print(f"╠{linha}╣")
        for m in alertas:
            msg = f"  ⚠  {m.nome} {m.tipo_alerta} de R${m.valor_alerta_disparado:.2f}!"
            print(f"║{msg:<{largura}}║")

    print(f"╚{linha}╝")

def main():
    print("Iniciando monitor...")

    while True:
        try:
            buscar_cotacoes(moedas)

            for moeda in moedas:
                banco.salvar(moeda)

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