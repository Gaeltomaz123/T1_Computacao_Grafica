from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Poligonos import *
from InstanciaBZ import *
from Bezier import *
from ListaDeCoresRGB import *
import random
import time
import math
# ***********************************************************************************

# Cores aleatórias para as curvas
cores = []
for i in range(0, 21):
    cores.append(random.randint(2, 92))

# Modelos de Objetos
PontosControle = Polygon()

# Limites da Janela de Seleção
Min = Ponto()
Max = Ponto()

# lista de instancias do Personagens
Personagens = [] 

# ***********************************************************************************
# Lista de curvas Bezier
Curvas = []
Curvas_00 = []
Interceccoes_Inicial = []
Interceccoes_Final = []
Circular = 0
score = 0
jogo_rodando = False
# ***********************************************************************************
#
# ***********************************************************************************
def CarregaModelos():
    PontosControle.LePontosDeArquivo("CurvasControle.txt")

# ***********************************************************************************
def Score():
    global score
    SetColor(4)
    glRasterPos2f(-4.7, 4) 
    score_text = f"Score: {score}"
    
    for char in score_text:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))


def Atualiza_Score():
    global score
    if jogo_rodando:  
        score += 1    


def DesenhaInimigo():
    glBegin(GL_LINE_LOOP)  
    glVertex3f(0.2, 0.0, 0.0)    # Primeiro vértice
    glVertex3f(-0.2, -0.2, 0.0)  # Segundo vértice
    glVertex3f(-0.2, 0.2, 0.0)   # Terceiro vértice
    glEnd()

def DesenhaJogador():
    glBegin(GL_TRIANGLES)
    glVertex3f(0.2, 0.0, 0.0)
    glVertex3f(-0.2, -0.2, 0.0)
    glVertex3f(-0.2,  0.2, 0.0)
    glEnd()


# ***********************************************************************************
# Esta função deve instanciar todos os personagens do cenário
# ***********************************************************************************
def CriaInstancias():
    global Personagens

    # Cria jogador
    Personagens.append(InstanciaBZ())
    Personagens[0].modelo = DesenhaJogador
    Personagens[0].rotacao = 0
    Personagens[0].posicao = Ponto(-0.1,0)
    Personagens[0].escala = Ponto (0.7,0.7,0.7)
    Personagens[0].cor = 4

    # Cria Inimigos
    for i in range(1, 11):
        Personagens.append(InstanciaBZ())
        Personagens[i].modelo = DesenhaInimigo
        Personagens[i].rotacao = 0
        Personagens[i].posicao = Ponto(0,0,0)
        Personagens[i].escala = Ponto (0.7,0.7,0.7)
        Personagens[i].cor = 50 + i
        Personagens[i].t = 0.5
        Personagens[i].movendo = True
        if i > 4:
            Personagens[i].direcao = -1


# ***********************************************************************************
def CriaCurvas():
    global Curvas
    infile = open("Curvas.txt")
    line = infile.readline()
    for line in infile:
        words = line.split()
        C = Bezier(PontosControle.getVertice(int(words[0])), PontosControle.getVertice(int(words[1])), PontosControle.getVertice(int(words[2])))
        Curvas.append(C)
    infile.close()

def CriaInterceccoes():
    global Curvas
    global Interceccoes_Inicial
    global Interceccoes_Final
    global Curvas_00

    for curva in Curvas:
        interceccao_inicial = []
        interceccao_final = []
        # Se a curva começa ou termina no ponto (0,0) é adicionada a lista de curvas com pontos (0,0)
        if((curva.Coords[0].x == 0 and curva.Coords[0].y == 0) or (curva.Coords[2].x == 0 and curva.Coords[2].y == 0)):
            Curvas_00.append(curva)
        for curva_int in Curvas:
            #Compara ponto inicial com ponto inicial
            if(curva.Coords[0].x == curva_int.Coords[0].x and curva.Coords[0].y == curva_int.Coords[0].y):
                interceccao_inicial.append(curva_int)
            #Compara ponto inicial com ponto final
            if(curva.Coords[0].x == curva_int.Coords[2].x and curva.Coords[0].y == curva_int.Coords[2].y):
                interceccao_inicial.append(curva_int)
            #Compara ponto final com ponto inicial
            if(curva.Coords[2].x == curva_int.Coords[0].x and curva.Coords[2].y == curva_int.Coords[0].y):
                interceccao_final.append(curva_int)
            #Compara ponto final com ponto final 
            if(curva.Coords[2].x == curva_int.Coords[2].x and curva.Coords[2].y == curva_int.Coords[2].y):
                interceccao_final.append(curva_int)

        # Remove as proprias curvas
        interceccao_inicial.remove(curva)
        interceccao_final.remove(curva)
        Interceccoes_Inicial.append(interceccao_inicial)
        Interceccoes_Final.append(interceccao_final)


# ***********************************************************************************
def init():
    global Min, Max
    # Define a cor do fundo da tela
    glClearColor(0, 0, 0, 0)

    CarregaModelos()
    CriaInstancias()
    CriaCurvas()
    CriaInterceccoes()

    d:float = 5
    Min = Ponto(-d,-d)
    Max = Ponto(d,d)

