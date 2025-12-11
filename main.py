#!/usr/bin/env python3
from dotenv import load_dotenv 
load_dotenv() 

from core.generator import generate_command
from core.seeder import seed_command
import argparse
import sys
from core.docker import up_command, down_command
from core.utils import check_docker

def main():
    parser = argparse.ArgumentParser(description="Formbricks Data Seeder CLI")
    parser.add_argument('--verbose', '-v', action='store_true')

    subparsers = parser.add_subparsers(dest='group', required=True)
    fb_parser = subparsers.add_parser('formbricks', help='Formbricks commands')
    fb_sub = fb_parser.add_subparsers(dest='command', required=True)

    # up command
    up_p = fb_sub.add_parser('up', help='Start Formbricks containers.')
    up_p.set_defaults(func=up_command)

    # down command
    down_p = fb_sub.add_parser('down', help='Stop and clean up Formbricks containers.')
    down_p.set_defaults(func=down_command)

    # generate command
    gen_p = fb_sub.add_parser('generate', help='Generate realistic data via LLM.')
    gen_p.set_defaults(func=generate_command)

    # seed command
    seed_p = fb_sub.add_parser('seed', help='Fill the app with data using APIs.')
    seed_p.set_defaults(func=seed_command)

    args = parser.parse_args()
    args.verbose = args.verbose or getattr(args, 'verbose', False)

    if args.group == 'formbricks':
        check_docker()
        args.func(args)

if __name__ == "__main__":
    main()