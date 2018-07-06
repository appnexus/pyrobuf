from pyrobuf.compile import Compiler


if __name__ == "__main__":
    compiler = Compiler.parse_cli_args()
    compiler.compile()
