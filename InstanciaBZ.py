# ************************************************
#   InstanciaBZ.py
#   Define a classe Instancia
#   Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
# ************************************************

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Ponto import *
import random 
from ListaDeCoresRGB import *

""" Classe Instancia """
class InstanciaBZ:   
    def __init__(self, n=None, npc=None, t=0, cor=4, velocidade=0.1, direcao = 1, movendo=False, inicio=True, escolheu=False):
        self.posicao = Ponto (0,0,0) 
        self.escala = Ponto (1,1,1)
        self.rotacao:float = 0.0
        self.modelo = None
        self.num_curva = n
        self.num_prox_curva = npc
        self.t = t
        self.cor = cor
        self.velocidade = velocidade
        self.direcao = direcao
        self.movendo = movendo
        self.inicio = inicio
        self.escolheu = escolheu
    
    """ Imprime os valores de cada eixo do ponto """
    # Faz a impressao usando sobrecarga de funcao
    # https://www.educative.io/edpresso/what-is-method-overloading-in-python
    def imprime(self, msg=None):
        if msg is not None:
            pass 
        else:
            print ("Rotacao:", self.rotacao)

    """ Define o modelo a ser usada para a desenhar """
    def setModelo(self, func):
        self.modelo = func

    def Desenha(self):
        #print ("Desenha")
        #self.escala.imprime("\tEscala: ")
        #print ("\tRotacao: ", self.rotacao)
        glPushMatrix()
        glTranslatef(self.posicao.x, self.posicao.y, 0)
        glRotatef(self.rotacao, 0, 0, 1)
        glScalef(self.escala.x, self.escala.y, self.escala.z)
        SetColor(self.cor)
        self.modelo()
        glPopMatrix()


    
