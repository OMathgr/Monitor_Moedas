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
    print(f"\n  Próxima atualização em 30s — Ctrl+C para sair")

def main():
    print("Iniciando monitor...")

    while True:
        try:
            buscar_cotacoes(moedas)

            for moeda in moedas:
                banco.salvar(moeda)

            desenhar_dashboard(moedas)
            time.sleep(30)

        except ConnectionError as e:
            limpar_tela()
            print(f"[ERRO DE CONEXÃO] {e}")
            print("Tentando novamente em 30s...")
            time.sleep(30)

        except KeyboardInterrupt:
            print("\n\nMonitor encerrado.")
            break

if __name__ == "__main__":
    main()