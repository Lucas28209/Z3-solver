
from z3 import *

#variáveis
a=Bool('a')
b=Bool('b')
c=Bool('c')
d=Bool('d')
e=Bool('e')
f=Bool('f')
g=Bool('g')
z=Bool('z')

#auxiliares 
defg = (And(Or(d,e),Or(f,g)))
bcz = (And(b,c,z))

#dependências
dep1 = Implies(a,bcz)
dep2 = Implies(b,d) # b->d (se b=1 and d=1)
dep3 = Implies(c,defg) # c->(d or e) and (f or g) (se d=1 and f=1)

#conflitos
conf1 = Or(And(d,Not(e)),And(Not(d,e))) #(d=1 and e=0) or (d=0 and e=1) 
conf2 = Or(And(d,Not(g)),And(Not(d,g))) #(d=1 and g=0) or (d=0 and g=1) 
#pacotes a serem instalados
pac = And(a,z)

#solver
s=Solver()

s.add(pac)

s.add(dep1)
s.add(dep2)
s.add(dep3)

s.add(conf1)
s.add(conf2)

#interface
aux = s.check()
print("É satisfazível? R:", aux)

if isinstance(aux, CheckSatResult):
    lista = s.model()
    list = []
    for i in lista:
        if lista[i]:
            list.append(i)
    print("Pacotes que precisam ser instalados", list )