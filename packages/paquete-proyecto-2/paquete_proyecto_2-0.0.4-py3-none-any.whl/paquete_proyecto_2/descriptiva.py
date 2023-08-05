class Paquete:
  def __init__(self, __x: list):
    self.__x= x 
    self.media = sum(self.__x)/len(self.__x)
  def mediana(self):
    '''Calcula cuando n es par: (__x_n+1)/2 o cuando n es impar calcula: (__x(n/2)*__x(n/2)+1)/2 '''
    m = sorted(self.__x)
    if len(self.__x) %2 != 0:
      print(self.__x[(len(m)//2)])
    else:
      print((self.__x[(len(m)//2)-1] + self.__x[(len(m)//2)])/2)
  def moda(self):
    '''Calcula: L_i-1+a(D₁/D₁+D₂)'''
    diccionario= {}
    for numero in self.__x:
      clave = str(numero)
      if not clave in diccionario:
        diccionario[clave] = 1
      else:
        diccionario[clave] += 1
      frecuencia_mayor = 0
    numero_repetido = self.__x[0]
    #print(diccionario)
    r = ma__x(diccionario.values())
    moda = [key for key, value in diccionario.items() if value == r] 
    if r == 1:
      print(self.__x)
    if r > 1:
      print(f'{moda} repetido {r} veces')
  def varianza(self):
    '''Calcula: Σ(__x₁-__x̄)²/n-1'''
    c=[]
    for i in self.__x:
      c.append((i-self.media)**2)
      d=sum(c)
      e= d/(len(self.__x)-1)
    print(e)
  def desviacion(self):
    '''Calcula la desviacion estanadar poblacional: √(Σ(__x₁-__x̄)²/N)'''
    c=[]
    for i in self.__x:
      c.append((i-self.media)**2)
      d=sum(c)
      e= d/(len(self.__x))
      e_2 = e**(1/2)
    print(e_2)
  def coeficiente_var(self):
    '''Calcula: (√(Σ(__x₁-__x̄)²/N)/(|(Σ__x_i)/N|))'''
    c=[]
    for i in self.__x:
      c.append((i-self.media)**2)
      d=sum(c)
      e= (d/(len(self.__x)))**(1/2)
    print(e/abs(self.media)) 
  def curtosis(self):
    '''Calcula: (((Σ__x_i-__x̄)⁴*n_i)/(Ns___x⁴))-3'''
    ku = []
    for i in self.__x:
      ku.append((i-self.media)**4)
      sum_ku = sum(ku)
      c=[]
      for i in self.__x:
        c.append((i-self.media)**2)
        d=sum(c)
        e= d/(len(self.__x))
        e_2 = e**(1/2)
    print(sum_ku/(len(self.__x)*(e_2)**4)-3)
  def simetria(self):
    '''(((Σ__x_i-__x̄)³*n_i)/(Ns___x³))'''
    si = []
    for i in self.__x:
      si.append((i-self.media)**3)
    c=[] 
    sum_si = sum(si)/len(self.__x)
    for j in self.__x:
      c.append((j-self.media)**2)
    d=sum(c)
    e= d/(len(self.__x))
    e_2 = e**(1/2)
    print(sum_si/(e_2)**3)