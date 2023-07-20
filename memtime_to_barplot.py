import numpy as np
import matplotlib.pyplot as plt 
import argparse

#paramètres memtime : random_memtime.txt, ctgsort_memtime.txt, opti_memtime.txt, minimap_memtime.txt, miniasm_memtime.txt, 
#-random_result.txt,-ctgs_and_unmapped_result.txt, -opti_result.txt
#paramètres output : barplottime_result.png, barplotmemory_result.png


def main():
    parser = argparse.ArgumentParser(description='Produit 2 barplots (memoire et temps) à partir des fichiers benchmark en entrée')

    parser.add_argument('--opt', type=str, nargs=2, required=True,
                        help='Le chemin vers les 2 fichiers txt contenant le benchmark du tri opti et de k2r dessus, dans cet ordre.')
    parser.add_argument('--tri', type=str, nargs=4, required=True,
                        help='Le chemin vers les 4 fichiers txt contenant les memtime du tri (minimap, miniasm et sortthereads) et le benchmark de k2r dessus, dans cet ordre.')
    parser.add_argument('--rand', type=str, nargs=2, required=True,
                        help='Le chemin vers les 2 fichiers txt contenant le benchmark du tri random et de k2r dessus, dans cet ordre.')

    parser.add_argument('--timeplot_out', type=str, nargs=1, required=True,
                        help='Nom du fichier dans lequel on veut que le barplot de temps soit stocké.')
    parser.add_argument('--memoryplot_out', type=str, nargs=1, required=True,
                        help='Nom du fichier dans lequel on veut que le barplot de mémoire soit stocké.')
    
    args = parser.parse_args()

    columns = ['random', 'tri', 'opti']
    rows = ['minimap', 'miniasm', 'tri', 'k2r']

    #Création du tableau contenant les différents temps d'exécution
    #Création du tableau contenant les différentes valeurs de mémoire utilisées
    data_time = []
    data_memory = []

    minimap_times = [0]
    minimap_memories = [0]
    #récupération de temps et mémoire de minimap dans le fichier _memtime
    with open(args.tri[0]) as minimap_memtime:
        lines=minimap_memtime.readlines()
        line=lines[0]
        i=1
        while i<len(lines) and line.startswith('\t')==False:
            line = lines[i]
            i+=1
        map_time = int(lines[i].split(' ')[3].strip().split('.')[0])
        minimap_times.append(map_time)
        map_memory = round(float(lines[i+8].split(' ')[5].strip())/1048.58*1.07, 2)
        minimap_memories.append(map_memory)
        max_time = map_time
        max_memory = map_memory
    minimap_times.append(0)
    minimap_memories.append(0)

    miniasm_times = [0]
    miniasm_memories = [0]
    #récupération de temps et mémoire de miniasm dans le fichier _memtime
    with open(args.tri[1]) as miniasm_memtime:
        lines=miniasm_memtime.readlines()
        line=lines[0]
        i=1
        while i<len(lines) and line.startswith('\t')==False:
            line = lines[i]
            i+=1
        asm_time = int(lines[i].split(' ')[3].strip().split('.')[0])
        miniasm_times.append(asm_time)
        asm_memory = round(float(lines[i+8].split(' ')[5].strip())/1048.58*1.07, 2)
        miniasm_memories.append(asm_memory)
        if asm_time > max_time:
            max_time = asm_time
        if asm_memory > max_memory:
            max_memory = asm_memory
    miniasm_times.append(0)
    miniasm_memories.append(0)

    tri_times = []
    tri_memories = []
    #Récupération des temps et mémoires des 3 tris dans les fichiers benchmark pour opti et rand et _memtime pour le tri
    with open(args.rand[0]) as file:
        lines=file.readlines()
        mem = int(lines[1].split('\t')[2].split('.')[0])
        time = int(lines[1].split('\t')[9].split('.')[0])
        tri_times.append(time)
        tri_memories.append(mem)
        if mem > max_memory:
            max_memory = mem
        if time > max_time:
            max_time=time
    with open(args.tri[2]) as file:
        lines=file.readlines()
        mem = round(float(lines[9].split(' ')[5].strip())/1048.58*1.07, 2)
        time = int(lines[1].split(' ')[3].strip().split('.')[0])
        tri_times.append(time)
        tri_memories.append(mem)
        if mem > max_memory:
            max_memory = mem
        if time > max_time:
            max_time=time
    with open(args.opt[0]) as file:
        lines=file.readlines()
        mem = int(lines[1].split('\t')[2].split('.')[0])
        time = int(lines[1].split('\t')[9].split('.')[0])
        tri_times.append(time)
        tri_memories.append(mem)
        if mem > max_memory:
            max_memory = mem
        if time > max_time:
            max_time=time

    k2r_times = []
    k2r_memories = []
    k2r_files = [args.rand[1], args.tri[3], args.opt[1]]
    #Récupération des temps et mémoires des 3 tris dans les fichiers benchmark de k2r
    for filek2r in k2r_files:
        with open(filek2r) as file:
            lines=file.readlines()
            mem = int(lines[1].split('\t')[2].split('.')[0])
            time = int(lines[1].split('\t')[9].split('.')[0])
            k2r_times.append(time)
            k2r_memories.append(mem)
            if mem > max_memory:
                max_memory = mem
            if time > max_time:
                max_time=time

    data_time.append(minimap_times)
    data_time.append(miniasm_times)
    data_time.append(tri_times)
    data_time.append(k2r_times)

    data_memory.append(minimap_memories)
    data_memory.append(miniasm_memories)
    data_memory.append(tri_memories)
    data_memory.append(k2r_memories)

    #Tracé du barplot des temps

    values = np.arange(0, max_time, max_time/7)

    colors = plt.cm.BuPu(np.linspace(0.1, 0.6, len(rows)))
    n_rows = len(data_time)

    index = np.arange(len(columns)) + 0.3
    bar_width = 0.4

    y_offset = np.zeros(len(columns))

    cell_text = []
    for row in range(n_rows):
        plt.bar(index, data_time[row], bar_width, bottom=y_offset, color=colors[row])
        y_offset = y_offset + data_time[row]
        cell_text.append(['%1.1f' % x for x in y_offset])
    # Reverse colors and text labels to display the last value at the top.
    #colors = colors[::-1]
    #cell_text.reverse()

    # Add a table at the bottom of the axes
    the_table = plt.table(cellText=cell_text,
                        rowLabels=rows,
                        rowColours=colors,
                        colLabels=columns,
                        loc='bottom')

    # Adjust layout to make room for the table:
    plt.subplots_adjust(left=0.2, bottom=0.2)

    plt.ylabel(f"Temps en secondes")
    #plt.yticks(values * value_increment, ['%d' % val for val in values])
    plt.xticks([])
    plt.title('Durée d exécution de chaque fonction (cumulative)')

    #plt.show()
    plt.savefig(args.timeplot_out[0])

    #Tracé du barplot des mémoires
    plt.clf()
    values = np.arange(0, max_memory, max_memory/7)

    n_rows = len(data_memory)
    y_offset = np.zeros(len(columns))

    cell_text = []
    for row in range(n_rows):
        plt.bar(index, data_memory[row], bar_width, bottom=y_offset, color=colors[row])
        y_offset = y_offset + data_memory[row]
        cell_text.append(['%1.1f' % x for x in y_offset])
    # Reverse colors and text labels to display the last value at the top.
    #colors = colors[::-1]
    #cell_text.reverse()

    # Add a table at the bottom of the axes
    the_table = plt.table(cellText=cell_text,
                        rowLabels=rows,
                        rowColours=colors,
                        colLabels=columns,
                        loc='bottom')

    # Adjust layout to make room for the table:
    plt.subplots_adjust(left=0.2, bottom=0.2)

    plt.ylabel(f"Mémoire en Mo")
    #plt.yticks(values * value_increment, ['%d' % val for val in values])
    plt.xticks([])
    plt.title('Mémoire max lors de l exécution de chaque fonction (cumulative)')

    #plt.show()
    plt.savefig(args.memoryplot_out[0])

if __name__ == '__main__':
    main()