# ****************************************************************
def animate():
    global Curvas
    global Curvas_00
    global Interceccoes_Inicial
    global Interceccoes_Final
    global jogo_rodando


    #Para cada personagem
    for personagem in Personagens:
        #Se ainda não escolheu nenhuma curva
        if personagem.num_curva == None:
            curva_inicial = random.choice(Curvas_00)
            personagem.num_curva = Curvas.index(curva_inicial)
            personagem.num_prox_curva = personagem.num_curva

        # Se chegou na metade da curvaa
        if not personagem.escolheu:
            if round(personagem.t, 2) == 0.5:
                # Se estiver indo escolhe as interceccoes finais, se estiver voltando as iniciais
                if personagem.direcao == 1:
                    personagem.num_prox_curva = Curvas.index(random.choice(Interceccoes_Final[personagem.num_curva]))
                else:
                    personagem.num_prox_curva = Curvas.index(random.choice(Interceccoes_Inicial[personagem.num_curva]))

        if Personagens.index(personagem) == 0 and personagem.inicio == False:
                jogo_rodando = True
                Verifica_Colisao(personagem)
        
        # Se movendo setado para true
        if personagem.movendo:
            personagem.inicio = False
            # Alternância de Direção
            # Curva atual recebe a proxima curva
            if personagem.t > 1:
                personagem.num_curva = personagem.num_prox_curva
                personagem.direcao = -1
                personagem.escolheu = False
                Circular = 0
            elif personagem.t < 0:
                personagem.num_curva = personagem.num_prox_curva
                personagem.direcao = 1
                personagem.escolheu = False
                Circular = 0
            # Calculo da velocidade do personagem
            deltaT = personagem.velocidade / Curvas[personagem.num_curva].ComprimentoTotalDaCurva
            personagem.t += deltaT * personagem.direcao

            # Calculo da Movimentação e da rotacao rente a curva
            P = Calcula(Curvas[personagem.num_curva].Coords, personagem.t)
            P1 = Calcula(Curvas[personagem.num_curva].Coords, personagem.t + 0.01 * personagem.direcao)
            tangente_x = P1.x - P.x
            tangente_y = P1.y - P.y
            personagem.rotacao = math.degrees(math.atan2(tangente_y, tangente_x))
            personagem.posicao = P
    glutPostRedisplay()

# Funcao calcula presente na InstanciaBZ
def Calcula(Coords, t):
        UmMenosT = 1-t
        P = Ponto()
        P = Coords[0] * UmMenosT * UmMenosT + Coords[1] * 2 * UmMenosT * t + Coords[2] * t*t
        return P  

def Verifica_Colisao(personagem):
    global score
    global jogo_rodando

    for inimigos in Personagens:
        if inimigos != personagem:
            if (personagem.posicao.x >= inimigos.posicao.x - 0.1 and personagem.posicao.x <= inimigos.posicao.x + 0.1) and (personagem.posicao.y >= inimigos.posicao.y - 0.1 and personagem.posicao.y <= inimigos.posicao.y + 0.1):
                score = 0
                jogo_rodando = False
                os._exit(0)

    
    

# ****************************************************************
def DesenhaLinha (P1, P2):
    glBegin(GL_LINES)
    glVertex3f(P1.x,P1.y,P1.z)
    glVertex3f(P2.x,P2.y,P2.z)
    glEnd()

# ****************************************************************
def RotacionaAoRedorDeUmPonto(alfa: float, P: Ponto):
    glTranslatef(P.x, P.y, P.z)
    glRotatef(alfa, 0,0,1)
    glTranslatef(-P.x, -P.y, -P.z)

