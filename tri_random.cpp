#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <cstdlib>
#include <unistd.h>
#include <climits>
#include <algorithm>
#include <map>

using namespace std;

vector<uint64_t> read_line_position(const string& filename){
    vector<uint64_t> read_line_pos={0};
    fstream file(filename, ios::in);
    if(file){
        string line;
        uint64_t total_count = 0;
        while(!file.eof()){
            getline(file, line);
            total_count += line.length();
            read_line_pos.push_back(total_count+1);
        }
        return read_line_pos;
    }
    else{
        cerr << "Error opening the file (read_line_position)." << endl;
    }
    return {};
}

string get_read_sequence(const vector<uint64_t>& read_line_pos, const string& filename, uint64_t read_id){
    auto pos_seq = read_line_pos[(read_id*2)+1];
    auto pos_entete_suivant = read_line_pos[(read_id*2)+2];

    fstream file_in(filename, ios::in);
    char line_seq[100000];
    if(file_in){
        file_in.seekg((pos_seq+read_id*2), file_in.beg);
        file_in.read(line_seq, ((pos_entete_suivant+read_id)-(pos_seq+read_id)));
        //line_seq[((pos_entete_suivant+read_id*2)-(pos_seq+read_id))] = 0;
        line_seq[pos_entete_suivant-pos_seq+2] = 0;
        file_in.close();
        return line_seq;
    }
    else{
        cerr << "Error opening the input file (get_read_sequence)." << endl;
    }
    return "";
}

vector<int> random_read_order(uint64_t nb_reads){
    srand((unsigned) time(NULL));
    vector<int> read_order(nb_reads);
    for(int i = 0; i<read_order.size(); i++){
        read_order[i] = i;
    }
    int index=0;
    for(int i = 0; i<read_order.size(); i++){
        index=rand()%read_order.size();
        int tmp = read_order[index];
        read_order[index]=read_order[i];
        read_order[i] = tmp;
    }
    return(read_order);
}

void random_reads_sorting(const string& reads_file, const string& out_file){
    //les reads sont triés aléatoirement
    vector<uint64_t> read_line_pos = read_line_position(reads_file);
    vector<int> read_order = random_read_order(read_line_pos.size()/2-1);
    vector<int> permutation_vector(read_order.size(), 0);
    fstream out(out_file, ios::out);
    if(out){
        for(int i = 0; i<read_order.size(); i++){
            out << ">"+to_string(read_order[i]) << endl;
            out << get_read_sequence(read_line_pos, reads_file, read_order[i]) << endl;
            permutation_vector[read_order[i]] = i;
        }
    }
}

int main(int argc, char *argv[])
{
    if (argc!=3){
        cerr << "Mauvais nombre d'arguments" << endl;
    }
    string readsfile = argv[1];
    string outfile = argv[2];
    random_reads_sorting(readsfile, outfile);
    return 0;
}