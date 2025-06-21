# manager/db_manager.py

import json
import os

class DBManager:
    """
    Gerencia a leitura e escrita do histórico de vitórias em um arquivo JSON.
    """
    def __init__(self, filepath='db/history.json'):
        self.filepath = filepath
        # Garante que o diretório 'db' exista
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        # Garante que o arquivo exista
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as f:
                json.dump([], f)

    def load_ranking(self):
        """ Carrega os dados do ranking do arquivo JSON. """
        try:
            with open(self.filepath, 'r') as f:
                # Ordena por vitórias (decrescente) e retorna o top 5
                data = json.load(f)
                sorted_data = sorted(data, key=lambda item: item['wins'], reverse=True)
                return sorted_data[:5]
        except (IOError, json.JSONDecodeError):
            return []

    def save_ranking(self, data):
        """ Salva os dados do ranking no arquivo JSON. """
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=4)

    def update_ranking(self, winner_name):
        """ Atualiza o ranking com o nome do vencedor. """
        data = self.load_ranking() # Carrega todos os dados, não apenas o top 5
        
        # Procura pelo vencedor na lista
        found = False
        for player in data:
            if player['name'] == winner_name:
                player['wins'] += 1
                found = True
                break
        
        # Se o jogador não foi encontrado, adiciona um novo registro
        if not found:
            data.append({'name': winner_name, 'wins': 1})
            
        self.save_ranking(data)