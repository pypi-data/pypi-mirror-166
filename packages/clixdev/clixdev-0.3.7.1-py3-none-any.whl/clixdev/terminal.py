import argparse


def terminal():
    try:
        parser = argparse.ArgumentParser(prog="clixdev", description="Clix.dev command line tool.")
        parser.add_argument('action', choices=['generate'])
        parser.add_argument('terminal_token', type=str)
        parser.add_argument('project_token', type=str)
        parser.add_argument('-dir', type=str, required=False)
        args = parser.parse_args()

        if args.action == 'generate':
            from .generators.django_writer import generate
            generate(args.terminal_token, args.project_token, args.dir)
            return True
        
        return False
    except Exception as e:
        print(e)
        return False
