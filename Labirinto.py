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

angulo = 0.0
t = 0
velocidade = 0.004
curva_atual = None
direcao = 1 
# ***********************************************************************************
#
# ***********************************************************************************
def CarregaModelos():
    PontosControle.LePontosDeArquivo("CurvasControle.txt")

# ***********************************************************************************
def DesenhaPersonagem():
    glBegin(GL_TRIANGLES)
    SetColor(YellowGreen)
    glVertex3f(0.0, 0.2, 0.0)
    glVertex3f(-0.2, -0.2, 0.0)
    glVertex3f(0.2,  -0.2, 0.0)
    glEnd()



# ***********************************************************************************
# Esta função deve instanciar todos os personagens do cenário
# ***********************************************************************************
def CriaInstancias():
    global Personagens
    Personagens.append(InstanciaBZ())
    Personagens[0].modelo = DesenhaPersonagem
    Personagens[0].rotacao = 1
    Personagens[0].posicao = Ponto(0,0)
    Personagens[0].escala = Ponto (1,1,1)


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


def IndicesCurvas(Nome):
        
        
        return indices


# ***********************************************************************************
def init():
    global Min, Max
    # Define a cor do fundo da tela
    glClearColor(0, 0, 0, 0)

    CarregaModelos()
    CriaInstancias()
    CriaCurvas()

    d:float = 5
    Min = Ponto(-d,-d)
    Max = Ponto(d,d)

# ****************************************************************
def animate():
    global t
    global velocidade
    global curva_atual
    global direcao

    t += velocidade * direcao
        
    print(curva_atual)

    if curva_atual == None:
        curva_atual = random.choice(Curvas)
    else:
        if t > 1.0: 
            curvas_comum = []
            for curva in Curvas:
                if(curva != curva_atual):
                    for coord in curva.Coords:
                        if coord.x == round(Personagens[0].posicao.x) and coord.y == round(Personagens[0].posicao.y):
                            curvas_comum.append(curva)
            curva_atual = random.choice(curvas_comum)
            t = 1.0
            direcao = -1  # Inverte para voltar
        elif t < 0.0:
            curva_atual = random.choice(Curvas)
            t = 0.0
            direcao = 1 

    P = Calcula(curva_atual.Coords, t)
    Personagens[0].posicao.x = P.x
    Personagens[0].posicao.y = P.y
    glutPostRedisplay()

def Calcula(Coords, t):
        UmMenosT = 1-t
        P = Ponto()
        P = Coords[0] * UmMenosT * UmMenosT + Coords[1] * 2 * UmMenosT * t + Coords[2] * t*t
        return P  

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
    
    glutSwapBuffers()

# ***********************************************************************************
# The function called whenever a key is pressed. 
# Note the use of Python tuples to pass in: (key, x, y)
#ESCAPE = '\033'
ESCAPE = b'\x1b'
def keyboard(*args):
    print (args)
    # If escape is pressed, kill everything.
    if args[0] == b'q':
        os._exit(0)
    if args[0] == ESCAPE:
        os._exit(0)
# Forca o redesenho da tela
    glutPostRedisplay()

# **********************************************************************
#  arrow_keys ( a_keys: int, x: int, y: int )   
# **********************************************************************
def arrow_keys(a_keys: int, x: int, y: int):
    if a_keys == GLUT_KEY_UP:         # Se pressionar UP
        Personagens[0].escala.x += 1
    if a_keys == GLUT_KEY_DOWN:       # Se pressionar DOWN
        Personagens[0].escala.x -= 1
    if a_keys == GLUT_KEY_LEFT:       # Se pressionar LEFT
        Personagens[0].posicao.x -= 1
        
    if a_keys == GLUT_KEY_RIGHT:      # Se pressionar RIGHT
        Personagens[0].posicao.x += 1

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
