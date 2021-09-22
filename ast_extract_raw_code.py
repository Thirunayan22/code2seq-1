import os
import json
import common
import platform
import subprocess
from threading import Timer
from argparse import ArgumentParser
from preprocess import process_file,save_dictionaries

class extractAST:

    def __init__(self,dataset_dir):

        self.extractor_jar_path = "JavaExtractor/JPredict/target/JavaExtractor-0.0.1-SNAPSHOT.jar"
        self.extractor_num_threads = 64
        self.max_path_length = 8
        self.max_path_width = 2
        self.max_contexts = 200
        self.max_data_contexts = 200
        self.subtoken_vocab_size = 186277
        self.target_vocab_size = 26347
        self.num_threads = 10
        
        self.dataset_dir = dataset_dir



        self.train_data_file = f"{self.dataset_dir}/train_ast.raw.txt"
        self.target_histogram_file = f"{self.dataset_dir}/train_ast.histo.tgt.c2s"
        self.source_subtoken_histogram_file = f"{self.dataset_dir}/train_ast.histo.ori.c2s"
        self.node_histogram_file = f"{self.dataset_dir}/train_ast.histo.node.c2s"

        if not os.path.exists(self.dataset_dir):
            os.mkdir(self.dataset_dir)

        else:

            if len(os.listdir(self.dataset_dir)) > 0 :
                print("Existing Histogram and .c2s dataset files found, deleting all old files...")
                for file in os.listdir(self.dataset_dir):
                    file_path = os.path.join(self.dataset_dir,file)
                    if os.path.exists(file_path):
                        os.remove(file_path)

        


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
                sleeper = subprocess.Popen(file_extraction_command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,)
                extracted_ast_output = sleeper.communicate()[0].rstrip()
                timer = Timer(60*60,kill,[sleeper])

                output_file.write(extracted_ast_output.decode(encoding="utf-8"))
                

        else:
            
            sleeper = subprocess.Popen(file_extraction_command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            extracted_ast_output = sleeper.communicate()[0].rstrip()
            timer = Timer(60*60,kill,[sleeper])

        print("Ending function")
        return extracted_ast_output
    
    def extract_histogram(self):

        """ 
        preprocesses the contents of a given ast file to create histogram

        Params:
            extracted_ast : generated ast from source code

        """



        if not os.path.exists(self.train_data_file):
            raise Exception("Generate raw ast file before running preprocessing function")

        # The preprocess_wsl_commands.sh file contains the bash commands for preprocessing along with the output file paths
        histogram_extraction_command = "./preprocess_wsl_commands.sh"

        if platform.system().lower() == "windows" :

            try:
                print("Inside WSL Execution")
                histogram_extraction_command = 'wsl ' + f'{histogram_extraction_command}'

            except Exception as e:
                print(e)
                raise Exception("Please check whether you have WSL installed on your windows machine")

        print("Histogram Execution Command : ",histogram_extraction_command)

        generate_histogram_status = os.system(histogram_extraction_command)

        print("Histogram Command Execution Status : ",generate_histogram_status)


    def preprocess_ast(self):

        """
        Takes in a histogram, preprocesses and truncates AST paths which are too long
        """

        subtoken_to_count_hist = common.Common.load_histogram(path=self.source_subtoken_histogram_file,
                                                              max_size=int(self.subtoken_vocab_size))
        node_to_count_hist = common.Common.load_histogram(path=self.node_histogram_file,
                                                          max_size=None)

        target_to_count_hist = common.Common.load_histogram(path=self.target_histogram_file,
                                                            max_size=self.target_vocab_size)


        num_training_examples = 0
        dataset_name = f"{self.dataset_dir}/{self.dataset_dir}"
        num_examples = process_file(file_path=self.train_data_file,
                                    data_file_role="test",
                                    dataset_name=dataset_name,
                                    max_contexts=self.max_contexts,
                                    max_data_contexts=self.max_data_contexts
                                    )

        save_dictionaries(dataset_name=dataset_name,
                          subtoken_to_count=subtoken_to_count_hist,
                          node_to_count=node_to_count_hist,
                          target_to_count=target_to_count_hist,
                          max_contexts=self.max_data_contexts,
                          num_examples=num_training_examples)


        return num_examples


if __name__ == '__main__':

    parser =  ArgumentParser()
    parser.add_argument("--save_file",required=True)
    args = parser.parse_args()
    
    test_java_file_path = "Input.source"
    ast_extractor = extractAST(dataset_dir="generated_ast_dataset")

    save_output = json.loads(args.save_file.lower())
    ast_extracted_output = ast_extractor.extract_from_file(test_java_file_path,save_output=save_output)

    print("AST Extracted")
    print(f"AST extracted output : {ast_extracted_output}")

    print("Generating Histograms...")
    ast_extractor.extract_histogram()

    print("Using Generated Histograms To Preprocess And Shorten Paths")
    ast_extractor.preprocess_ast()




