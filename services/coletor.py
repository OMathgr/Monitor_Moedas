from services.cotacao import buscar_cotacoes
from data.banco import BancoMoedas

class Coletor:
    def __init__(self, moedas):
        self.moedas = moedas
        self.banco = BancoMoedas()

    def coletar(self):
        buscar_cotacoes(self.moedas)

        for moeda in self.moedas:
            self.banco.salvar(moeda)