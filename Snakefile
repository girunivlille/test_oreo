rule target:
    input:
        "order_cel_10kb_30X_1000/graphs/order_cel_10kb_30X_1000_graph_result.png",
        "order_cel_10kb_30X_1000/graphs/order_cel_10kb_30X_1000_barplottime_result.png",
        "order_cel_10kb_30X_1000/graphs/order_cel_10kb_30X_1000_barplotmemory_result.png"

rule move_fa:
    input:
        reads = "{read}.fa"
    output:
        dest = temp("{read}/reads/{read}-opti.fa"),
        bench = "{read}/results/{read}_opti_memtime.txt"
    benchmark:
        "{read}/results/{read}_opti_memtime.txt"
    shell:
        "cp {input.reads} {output.dest}"

rule reads_sort:
    input:
        reads = "{read}/reads/{read}-opti.fa"
    threads:
        16
    output:
        sorted_reads_mv = "{read}/reads/{read}-sorted.fa",
        minimap_memtime = "{read}/results/{read}_minimap_memtime.txt",
        miniasm_memtime = "{read}/results/{read}_miniasm_memtime.txt",
        tri_memtime = "{read}/results/{read}_sort_memtime.txt"
    shell:
        "python3 sort_the_reads/sort_the_reads.py --reads {input.reads} -t && mv {wildcards.read}/reads/{wildcards.read}-opti_sorted.fa {output.sorted_reads_mv} && mv {wildcards.read}/reads/{wildcards.read}-opti_minimap_memtime.txt {output.minimap_memtime} && mv {wildcards.read}/reads/{wildcards.read}-opti_miniasm_memtime.txt {output.miniasm_memtime} && mv {wildcards.read}/reads/{wildcards.read}-opti_sort_memtime.txt {output.tri_memtime}"

rule random:
    input:
        reads = "{read}/reads/{read}-opti.fa"
    output:
        rand = temp("{read}/reads/{read}-random.fa"),
        bench = "{read}/results/{read}_random_memtime.txt"
    benchmark:
        "{read}/results/{read}_random_memtime.txt"
    shell:
        "./tri_random {input.reads} {output.rand}"

rule k2r:
    input:
        reads = "{read}/reads/{read}-{algo}.fa"
    output:
        result = "{read}/results/{read}-{algo}_result.txt",
        bench = "{read}/results/{read}-{algo}_k2r_bench.txt"
    benchmark:
        "{read}/results/{read}-{algo}_k2r_bench.txt"
    shell:
        "index_kmer_to_reads/index {input.reads} 31 smt_useless.txt 1 > {output.result}"

rule graph:
    input:
        rand = "{read}/results/{read}-random_result.txt",
        tri = "{read}/results/{read}-sorted_result.txt",
        opti = "{read}/results/{read}-opti_result.txt"
    output:
        "{read}/graphs/{read}_graph_result.png"
    shell:
        "python3 result_to_png.py --opt {input.opti} --tri {input.tri} --rand {input.rand} --out {output}"

rule barplots:
    input:
        opt_tri = "{read}/results/{read}_opti_memtime.txt",
        opt_k2r = "{read}/results/{read}-opti_k2r_bench.txt",
        tri_minimap = "{read}/results/{read}_minimap_memtime.txt",
        tri_miniasm = "{read}/results/{read}_miniasm_memtime.txt",
        tri_memtime = "{read}/results/{read}_sort_memtime.txt",
        tri_k2r = "{read}/results/{read}-sorted_k2r_bench.txt",
        rand_tri = "{read}/results/{read}_random_memtime.txt",
        rand_k2r = "{read}/results/{read}-random_k2r_bench.txt"
    output:
        time = "{read}/graphs/{read}_barplottime_result.png",
        mem= "{read}/graphs/{read}_barplotmemory_result.png"
    shell:
        "python3 memtime_to_barplot.py --opt {input.opt_tri} {input.opt_k2r} --tri {input.tri_minimap} {input.tri_miniasm} {input.tri_memtime} {input.tri_k2r} --rand {input.rand_tri} {input.rand_k2r} --timeplot_out {output.time} --memoryplot_out {output.mem}"