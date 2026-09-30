from datetime import datetime


class Moeda:

    def __init__(self, codigo, nome):
        self.codigo = codigo
        self.nome = nome
        self.valor_atual = None
        self.valor_anterior = None
        self.historico = []

        # Alertas
        self.alerta_acima = None
        self.alerta_abaixo = None
        self.alerta_acima_personalizado = False
        self.alerta_abaixo_personalizado = False
        self.alerta_disparado = False
        self.valor_alerta_disparado = None
        self.tipo_alerta = None

    def definir_alerta(self, valor_central, margem=0.20):
        self.alerta_acima = round(valor_central + margem, 2)
        self.alerta_abaixo = round(valor_central - margem, 2)
        self.alerta_acima_personalizado = False
        self.alerta_abaixo_personalizado = False

    def atualizar(self, novo_valor):
        self.valor_anterior = self.valor_atual
        self.valor_atual = novo_valor
        self.historico.append({
            "valor": novo_valor,
            "hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        if self.valor_anterior is None:
            self.definir_alerta(novo_valor)
            return

        self.alerta_disparado = False
        self.valor_alerta_disparado = None
        self.tipo_alerta = None

        if self.alerta_acima and self.valor_atual >= self.alerta_acima:
            self.alerta_disparado = True
            self.valor_alerta_disparado = self.alerta_acima
            self.tipo_alerta = "acima"

            self._reajustar_alerta_acima()

        elif self.alerta_abaixo and self.valor_atual <= self.alerta_abaixo:
            self.alerta_disparado = True
            self.valor_alerta_disparado = self.alerta_abaixo
            self.tipo_alerta = "abaixo"

            self._reajustar_alerta_abaixo()

    def _reajustar_alerta_acima(self):
        self.alerta_acima = round(self.valor_atual + 0.20, 2)
        self.alerta_acima_personalizado = False

    def _reajustar_alerta_abaixo(self):
        self.alerta_abaixo = round(self.valor_atual - 0.20, 2)
        self.alerta_abaixo_personalizado = False

    @property
    def variacao(self):
        if self.valor_anterior is None or self.valor_atual is None:
            return 0

        return self.valor_atual - self.valor_anterior

    @property
    def variacao_percentual(self):
        if self.valor_anterior is None or self.valor_anterior == 0:
            return 0

        return (self.variacao / self.valor_anterior) * 100

    @property
    def em_alerta(self):
        if self.valor_atual is None:
            return False

        if self.alerta_acima and self.valor_atual >= self.alerta_acima:
            return True

        if self.alerta_abaixo and self.valor_atual <= self.alerta_abaixo:
            return True

        return False

    @property
    def simbolo_variacao(self):
        if self.variacao > 0:
            return "▲"

        if self.variacao < 0:
            return "▼"

        return "━"

    def __str__(self):
        if self.valor_atual is None:
            return f"{self.nome} ({self.codigo}) — aguardando dados..."

        return (
            f"{self.nome} ({self.codigo}) "
            f"R$ {self.valor_atual:.2f} "
            f"{self.simbolo_variacao} {self.variacao:+.4f} "
            f"({self.variacao_percentual:+.2f}%)"
        )

    def __repr__(self):
        return (
            f"Moeda(codigo='{self.codigo}', "
            f"valor_atual={self.valor_atual})"
        )