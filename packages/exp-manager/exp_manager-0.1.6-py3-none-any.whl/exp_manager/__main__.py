from exp_manager.parser import parser

def main():
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
