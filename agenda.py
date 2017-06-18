import sys

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'

# Imprime texto com cores. Por exemplo, para imprimir "Oi mundo!" em vermelho, basta usar
#
# printCores('Oi mundo!', RED)
# printCores('Texto amarelo e negrito', YELLOW + BOLD)

def printCores(texto, cor) :
  print(cor + texto + RESET)
  

# Adiciona um compromisso aa agenda. Um compromisso tem no minimo
# uma descrição. Adicionalmente, pode ter, em caráter opcional, uma
# data (formato DDMMAAAA), um horário (formato HHMM), uma prioridade de A a Z, 
# um contexto onde a atividade será realizada (precedido pelo caractere
# '@') e um projeto do qual faz parte (precedido pelo caractere '+'). Esses
# itens opcionais são os elementos da tupla "extras", o segundo parâmetro da
# função.
#
# extras ~ (data, hora, prioridade, contexto, projeto)
#
# Qualquer elemento da tupla que contenha um string vazio ('') não
# deve ser levado em consideração. 
def adicionar(descricao, extras):

  # não é possível adicionar uma atividade que não possui descrição. 
  if descricao  == '' :
    return False
  else:
    if extras[0] == '':
      extras[0].pop()
    else:
      if dataValida(extras[0]) == True:
        extras.pop()  
  ################ COMPLETAR


  # Escreve no TODO_FILE. 
  try: 
    fp = open(TODO_FILE, 'a')
    fp.write(novaAtividade + "\n")
    fp.close()
  except IOError as err:
    print("Não foi possível escrever para o arquivo " + TODO_FILE)
    print(err)
    return False

  return True


# Valida a prioridade.
def prioridadeValida(pri):
  if (len(pri) < 3) or (len(pri) > 3):
    return False
  if pri[0] != '(':
    return False
  if pri[2] != ')':
    return False
  if pri[1].isalpha() == False:
    return False
  else: 
    return True

# Valida a hora. Consideramos que o dia tem 24 horas, como no Brasil, ao invés
# de dois blocos de 12 (AM e PM), como nos EUA.
def horaValida(horaMin) :
  if len(horaMin) != 4 or not soDigitos(horaMin):
    return False
  else:
    if (horaMin[0] and horaMin[1] >= '0') and (horaMin[0] and horaMin[1] <= '23'):
      if (horaMin[2] and horaMin[3] >= '0') and (horaMin[0] and horaMin[1] <= '59'):
        return True

# Valida datas. Verificar inclusive se não estamos tentando
# colocar 31 dias em fevereiro. Não precisamos nos certificar, porém,
# de que um ano é bissexto. 
def dataValida(data) :

  if len(data) != 8 or not soDigitos(data):
      return False
  if (data[2] + data[3] == '04' or '06' or '09' or '11')  and (data[0] + data[1] == '31'):
      return False
  if (data[2] + data[3] == '02') and (data[0] + data[1] > '29'):
      return False
  else:
    if (data[0] + data[1] >= '01') and ((data[2] + data[3] >= '01') and (data[2] + data[3] <= '12')):
      return True
# Valida que o string do projeto está no formato correto. 
def projetoValido(proj):

  if (len(proj) < 2):
    return False
  if(proj[0] != '+'):
    return False
  else:
    return True
  
# Valida que o string do contexto está no formato correto. 
def contextoValido(cont):

  if (len(cont) < 2):
    return False
  if(cont[0] != '@'):
    return False
  else:
    return True

# Valida que a data ou a hora contém apenas dígitos, desprezando espaços
# extras no início e no fim.
def soDigitos(numero) :
  if type(numero) != str :
    return False
  for x in numero :
    if x < '0' or x > '9' :
      return False
  return True


# Dadas as linhas de texto obtidas a partir do arquivo texto todo.txt, devolve
# uma lista de tuplas contendo os pedaços de cada linha, conforme o seguinte
# formato:
#
# (descrição, prioridade, (data, hora, contexto, projeto))
#
# É importante lembrar que linhas do arquivo todo.txt devem estar organizadas de acordo com o
# seguinte formato:
#
# DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
#
# Todos os itens menos DESC são opcionais. Se qualquer um deles estiver fora do formato, por exemplo,
# data que não tem todos os componentes ou prioridade com mais de um caractere (além dos parênteses),
# tudo que vier depois será considerado parte da descrição.  

