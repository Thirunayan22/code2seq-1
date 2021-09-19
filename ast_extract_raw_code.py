import os
import json
import subprocess
from threading import Timer
from argparse import ArgumentParser


class extractAST:

    def __init__(self,dataset_dir):

        self.extractor_jar_path = "JavaExtractor/JPredict/target/JavaExtractor-0.0.1-SNAPSHOT.jar"
        self.extractor_num_threads = 64
        self.max_path_length = 8
        self.max_path_width = 2
        
        self.dataset_dir = dataset_dir

        self.train_data_file = f"{self.dataset_dir}/train_ast.raw.txt"
        self.target_histogram_file = f"{self.dataset_dir}/train_ast.histo.tgt.c2s"
        self.source_subtoken_histogram = f"{self.dataset_dir}/train_ast.histo.ori.c2s"
        self.node_histogram_file = f"{self.dataset_dir}/train_ast.histo.node.c2s"


        if not os.path.exists(self.dataset_dir):
            os.mkdir(self.dataset_dir)
            with open(f"{self.train_data_file}","w+") as train_dataset_file:
                pass

            with open(f"{self.target_histogram_file}","w+") as targe_histogram_file:
                pass

            with open(f"{self.source_subtoken_histogram}","w+") as source_subtoken_hist_file:
                pass

            with open(f"{self.node_histogram_file}","w+") as node_histogram_file:
                pass
        


    def extract_from_file(self,java_file_path,save_output=False):

        """
        Extracts AST given raw java file

        Params : 
            java_file_path : path to raw java file
            save_output : saves extracted ast as a file if set to True
        """

        extracted_ast_output = ""
        file_extraction_command =  'java -cp ' + self.extractor_jar_path + ' JavaExtractor.App --max_path_length ' + \
                    str(self.max_path_length) + ' --max_path_width ' + str(self.max_path_width) + ' --file ' + java_file_path

        kill = lambda process: process.kill()


        print(f"Save file mode : {save_output}")

        if save_output:
            with open(f"{self.train_data_file}","a+") as output_file:
                sleeper = subprocess.Popen(file_extraction_command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                extracted_ast_output = sleeper.communicate()[0].rstrip()
                timer = Timer(60*60,kill,[sleeper])

                output_file.write(extracted_ast_output.decode(encoding="utf-8"))
                

        else:
            
            sleeper = subprocess.Popen(file_extraction_command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            extracted_ast_output = sleeper.communicate()[0].rstrip()
            timer = Timer(60*60,kill,[sleeper])

        print("Ending function")
        return extracted_ast_output
    
    def preprocess_ast(self,extracted_ast):

        """ 
        preprocesses the contents of a given ast file to create histgram and 
        truncate methods with too many context

        Params:
            extracted_ast : generated ast from source code

        """

        target_hist_command = f"cat {self.train_data_file} | cut -d' ' -f1 | tr '|' '\n' | awk 'cccccc' > {self.target_histogram_file}"

        subtoken_hist_command = f"cat {self.train_data_file} | cut -d' ' -f2- | tr ' ' '\n' | cut -d',' -f1,3 | tr ',|' '\n' | awk" + " '{n[$0]++} END {for (i in n) print i,n[i]}' > " + f"{self.source_subtoken_histogram}"

        node_hist_command = f"cat {self.train_data_file} | cut -d' ' -f2- | tr ' ' '\n' | cut -d',' -f2 | tr '|' '\n' | awk"  + " '{n[$0]++} END {for (i in n) print i,n[i]}' > " + f"{self.node_histogram_file}"
        
        generate_target_histogram_status = os.system(target_hist_command)
        # timer = Timer(60*60,kill,[generate_target_histogram])

        generate_subtoken_histogram_status = os.system(subtoken_hist_command)
        # timer = Timer(60*60,kill,[generate_subtoken_histogram])

        generate_node_histogram_status = os.system(node_hist_command)
        # timer = Timer(60*60,kill,[generate_node_histogram])

        print("Target Histogram Execution Status : ",bool(generate_target_histogram_status))
        print("Subtoken Histogram Execution Status : ",bool(generate_subtoken_histogram_status))
        print("Node Histogram Execution Status : ",bool(generate_node_histogram_status))

if __name__ == '__main__':

    parser =  ArgumentParser()
    parser.add_argument("--save_file",required=True)
    args = parser.parse_args()
    
    test_java_file_path = "./Input.source"
    ast_extractor = extractAST(dataset_dir="./generated_ast_dataset")

    save_output = json.loads(args.save_file.lower())
    ast_extracted_output = ast_extractor.extract_from_file(test_java_file_path,save_output=save_output)

    print("AST Extracted")
    # print(f"AST extracted output : {ast_extracted_output}")

    print("Generating Histograms...")
    ast_extractor.preprocess_ast(ast_extracted_output)



