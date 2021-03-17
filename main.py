#!/usr/bin/python

from os import mkdir
import argparse
import pathlib
import time
import string
from jinja2 import Environment, FileSystemLoader


def init_argparse():
    parser = argparse.ArgumentParser(
            prog="python auto_proj_builder.py",
            usage="%(prog)s --author 'name_string' --project_title \
'project_string'",
            description="Creates readme.md and main.py, filled with some \
                         boilerplate, to new directory project_name\n\n"
            )
    parser.add_argument(
            "-v", "--version", action="version",
            version="{parser.prog} version 1.0.0"
            )
    parser.add_argument(
            "-a", "--author", action='store',
            help="The name of the author for this new project, in quotes. \
                    Max 40 chars."
            )
    parser.add_argument(
            "-p", "--project_title",
            help="The title of this new project, max 40 chars, no whitespace."
            )
    parser.add_argument(
            "-d", "--description", action='store', default="",
            help="A single-line descrption of the project."
            )
    return parser


def render_output(project_path,
                  template_path,
                  template_filename,
                  output_filename,
                  argument_dict):

    # Environment for jinja
    env = Environment(
            loader=FileSystemLoader(template_path)
            )

    # Set up some paths
    template_path = template_path + template_filename
    output_path = project_path + output_filename

    # Open and read our template
    _template = env.get_template(template_filename)
    template_str = open(template_path, mode='r').read()

    # Process the template into our new output
    new_output_str = _template.render(project_name=argument_dict["proj_title"],
                                      author_name=argument_dict["author"],
                                      description=argument_dict["description"])

    # print(f"Creating readme in {project_path}")
    with open(output_path, "w") as new_file:
        new_file.write(new_output_str)
    pass


def is_valid_input_format(arg_type, argument):
    if len(argument) > 40:
        print(f"\nError: the {arg_type} argument you entered ({argument}) exceeds \
the max length of 40 (by {len(argument)-40}). Try again.")
        return False

    if arg_type == "project_title":
        for char in argument:
            if char in string.whitespace:
                print("\nError: no white space allowed in the project name \
({project_name}). Try again")
                return False
    return True


def main():
    parser = init_argparse()
    args = parser.parse_args()

    author_name = args.author
    if not is_valid_input_format("author", author_name):
        return -1

    project_title = args.project_title
    if not is_valid_input_format("project_title", project_title):
        return -1

    proj_description = args.description

    arg_dict = {"author": author_name, "proj_title": project_title,
                "description": proj_description}

    current_wd = pathlib.Path().absolute()
    parent_path = str(current_wd.parent)

    new_dir_path = parent_path + "/" + project_title + "_" + \
        str(time.time()) + "/"

    print(f"Creating project {project_title} by {author_name}")
    print(f"Creating directory {new_dir_path}")
    mkdir(new_dir_path)

    template_path = str(current_wd) + "/templates/"

    render_output(new_dir_path, template_path, "README_template.md",
                  "README.md", arg_dict)
    render_output(new_dir_path, template_path, "main_template.py",
                  "main.py", arg_dict)
    render_output(new_dir_path, template_path, "todo_template.md",
                  "TODO.md", arg_dict)

if __name__ == "__main__":
    main()
