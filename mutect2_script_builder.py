'''
docstring for module is here
'''
# from os import mkdir
import argparse
import pathlib
# import time
# import string
from jinja2 import Environment, FileSystemLoader


def init_argparse():
    '''
    function docstring goes here
    '''
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


def get_param_template(filebase_list, mode):
    '''
    function docstring goes here
    '''

    param_list = list()
    for filebase in filebase_list:
        filebase = filebase.replace("\n", "")
        if mode == "bam":
            param = "\t-I ${bam_dir}/" + filebase + "_recalibrated.bam"
        elif mode == "norm_samplename":
            param = "\t-normal " + filebase
        param_list.append(param)

    return param_list



def render_output(project_path,
                  template_path,
                  template_filename,
                  output_filename,
                  argument_dict,
                  tumor_only=False):

    '''
    function docstring goes here
    '''
    # Environment for jinja
    env = Environment(
        loader=FileSystemLoader(template_path))

    # Set up some paths
    template_path = str(template_path) + template_filename
    output_path = str(project_path) + "/" + output_filename

    # Open and read our template
    _template = env.get_template(template_filename)
    template_str = open(template_path, mode='r').read()


    # First grab the tumor bam filenames and turn them into a mutect2
    # argument
    tumor_files_template = get_param_template(argument_dict["tumors"],
                                              "bam")

    end_line_string = " \\\n"
    tumor_file_string = ""
    normal_file_string = ""
    normal_name_string = ""

    for tumor_file_arg in tumor_files_template:
        tumor_file_string += tumor_file_arg + end_line_string

    # Then, if there are normals, do the same with the normal samples
    if not tumor_only:
        normal_files_template = get_param_template(argument_dict["normals"],
                                                   "bam")
        normal_names_template = get_param_template(argument_dict["normals"],
                                                   "norm_samplename")

        for normal_file_arg in normal_files_template:
            normal_file_string += normal_file_arg + end_line_string
        for normal_name_arg in normal_names_template:
            normal_name_string += normal_name_arg + end_line_string


    # Process the template into our new output
    new_output_str = _template.render(reference=argument_dict["reference"],
                                      tumor_files=tumor_file_string,
                                      normal_files=normal_file_string,
                                      normal_samples=normal_name_string,
                                      sample=argument_dict["sample"])

    with open(output_path, "w") as new_file:
        new_file.write(new_output_str)



def main():
    '''
    docstring goes here
    '''
    # parse the arguments and store them
    parser = init_argparse()
    args = parser.parse_args()

    reference = args.reference
    sample = args.sample_base
    filename = "data/reads/samples/" + sample + ".txt"
    has_normals = False

    # Setup the directories
    current_wd = pathlib.Path().absolute()
    # parent_path = str(current_wd.parent)
    # new_dir_path = parent_path + "/" + project_title + "_" + \
        # str(time.time()) + "/"

    with open(filename) as f:
        sample_files = f.readlines()

    # Separate the sample in the list into the normal and tumor lists
    normals_list = list()
    tumors_list = list()
    for line in sample_files:
        if "P1" in line or "P2" in line:
            tumors_list.append(line)
        elif "PBL" in line:
            normals_list.append(line)
            has_normals = True
        else:
            print(f"Watch out, {line} doesn't have P1, P2, or PBL in the \
                  sample name.")

    print(f"There are {len(normals_list)} normals and {len(tumors_list)} tumors")
    print()


    arg_dict = {"sample": sample, "normals": normals_list,\
                "tumors": tumors_list, "reference": reference}
    template_path = str(current_wd) + "/templates/"
    output_file = sample + "_mutect2_norm_tumor.sh"

    render_output(current_wd, template_path, "mutect2_norm_tumor_template.sh",
                  output_file, arg_dict, tumor_only = has_normals)


if __name__ == "__main__":
    main()
