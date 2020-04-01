class TreeBuilder():
    """Construit un arbre de Huffman"""

    def __init__(self, texte):
        self.texte = texte

    def tree(self):
        #Calcul des fréquences
        freq = []
        liste = list(self.texte)
        for lettre in liste:
            c = 0
            for k in liste:
                if lettre == k:
                    c += 1
            freq.append((lettre,c))
        freq = list(set(freq))
        freq = sorted(freq, key = lambda x : x[1])

        #Construction de l'arbre

        arbre = freq.copy()
        while len(arbre) > 1 :
            arbre.append(((arbre[0],arbre[1]), arbre[0][1]+arbre[1][1]))
            del(arbre[0])
            del(arbre[0])
            arbre = sorted(arbre, key = lambda x : x[-1])

        return(arbre)

class Codec():
    """Construit un codeur/décodeur"""

    def __init__(self, tree):
        self.tree = tree

    def explorer(graphe,sommet,dictionnaire={}, clé=[]):

        if len(sommet[0]) == 1:
            dictionnaire[str(sommet[0][0])]="".join(str(b) for b in clé)

            if clé != []:
                clé.pop()

        else :
            for i in range(2):
                fils = sommet[0][i]
                clé.append(i)
                Codec.explorer(graphe,fils,dictionnaire,clé)
            if clé != []:
                clé.pop()

    def encode(self,texte):

        valeurs = {
        }
        texteencode = []

        texte = list(texte)

        Codec.explorer(self.tree,self.tree[0],valeurs,[])

        for a in texte:
            texteencode.append(valeurs[a])

        return "".join(a for a in texteencode)

    def decode(self,code):

        valeurs = {
        }
        textedecode = []
        code = list(code)
        cle = []
        cle2=''

        Codec.explorer(self.tree,self.tree[0],valeurs,[])
        valeurs_inverse = {v: k for k, v in valeurs.items()}

        while len(code) > 0:
            while cle2 not in valeurs_inverse and len(code)>0:
                cle.append(code[0])
                cle2 = "".join(cle)
                del code[0]
            textedecode.append(valeurs_inverse[cle2])
            cle = []
            cle2 = ""

        return "".join(textedecode)






#### test

text = "bonjour ceci est un test"
builder = TreeBuilder(text)
binary_tree = builder.tree()


# on passe l'arbre binaire à un encodeur/décodeur
codec = Codec(binary_tree)
# qui permet d'encoder
encoded = codec.encode(text)

print(text)
print(encoded)

decoded = codec.decode(encoded)
print(decoded)