# ***********************************************************************************
def reshape(w,h):

    global Min, Max
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Cria uma folga na Janela de Selecão, com 10% das dimensoes do poligono
    BordaX = abs(Max.x-Min.x)*0.1
    BordaY = abs(Max.y-Min.y)*0.1
    #glOrtho(Min.x-BordaX, Max.x+BordaX, Min.y-BordaY, Max.y+BordaY, 0.0, 1.0)
    glOrtho(Min.x, Max.x, Min.y, Max.y, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

# ***********************************************************************************
def DesenhaPersonagens():
    for I in Personagens:
        I.Desenha()


# ***********************************************************************************

# ***********************************************************************************
def DesenhaCurvas():
    v = 0
    colors = []
    #for v, I in enumerate(Curvas):
    count = 0
    for I in Curvas:
        glLineWidth(2)
        SetColor(cores[count])
        I.Traca()
        if(Personagens[0].num_prox_curva != None):
            if(Curvas[Personagens[0].num_prox_curva] == I):
                glLineWidth(6)
                SetColor(1)
                I.Traca()
        count += 1
        #DesenhaPoligonoDeControle(v)


# ***********************************************************************************
def display():

	# Limpa a tela coma cor de fundo
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    DesenhaCurvas()
    DesenhaPersonagens()
    Score()
    Atualiza_Score()
    
    glutSwapBuffers()

# ***********************************************************************************
# The function called whenever a key is pressed. 
# Note the use of Python tuples to pass in: (key, x, y)
#ESCAPE = '\033'
ESCAPE = b'\x1b'
SPACE = b' '
def keyboard(*args):
    print (args)
    # If escape is pressed, kill everything.
    if args[0] == b'q':
        os._exit(0)
    if args[0] == ESCAPE:
        os._exit(0)
    if args[0] == SPACE:
        if(Personagens[0].movendo):
            Personagens[0].movendo = False
        else:
            Personagens[0].movendo = True
# Forca o redesenho da tela
    glutPostRedisplay()

# **********************************************************************
#  arrow_keys ( a_keys: int, x: int, y: int )   
# **********************************************************************
def arrow_keys(a_keys: int, x: int, y: int):
    global Curvas_00
    global Interceccoes_Inicial
    global Interceccoes_Final
    global Circular

    if a_keys == GLUT_KEY_UP:         # Se pressionar UP
        Personagens[0].escolheu = True
        if Personagens[0].inicio:
            Personagens[0].num_curva = Curvas.index(Curvas_00[(Personagens[0].num_prox_curva + 1) % len(Curvas_00)])
            Personagens[0].num_prox_curva = Personagens[0].num_curva
        else:
            if Personagens[0].direcao == 1:
                Personagens[0].num_prox_curva = Curvas.index(Interceccoes_Final[(Personagens[0].num_curva)][Circular % len(Interceccoes_Final[(Personagens[0].num_curva)])])
            else:
                Personagens[0].num_prox_curva = Curvas.index(Interceccoes_Inicial[(Personagens[0].num_curva)][Circular % len(Interceccoes_Inicial[(Personagens[0].num_curva)])])
            Circular += 1


    if a_keys == GLUT_KEY_DOWN:       # Se pressionar DOWN
        Personagens[0].escolheu = True
        if Personagens[0].inicio:
            Personagens[0].num_curva = Curvas.index(Curvas_00[(Personagens[0].num_prox_curva - 1) % len(Curvas_00)])
            Personagens[0].num_prox_curva = Personagens[0].num_curva
        else:
            if Personagens[0].direcao == 1:
                Personagens[0].num_prox_curva = Curvas.index(Interceccoes_Final[(Personagens[0].num_curva)][Circular % len(Interceccoes_Final[(Personagens[0].num_curva)])])
            else:
                Personagens[0].num_prox_curva = Curvas.index(Interceccoes_Inicial[(Personagens[0].num_curva)][Circular % len(Interceccoes_Inicial[(Personagens[0].num_curva)])])
            Circular -= 1
            


    if a_keys == GLUT_KEY_LEFT:       # Se pressionar LEFT
        if Personagens[0].direcao == 1:
            Personagens[0].direcao = -1
            Personagens[0].num_prox_curva = Curvas.index(random.choice(Interceccoes_Inicial[Personagens[0].num_curva]))
        else:
            Personagens[0].direcao = 1
            Personagens[0].num_prox_curva = Curvas.index(random.choice(Interceccoes_Final[Personagens[0].num_curva]))
            Personagens[0].escolheu = True
        
    if a_keys == GLUT_KEY_RIGHT:      # Se pressionar RIGHT
        if Personagens[0].direcao == 1:
            Personagens[0].direcao = -1
            Personagens[0].num_prox_curva = Curvas.index(random.choice(Interceccoes_Inicial[Personagens[0].num_curva]))
        else:
            Personagens[0].direcao = 1
            Personagens[0].num_prox_curva = Curvas.index(random.choice(Interceccoes_Final[Personagens[0].num_curva]))
            Personagens[0].escolheu = True

    glutPostRedisplay()

# ***********************************************************************************
#
# ***********************************************************************************
def mouse(button: int, state: int, x: int, y: int):
    global PontoClicado
    if (state != GLUT_DOWN): 
        return
    if (button != GLUT_RIGHT_BUTTON):
        return
    #print ("Mouse:", x, ",", y)
    # Converte a coordenada de tela para o sistema de coordenadas do 
    # Personagens definido pela glOrtho
    vport = glGetIntegerv(GL_VIEWPORT)
    mvmatrix = glGetDoublev(GL_MODELVIEW_MATRIX)
    projmatrix = glGetDoublev(GL_PROJECTION_MATRIX)
    realY = vport[3] - y
    worldCoordinate1 = gluUnProject(x, realY, 0, mvmatrix, projmatrix, vport)

    PontoClicado = Ponto (worldCoordinate1[0],worldCoordinate1[1], worldCoordinate1[2])
    PontoClicado.imprime("Ponto Clicado:")

    glutPostRedisplay()

# ***********************************************************************************
#
# ***********************************************************************************
def mouseMove(x: int, y: int):
    #glutPostRedisplay()
    return


# ***********************************************************************************
# Programa Principal
# ***********************************************************************************
glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA)
# Define o tamanho inicial da janela grafica do programa
glutInitWindowSize(500, 500)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("Labirinto - T1")
glutDisplayFunc(display)
glutIdleFunc(animate)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutSpecialFunc(arrow_keys)
glutMouseFunc(mouse)
init()

try:
    glutMainLoop()
except SystemExit:
    pass
