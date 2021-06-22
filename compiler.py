from parser import Parser
from generator import Generator
from tokenizer import Tokenizer
from enums import NL

def compile_file(file_name):
    tokens = Tokenizer(file_name).tokenize()
    print("===============")
    print("".join([str(token) +
                   f"{NL if index < len(tokens) - 1 else ''}"
                   for index, token in enumerate(tokens)]
                  )
          )

    tree = Parser(tokens).parse()
    print(tree)
    generated_code = Generator().generate(tree)
    print("++++++++++++")
    print(generated_code)
    Generator.write_code_to_working_directory(generated_code, f"{file_name[:-3]}_result.py")


if __name__ == '__main__':
    compile_file("test3.js")
    compile_file("test.js")
    compile_file("test1.js")
    compile_file("test2.js")
