from colorama import Fore, Style

def red_text(text):
        return f"{Fore.RED}{text}{Style.RESET_ALL}"


class Ruler():

    """Compare deux chaines de caractères en utilisant l'algorithme de Needleman-Wunsch"""

    class Affichage():
        """Permet d'afficher en rouge les différences et les trous"""

        def __init__(self, s1, s2):
            self.s1 = s1
            self.s2 = s2

        def __str__(self):

            for k in range(len(self.s1)):
                if self.s1[k] == "=":
                    print(f"{red_text(self.s1[k])}", end="")
                elif self.s1[k] != self.s2[k]:
                    print(f"{red_text(self.s1[k])}", end="")
                else:
                    print(self.s1[k], end="")
            return ""


    def __init__(self, A, B, m=1, g=1):
        # On a pris 1 par coût par défaut pour un trou (g pour gap) et pour une différence (m pour mismatch)
        self.A = A
        self.B = B
        self.m = m
        self.g = g
        self.distance = "Aucune distance n'a encore été calculée"

    def compute(self):
        """Effectue le calcul selon l'algorithme de Needleman-Wunsch"""

        a,b = len(self.A),len(self.B)

        #On crée la matrice chemin qui donne pour chaque case M la(les) case(s) précédente(s) à partir de laquelle elle a été calculée

        chemin = [[[] for i in range(a+2)] for i in range (b+2)]

        for j in range(2, a+2):
            chemin[1][j] = [2]

        for i in range(2,b+2):
            chemin[i][1] = [1]

        #On remplit la matrice de similarité M

        M = [[0 for i in range(a+2)] for i in range(b+2)]

        for j in range(2,a+2):
            M[0][j] = self.A[j-2]

        for i in range(2,b+2):
            M[i][0] = self.B[i-2]

        for j in range(1,a+2):
            M[1][j] = (j-1)*self.g

        for i in range(1,b+2):
            M[i][1] = (i-1)*self.g

        for j in range(2,a+2):
            for i in range(2,b+2):
                diag = self.m* (self.A[j-2] != self.B[i-2]) + M[i-1][j-1]
                haut = M[i-1][j] + self.g
                bas = M[i][j-1] + self.g

                l = [diag,haut,bas]
                M[i][j] = int(min(l))

                for k in range(3):
                    if l[k] == min(l):
                        chemin[i][j].append(k)

        i,j = b+1,a+1
        distance = M[i][j]

        #On crée deux tableaux qui A2 et B2 qui contiendront les chaines alignées par l'algorithme.
        A2,B2 = [],[]

        #On crée le tableau parcours qui remonte la matrice M
        parcours = []

        while ((i,j) != (2,2) and (i,j) != (2,1) and (i,j) != (1,2)):
            if chemin[i][j][0] == 0: #Remarque : parfois, plusieurs chemins sont possibles mais on n'en calcule qu'un seul
                parcours.append(0)
                i-=1
                j-=1
            elif chemin[i][j][0] == 1:
                parcours.append(1)
                i-=1
            elif chemin[i][j][0] == 2:
                parcours.append(2)
                j-=1
            else:
                break

        parcours = parcours[::-1]

        #Selon la dernière case atteinte on ajoute le premier caractère de A2 et B2

        if (i,j) == (2,2):
            A2.append(self.A[0])
            B2.append(self.B[0])

        elif (i,j) == (2,1):
            A2.append('=')
            B2.append(self.B[0])

        elif (i,j) == (1,2):
            A2.append(self.A[0])
            B2.append('=')

        #On suit ensuite le parcours que l'on a trouvé pour remplir A2 et B2

        for a in parcours:
            if a == 0:
                i+=1
                j+=1
                A2.append(self.A[j-2])
                B2.append(self.B[i-2])

            elif a == 1:
                i+=1
                A2.append('=')
                B2.append(self.B[i-2])

            elif a == 2:
                j+=1
                A2.append(self.A[j-2])
                B2.append('=')

        A2="".join(A2)
        B2="".join(B2)

        #On crée les attributs

        self.A2 = A2
        self.B2 = B2
        self.distance = distance

    def report(self):
        """Renvoie la ligne du haut et la ligne du bas"""
        try:
            return Ruler.Affichage(self.A2,self.B2),Ruler.Affichage(self.B2,self.A2)

        except AttributeError:
            print("Le calcul doit d'abord être exécuté avec compute")

        except TypeError:
            pass