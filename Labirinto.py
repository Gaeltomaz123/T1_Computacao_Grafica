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
Interceccoes = []
# ***********************************************************************************
#
# ***********************************************************************************
def CarregaModelos():
    PontosControle.LePontosDeArquivo("CurvasControle.txt")

# ***********************************************************************************
def DesenhaPersonagem():
    glBegin(GL_TRIANGLES)
    glVertex3f(0.0, 0.2, 0.0)
    glVertex3f(-0.2, -0.2, 0.0)
    glVertex3f(0.2,  -0.2, 0.0)
    glEnd()



# ***********************************************************************************
# Esta função deve instanciar todos os personagens do cenário
# ***********************************************************************************
def CriaInstancias():
    global Personagens
    for i in range(10):
        Personagens.append(InstanciaBZ())
        Personagens[i].modelo = DesenhaPersonagem
        Personagens[i].rotacao = 0
        Personagens[i].posicao = Ponto(0,0)
        Personagens[i].escala = Ponto (1,1,1)
        Personagens[i].cor = 50 + i
        Personagens[i].t = 0.5
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
    global Interceccoes

    count = 0
    for curva in Curvas:
        interceccao = []
        for curva_int in Curvas:
                if(curva.Coords[2].x == curva_int.Coords[2].x and curva.Coords[2].y == curva_int.Coords[2].y):
                    interceccao.append(curva_int)
                if(curva.Coords[0].x != 0 and curva.Coords[0].y != 0 and (curva.Coords[0].x == curva_int.Coords[0].x and curva.Coords[0].y == curva_int.Coords[0].y)):
                    interceccao.append(curva_int)
        interceccao.remove(curva)
        count += 1
        Interceccoes.append(interceccao)


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
    
    #print(round(t, 3))
    for personagem in Personagens:
        if personagem.num_curva == None:
            personagem.num_curva = Curvas.index(random.choice(Curvas))
            personagem.num_prox_curva = Curvas.index(random.choice(Curvas))
        elif round(personagem.t, 1) == 0.5:
            personagem.num_prox_curva = Curvas.index(random.choice(Interceccoes[personagem.num_curva]))
        elif personagem.t > 1:
            personagem.num_curva = personagem.num_prox_curva
            personagem.direcao = -1
        elif personagem.t < 0:
            personagem.num_curva = Curvas.index(random.choice(Curvas))
            personagem.num_prox_curva = Curvas.index(random.choice(Curvas))
            personagem.direcao = 1
        deltaT = personagem.velocidade / Curvas[personagem.num_curva].ComprimentoTotalDaCurva
        personagem.t += deltaT * personagem.direcao
    
        P = Calcula(Curvas[personagem.num_curva].Coords, personagem.t)
        P1 = Calcula(Curvas[personagem.num_curva].Coords, personagem.t + 0.01)
        tangente_x = P1.x - P.x
        tangente_y = P1.y - P.y
        personagem.angulo = math.degrees(math.atan2(tangente_y, tangente_x))
        personagem.angulo += 270 * personagem.direcao
        personagem.rotacao = personagem.angulo
        personagem.posicao = P
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
