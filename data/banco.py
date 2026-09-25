import sqlite3

class BancoMoedas:

    def __init__(self, nome_arquivo='moedas.db'):
        self.nome_arquivo = nome_arquivo
        self._criar_tabela()

    def _criar_tabela(self):
        with sqlite3.connect(self.nome_arquivo) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS historico (
                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo    TEXT NOT NULL,
                    valor     REAL NOT NULL,
                    data_hora TEXT NOT NULL
                )
            """)

    def salvar(self, moeda):
        if not moeda.historico:
            return
        ultimo = moeda.historico[-1]
        with sqlite3.connect(self.nome_arquivo) as conn:
            conn.execute(
                "INSERT INTO historico (codigo, valor, data_hora) VALUES (?, ?, ?)",
                (moeda.codigo, ultimo["valor"], ultimo["hora"])
            )

    def buscar_historico(self, codigo, limite=100):
        with sqlite3.connect(self.nome_arquivo) as conn:
            cursor = conn.execute(
                "SELECT valor, data_hora FROM historico WHERE codigo = ? ORDER BY data_hora DESC LIMIT ?",
                (codigo, limite)
            )
            return cursor.fetchall()