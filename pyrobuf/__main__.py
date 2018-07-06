from pyrobuf.compile import Compiler


def main():
    compiler = Compiler.parse_cli_args()
    compiler.compile()


if __name__ == "__main__":
    main()
