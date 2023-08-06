
import os
from dreem_herschlag import util
                
class RNAstructure(object): #TODO
    def __init__(self, config) -> None:
        self.config = config
        self.rnastructure_path = config['path_to_RNAstructure'] if config['path_to_RNAstructure'][-1] == '/' else config['path_to_RNAstructure']+'/'

    def make_temp_folder(self, samp):
        temp_folder = 'temp/'+ samp + '/rnastructure/'
        isExist = os.path.exists(temp_folder)
        if not isExist:
            os.makedirs(temp_folder)
        return temp_folder

    def make_files(self, temp_prefix):
        self.ct_file = f"{temp_prefix}.ct"
        self.dot_file = f"{temp_prefix}_dot.txt"
        self.fasta_file = temp_prefix+'.fasta'

    def create_fasta_file(self, construct, sequence):
        # push the ref into a temp file
        temp_fasta = open(self.fasta_file, 'w')
        temp_fasta.write('>'+construct+'\n'+sequence)
        temp_fasta.close()

    def predict_construct(self):
        # Run RNAstructure
        util.run_command(f"{self.rnastructure_path}Fold {self.fasta_file} {self.ct_file} -d")
        assert os.path.getsize(self.ct_file) != 0, f"{self.ct_file} is empty, check that RNAstructure works"

    # cast the temp file into a dot_bracket structure and extract the attributes
    def extract_deltaG_struct(self):
        util.run_command(f"ct2dot {self.ct_file} 1 {self.dot_file}")
        temp_dot = open(self.dot_file, 'r')
        first_line = temp_dot.readline().split()
        # If only dots in the structure, no deltaG 
        if len(first_line) == 4:
            _, _, deltaG, _ = first_line
            deltaG = float(deltaG)
        if len(first_line) == 1:
            deltaG, _ = 'void', first_line[0][1:]

        _ = temp_dot.readline()[:-1] #  Remove the \n
        structure = temp_dot.readline()[:-1] # Remove the \n
        return deltaG,structure

    def run(self, samp, construct, sequence):
        temp_folder = self.make_temp_folder(samp)
        self.make_files(f"{temp_folder}{construct}")
        self.create_fasta_file(construct, sequence)
        self.predict_construct()
        return self.extract_deltaG_struct()

