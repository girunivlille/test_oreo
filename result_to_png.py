import numpy as np
import matplotlib.pyplot as plt 
import argparse

def main():
    parser = argparse.ArgumentParser(description='Produit une courbe à partir des résultats en entrée')

    parser.add_argument('--opt', type=str, nargs=1, required=True,
                        help='Le chemin vers le fichier txt contenant les résultats de k2r du fichier optimal.')
    parser.add_argument('--tri', type=str, nargs=1, required=True,
                        help='Le chemin vers le fichier txt contenant les résultats de k2r du tri de sortthereads.')
    parser.add_argument('--rand', type=str, nargs=1, required=True,
                        help='Le chemin vers le fichier txt contenant les résultats de k2r du fichier random.')
    parser.add_argument('--out', type=str, nargs=1, required=True,
                        help='Fichier dans lequel sera stocké le graphique.')
    args = parser.parse_args()
    list_x = []
    list_y = []
    maxi=0
    with open(args.rand[0]) as file:
        lines=file.readlines()
        mem_rand = round(float((lines[2].split(' '))[5].replace(',',''))//1000000, 2)
        if mem_rand>maxi:
            maxi=mem_rand
        list_y.append(mem_rand)
        list_x.append("rand")

    with open(args.tri[0]) as file:
        lines=file.readlines()
        mem_tri = round(float((lines[2].split(' '))[5].replace(',',''))//1000000, 2)
        if mem_tri>maxi:
            maxi=mem_tri
        list_y.append(mem_tri)
        list_x.append("tri")

    with open(args.opt[0]) as file:
        lines=file.readlines()
        mem_opt = round(float((lines[2].split(' '))[5].replace(',',''))//1000000, 2)
        if mem_opt>maxi:
            maxi=mem_opt
        list_y.append(mem_opt)
        list_x.append("opti")

    plt.plot(list_x, list_y)
    plt.ylim(ymax=round(maxi)+round(0,2*round(maxi)))
    plt.suptitle('Somme des tailles des couleurs compressées en Mo')
    if mem_tri!=0:
        rapport_rand_tri = str(round(mem_rand/mem_tri, 2)*100)+'%'
    else:
        rapport_rand_tri = 'None'
    if mem_opt!=0:
        rapport_tri_opt = str(round(mem_tri/mem_opt, 2)*100)+'%'
    else:
        rapport_tri_opt = 'None'
    titre = 'Rand/tri = '+ rapport_rand_tri + ", tri/opti = " + rapport_tri_opt
    plt.title(titre)
    plt.savefig(args.out[0])

if __name__ == '__main__':
    main()