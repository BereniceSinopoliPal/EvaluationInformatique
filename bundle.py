import sys
from ruler import Ruler


filename = sys.argv[1]
fichier = open(filename,"r")

lines = fichier.readlines()

for line in lines:
    if line == "":
        del line

if len(lines)%2 != 0:
    lines.pop()

for i in range(len(lines)//2):
    ruler = Ruler(lines[2*i], lines[2*i+1])
    ruler.compute()
    top, bottom = ruler.report()
    print(f"====== exemple # {i} - distance = {ruler.distance}")
    print(top)
    print(bottom)

fichier.close()
