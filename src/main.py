import os
from .parser import create_arg_parser


def main():
    # Clear terminal screen before starting
    os.system("cls" if os.name == "nt" else "clear")

    # Get parser
    args, args_help = create_arg_parser()

    if args.command:
        args.func(args)
    else:
        args_help()


if __name__ == "__main__":
    main()