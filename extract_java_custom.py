from common import Common
from java_extractor import JavaExtractor
from cpp_extractor import CppExtractor
from config import Config


SHOW_TOP_CONTEXTS = 10
MAX_PATH_LENGTH = 8
MAX_PATH_WIDTH = 2
EXTRACTION_API = 'https://po3g2dx2qa.execute-api.us-east-1.amazonaws.com/production/extractmethods'

args = None
config = Config.get_default_config(args)
path_extractor = JavaExtractor(config, EXTRACTION_API, config.MAX_PATH_LENGTH, max_path_width=2)

with open("Input.source","r") as file:
    source_input =  ' '.join(file.readlines())

predict_lines,pc_info_dict = path_extractor.extract_paths(source_input)

print("Predict Lines",predict_lines)
print("Predict PC Info dict : ",pc_info_dict)


# TODO - 0 - Try out from interactive_predict to pass in java source code from the java small dataset - ✅
# TODO - 1 - Reconfirm that the Jetbrains Pytorch implementation does not have any dataset generation methods  - ✅ - Egor Spirin responded the source code path should be extracted using a "tool", you have put an issue asking what he means by "tool". 
# TODO - 2 - convert extract.py path extraction operations to be callable through methods - ✅
# TODO - 3 - save extracted paths as files intermediarily and then run the "cat ..." preprocessing functions to create the histogram  - ✅
# TODO - 4 - use preprocess.py and preprocess data to truncate methods with too many path context and pad methods with less paths  - ✅
# TODO - 5 - Build a function that can take in a source code file as input and can output a ast-context path that can be directly fed into the model - ✅
# TODO - 6 - Adapt the linux preprocessing bash commands to run on windows - ✅
# TODO - 7 - Change function to take in a string java input, convert it to a file get the extracted ast, pass it to the model and delete the generated files
# TODO - 8 - Move back to pytorch code2seq implementation codebase and check how this extracted code2seq ast can be input to the pytorch model implementation, you can use Egor Spirin's response to your second message as well - ✅
# TODO - 9 - Convert the ast_raw_code_extract class to an importable module in the CognitiveCodeAnalyze codebase
# TODO - 10 - Convert the ast_test file in the Pytorch Codebase to an importable module in the CognitiveCodeAnalyze codebase
# TODO - 11 - Filter outputs of encoder/decoder embedding layers only from the pytorch code2seq model
# TODO - 12 - Respond to Egor Spirin and thank him for his quick response and support and also ask him if he would be open for a contribution for the individual inference module


