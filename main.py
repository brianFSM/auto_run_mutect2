from os import mkdir
import argparse
import pathlib
import time
import string
# from jinja2 import Environment, FileSystemLoader


def init_argparse():
    parser = argparse.ArgumentParser(
            prog="python auto_run_mutect2.py",
            usage="%(prog)s --sample_base 'sample_base'",
            description="Creates, and submits to slurm, a script for \
                         running mutect2 based on the number of tumor/normal \
                         samples"
            )
    parser.add_argument(
            "-v", "--version", action="version",
            version="{parser.prog} version 1.0.0"
            )
    parser.add_argument(
            "-s", "--sample_base", action='store',
            help="The sample base."
            )
    parser.add_argument(
            "-r", "--reference", action='store',
            default="hg38",
            help="The reference genome."
            )
    return parser


def main():
    parser = init_argparse()
    args = parser.parse_args()

    sample = args.sample_base
    filename = "data/reads/samples/" + sample + ".txt"

    normals_list = list()
    tumors_list = list()

    with open(filename) as f:
        sample_files = f.readlines()

    print(f"This is sample {sample}")
    print(f"The filename is {filename}")
    for line in sample_files:
        if "P1" in line or "P2" in line:
            tumors_list.append(line)
        elif "PBL" in line:
            normals_list.append(line)
        else:
            print(f"Watch out, {line} doesn't have P1, P2, or PBL in the \
                  sample name.")

    print(f"There are {len(normals_list)} normals and {len(tumors_list)} tumors")
    print()


if __name__ == "__main__":
    main()