'''
    # Processa os tokens um a um, verificando se são as partes da atividade.
    # Por exemplo, se o primeiro token é uma data válida, deve ser guardado
    # na variável data e posteriormente removido a lista de tokens. Feito isso,
    # é só repetir o processo verificando se o primeiro token é uma hora. Depois,
    # faz-se o mesmo para prioridade. Neste ponto, verifica-se os últimos tokens
    # para saber se são contexto e/ou projeto. Quando isso terminar, o que sobrar
    # corresponde à descrição. É só transformar a lista de tokens em um string e
    # construir a tupla com as informações disponíveis.
'''    
def organizar(g):
  itens = []
  j = 0
  g = open(TODO_FILE, 'r')
  linhas = g.readlines() 
  for l in linhas:
    data = '' 
    hora = ''
    pri = ''
    desc = ''
    contexto = ''
    projeto = ''
  
    l = l.strip() # remove espaços em branco e quebras de linha do começo e do fim
    tokens = l.split() # quebra o string em palavras

    while j < len(tokens):
      if dataValida(tokens[j]) == True:
        data = tokens[j]
      elif horaValida(tokens[j]) == True:
        hora = tokens[j]
      elif prioridadeValida(tokens[j]) == True:
        pri = tokens[j]
      elif (projetoValido(tokens[-1]) and contextoValido(tokens[-2])) == True:
        contexto = tokens[-2]
        projeto = tokens[-1]
      j += 1
      itens.append((desc, (data, hora, pri, contexto, projeto)))
    return itens 
  g.close()
  


# Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
# como se espera (com os separadores apropridados). 
#
# Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
# (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
# determinado projeto; (vi) atividades de determinado dia (data específica, hoje ou amanhã). Isso não
# é uma das tarefas básicas do projeto, porém. 
def listar():
  g = open(TODO_FILE, 'r')
  lis = organizar(g)
  lisOrd = ordenarPorPrioridade(lis) 
  g.close()
  for index, item in enumerate(lisOrd):
    if item[1] == 'A' or 'a':
      printCores(item[2], RED + BOLD)
    if item[1] == 'B' or 'b':
      printCores(item[2], YELLOW)
    if item[1] == 'C' or 'c':
      printCores(item[2], GREEN)
    if item[1] == 'D' or 'd':
      printCores(item[2], BLUE) 
    return index,item 

def ordenarPorDataHora(itens):

  ################ COMPLETAR

  return itens
   
def ordenarPorPrioridade(itens):
    aux = organizar(itens)
    j = 0
    while j < len(aux):
      if prioridadeValida(aux[j]) == True:
        aux = 0       
        return itens

def fazer(num):

  ################ COMPLETAR

  return 

def remover():

  ################ COMPLETAR

  return

# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'. 
def priorizar(num, prioridade):

  ################ COMPLETAR

  return 



# Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos.

def processarComandos(comandos) :
  if comandos[0] == ADICIONAR:
    comandos.pop(0) # remove 'agenda.py'
    comandos.pop(0) # remove 'adicionar'
    itemParaAdicionar = organizar([' '.join(comandos)])[0]
    # itemParaAdicionar = (descricao, (prioridade, data, hora, contexto, projeto))
    adicionar(itemParaAdicionar[0], itemParaAdicionar[1]) # novos itens não têm prioridade
  elif comandos[0] == LISTAR:
    return listar()

  elif comandos[0] == REMOVER:
    
    return    

    ################ COMPLETAR    

  elif comandos[0] == FAZER:
    return    

    ################ COMPLETAR

  elif comandos[0] == PRIORIZAR:
    return    

    ################ COMPLETAR

  else :
    print("Comando inválido.")
    
  
# sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
# invocado a partir da linha de comando e os elementos restantes são tudo que
# foi fornecido em sequência. Por exemplo, se o programa foi invocado como
#
# python3 agenda.py a Mudar de nome.
#
# sys.argv terá como conteúdo
#
# ['agenda.py', 'a', 'Mudar', 'de', 'nome']
processarComandos(sys.argv)

