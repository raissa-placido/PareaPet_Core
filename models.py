from enum import EspecieEnum

class Pet():
    def __init__(self, nome, especie: EspecieEnum, data = None):
        self.nome = nome
        self.especie = especie
        self.data = data
        