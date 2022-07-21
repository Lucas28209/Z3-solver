#Lucas de Oliveira Rocha

from z3 import *
import numpy as np



def resolucao():
      n = 9
      # Realiza a leitura do arquivo txt contendo o tabuleiro inicial
      # O arquivo 'sudoku.txt' contém um tabuleiro inicial que permite duas soluções
      tabuleiro = np.loadtxt('sudoku.txt')

      # Var -> Lista de 81 variáveis inteiras (x00,x01,x02...x87,x88)
      Var = [ [Int("x%s%s" % (i,j)) for j in range(n)] for i in range(n) ]   

      # Cada variável x[i][j] de Var deve estar no intervalo [1,9] ( x01 >= 1 and x01 <= 9  ... x88 >= 1 and x88 <= 9 )
      restricao1 = [ And(Var[i][j] >= 1, Var[i][j] <= 9) for i in range(n) for j in range(n) ]

      # Cada linha x[i] de Var deve apresentar um valor distinto das outras linhas, entre [1,9]
      restricao2 = [ Distinct(Var[i]) for i in range(n) ]

      # Cada coluna x[i][j] de Var deve apresentar um valor distinto das outras colunas, entre [1,9]
      restricao3 = [ Distinct([Var[i][j] for i in range(n) ])  for j in range(n) ]

      # Em cada uma das 9 grades do sudoku, esta deve apresentar um valor x[i][j] distinto das outras células da mesma grade
      # (x00 != x01 != x02 != x10 != x11 != x12 != x20 != x21 != x22)   
      restricao4 = [ Distinct([ Var[i + (I*3)][j + (J*3)] for i in range(3) for j in range(3) ]) for I in range(3) for J in range(3) ]

      # Junção das restrições 1,2,3 e 4 em uma única lista
      restricoes = restricao1 + restricao2 + restricao3 + restricao4 

      # Utiliziação do operdor If do Z3 -> if-then-else If(condição, expressão que deve ser verdade se a condição for verdade, expressão que deve ser verdade se a condição for falsa)
      sudoku_inicio = [ If(int(tabuleiro[i][j]) == 0, True, Var[i][j] == int(tabuleiro[i][j])) for i in range(n) for j in range(n) ]

      s = Solver()
      # Adiciona as restrições e a configuração inicial
      s.add(restricoes + sudoku_inicio)
      
      # Se o problema for satisfazível:
      while s.check() == sat:
            m = s.model()

            # Adiciona os valores das variáveis a matriz r            
            r = [ [ m.evaluate(Var[i][j]) for j in range(n) ] for i in range(n) ]
            
            # Chama a função imprime() para imprimir a matriz
            imprime(r) 

            # Cria uma lista de novas restrições 
            novas_restricoes = []
            for i in range(9):
                  for j in range(9):
                        aux = m.evaluate(Var[i][j])
                        # Cada par (variável,valor) é adicionados na lista novas_restricoes,
                        # de forma que a varívavel seja diferente do valor.
                        # x00 != 1, por exemplo
                        novas_restricoes.append((Var[i][j] != aux))
            # Adiciona a lista de novas restrições, utilizando o operador Or para 
            # tornar possível novas soluções com valores diferentes 
            s.add(Or(novas_restricoes))


      # Se o problema não for satisfazível ou não houverem mais soluções:
      else:
            print ("não há mais soluções")

def imprime(r):
      # Função para imprimir as respostas
      a = np.array(r)
      print('\nsolução:')
      for line in a:
            print ('  '.join(map(str, line)))
      


if __name__ == "__main__":   
      # Chama a função resolucao() 
      resolucao()