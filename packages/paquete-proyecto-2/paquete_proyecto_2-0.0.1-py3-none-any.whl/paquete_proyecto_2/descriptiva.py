class Paquete:
  def __init__(self, x: list):
    self.x= x 
    self.media = sum(self.x)/len(self.x)
    
  def mediana(self):
    '''Calcula cuando n es par: (x_n+1)/2 o cuando n es impar calcula: (x(n/2)*x(n/2)+1)/2 '''
    m = sorted(self.x)
    if len(self.x) %2 != 0:
      print(self.x[(len(m)//2)])
    else:
      print((self.x[(len(m)//2)-1] + self.x[(len(m)//2)])/2)
  def moda(self):
    '''Calcula: L_i-1+a(D₁/D₁+D₂)'''
    diccionario= {}
    for numero in self.x:
      clave = str(numero)
      if not clave in diccionario:
        diccionario[clave] = 1
      else:
        diccionario[clave] += 1
      frecuencia_mayor = 0
    numero_repetido = self.x[0]
    #print(diccionario)
    r = max(diccionario.values())
    moda = [key for key, value in diccionario.items() if value == r] 
    if r == 1:
      print(self.x)
    if r > 1:
      print(f'{moda} repetido {r} veces')
  def varianza(self):
    '''Calcula: Σ(x₁-x̄)²/n-1'''
    c=[]
    for i in self.x:
      c.append((i-self.media)**2)
      d=sum(c)
      e= d/(len(self.x)-1)
    print(e)
  def desviacion(self):
    '''Calcula: √(Σ(x₁-x̄)²/N)'''
    c=[]
    for i in self.x:
      c.append((i-self.media)**2)
      d=sum(c)
      e= d/(len(self.x))
      e_2 = e**(1/2)
    print(e_2)
  def coeficiente_var(self):
    '''Calcula: (√(Σ(x₁-x̄)²/N)/(|(Σx_i)/N|))'''
    c=[]
    for i in self.x:
      c.append((i-self.media)**2)
      d=sum(c)
      e= (d/(len(self.x)))**(1/2)
    print(e/abs(self.media)) 
  def curtosis(self):
    '''Calcula: (((Σx_i-x̄)⁴*n_i)/(Ns_x⁴))-3'''
    ku = []
    for i in self.x:
      ku.append((i-self.media)**4)
      sum_ku = sum(ku)
      c=[]
      for i in self.x:
        c.append((i-self.media)**2)
        d=sum(c)
        e= d/(len(self.x))
        e_2 = e**(1/2)
    print(sum_ku/(len(self.x)*(e_2)**4)-3)
  def simetria(self):
    '''(((Σx_i-x̄)³*n_i)/(Ns_x³))'''
    si = []
    for i in self.x:
      si.append((i-self.media)**3)
    c=[] 
    sum_si = sum(si)/len(self.x)
    for j in self.x:
      c.append((j-self.media)**2)
    d=sum(c)
    e= d/(len(self.x))
    e_2 = e**(1/2)
    print(sum_si/(e_2)**3)
    