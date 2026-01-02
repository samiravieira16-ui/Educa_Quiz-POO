import json
import os
try:
    from models.quiz import Quiz
    from models.pergunta import Pergunta
    from dao.connection import Connection
except ImportError:
    # Isso evita que o código pare de funcionar enquanto os outros arquivos não existem
    Quiz = Pergunta = Connection = None

class GameController:
    def __init__(self):
        """Inicializa o controlador carregando as configurações do projeto."""
        self.pontuacao = 0
        self.perguntas = []
        self.indice_atual = 0
        self.config = self._carregar_configuracoes()

    def _carregar_configuracoes(self):
        """
        Lê o arquivo settings.json. 
        O json.load() transforma o arquivo em um dicionário Python.
        """
        # Define o caminho: config/settings.json
        caminho_config = os.path.join('config', 'settings.json')
        
        try:
            with open(caminho_config, 'r', encoding='utf-8') as arquivo:
                # O tradutor: transforma texto do arquivo em dados para o código
                return json.load(arquivo)
        except (FileNotFoundError, json.JSONDecodeError):
            # Caso o arquivo não exista ou esteja mal formatado, usamos padrões
            print("Aviso: settings.json não encontrado. Usando configurações padrão.")
            return {
                "quiz.difficultyWeights": {"easy": 1, "medium": 2, "hard": 3}
            }

    def responder_pergunta(self, resposta_usuario):
        """Valida a resposta e aplica o peso de pontuação das configurações."""
        pergunta = self.obter_pergunta_atual()
        if not pergunta:
            return False

        if pergunta.verificar_resposta(resposta_usuario):
            # Busca os pesos do JSON. Se não achar a dificuldade, usa peso 1.
            pesos = self.config.get("quiz.difficultyWeights", {})
            multiplicador = pesos.get(pergunta.dificuldade, 1)
            
            ponto_base = 10
            self.pontuacao += (ponto_base * multiplicador)
            self.indice_atual += 1
            return True
        
        self.indice_atual += 1
        return False

    def obter_pergunta_atual(self):
        """Retorna a pergunta que deve ser exibida agora."""
        if self.indice_atual < len(self.perguntas):
            return self.perguntas[self.indice_atual]
        return None
