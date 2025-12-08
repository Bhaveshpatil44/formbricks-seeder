#!/usr/bin/env python3
from core.generator import generate_command
from core.seeder import seed_command
import argparse
import sys
from core.docker import up_command, down_command
from core.utils import check_docker

def main():
    parser = argparse.ArgumentParser(description="Formbricks Seeder")
    parser.add_argument('--verbose', '-v', action='store_true')

    subparsers = parser.add_subparsers(dest='group', required=True)
    fb_parser = subparsers.add_parser('formbricks', help='Formbricks commands')
    fb_sub = fb_parser.add_subparsers(dest='command', required=True)

    # up
    up_p = fb_sub.add_parser('up', help='Start Formbricks')
    up_p.add_argument('--verbose', '-v', action='store_true')
    up_p.set_defaults(func=up_command)

    # down
    down_p = fb_sub.add_parser('down', help='Stop Formbricks')
    down_p.add_argument('--verbose', '-v', action='store_true')
    down_p.set_defaults(func=down_command)

    # generate
    gen_p = fb_sub.add_parser('generate', help='Generate realistic data')
    gen_p.add_argument('--verbose', '-v', action='store_true')
    gen_p.set_defaults(func=generate_command)

    # seed
    seed_p = fb_sub.add_parser('seed', help='Seed everything via API')
    seed_p.add_argument('--verbose', '-v', action='store_true')
    seed_p.set_defaults(func=seed_command)

    args = parser.parse_args()
    args.verbose = args.verbose or getattr(args, 'verbose', False)

    if args.group == 'formbricks':
        check_docker()
        args.func(args)

if __name__ == "__main__":
    main()