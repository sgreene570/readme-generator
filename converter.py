"""
converter.py
Convert those silly plain text readmes to markdown easily!
"""


import subprocess
import requests
import json
import argparse
from shutil import copyfile


# Project information
__author__ = "Stephen Greene, and Matt Dzwonczyk"
__copyright__ = "Copyright 2017, The Cogent Project"
__credits__ = ["Stephen Greene", "Matt Dzwonczyk"]
__license__ = "MIT"
__version__ = "1.0.0"


# Important string constants
NEWLINE = "\n"
NEWLINE_MD = "<br>"
HEADING_MD = "#"
INPUT_FILE = "README.md"
OUTPUT_FILE = "OUTPUT.md"
BACKUP_FILE = "README.backup"
# Character used to enclose code segments where href tags should be inserted
LINK_CHAR = "_"


def main():
    """
    Entry point for converter.py.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--lang", action="store_true",
                        help="add repository language information to the readme")
    parser.add_argument("-c", "--contrib", action="store_true",
                        help="add repository contributor information to the " +
                        "readme")
    parser.add_argument("-f", "--fast", action="store_true",
                        help="replace the existing README.md without asking" +
                        " (still creates a README.backup)")
    args = parser.parse_args()

    repo_url = get_repo_url()
    api_url = get_api_url(repo_url)
    repo_contents = requests.get(api_url + "/contents")
    raw_files = get_raw_files(repo_contents)    # List of available files

    copyfile(INPUT_FILE, BACKUP_FILE) # Make a backup copy

    readmetxt = open(INPUT_FILE, "r")
    readmemd = open(OUTPUT_FILE, "w")
    lines = readmetxt.readlines()

    for x in range(len(lines)):
        line = lines[x]     # Create a copy of the current line
        for y in range(len(line)):      # Iterate over each char
            # Check if a line has LINK_CHARs to denote url zone
            if line[y] == LINK_CHAR and line[y+1:].count(LINK_CHAR) % 2 == 1:
                find_string = line[y+1:line[y+1:].index(LINK_CHAR) + y+1]
                print(find_string)
                for file_url in raw_files:
                    line_number = find_in_file(file_url, find_string)
                    if line_number is not -1:
                        print(line_number)
                        # Insert the href link to the correct line number
                        lines[x] = (line[:y-1] + "<a href=" +
                                    repo_contents.json()[raw_files.index(file_url) + 1]
                                    ["html_url"] + "#L" + str(line_number) + ">" +
                                    line[y+1:y+len(find_string)+1] + "</a>" +
                                    line[y+len(find_string)+2:])
                        break

        line = clean_line(lines[x])     # Update the copied line

        # Don't add empty lines
        # TODO: Is this harmful to custom formatting with lots of empty lines?
        if line == "\n":
            continue

        # Check if line is a heading
        if (x+1 < len(lines) and len(line) > 2 and line[-2] == ":" and
                lines[x+1] == NEWLINE):
            readmemd.write(HEADING_MD + line)
            x += 1
        else:
            readmemd.write(line + NEWLINE_MD)

        # Insert a normal new line for viewing
        # the markdown file in a text editor
        readmemd.write(NEWLINE)

    # Add repository language info at the bottom
    # if the user used the lang parameter
    if args.lang:
        readmemd.write(get_languages(api_url))

    # Add repository contributor info at the bottom
    # if the user used the contrib parameter
    if args.contrib:
        readmemd.write(get_contributors(api_url))

    # Wrap up file IO
    readmemd.flush()
    readmemd.close()
    readmetxt.close()

    # Confirmation message
    print("Formatted README generated to OUTPUT.md.")

    # Fast argument for automatically replacing the old README with the new
    if args.fast:
        copyfile(OUTPUT_FILE, INPUT_FILE) # Make a backup copy
    else:
        replace = input("Replace the README.md with the new OUTPUT.md contents? "
                        + "(A backup can be found in README.backup): ")
        if replace == "y" or replace == "yes":
            copyfile(OUTPUT_FILE, INPUT_FILE) # Make a backup copy
            print("README.md replaced with OUTPUT.md contents.")
        else:
            print("README.md not replaced with OUTPUT.md contents.")


def clean_line(line):
    """
    Removes existing <br> line breaks from the file so they don't multiply.
    """
    return line.replace("<br>", "")


def get_languages(api_url):
    """
    Return a "Languages Used" header and a list of languages used to add to the
    and the number of bits of that language to the README file.
    """
    languages_str = NEWLINE + "<br>" + NEWLINE + "##Languages Used" + NEWLINE + "<br>"
    languages = requests.get(api_url + "/languages").json()

    # Create the unordered list element
    languages_str += NEWLINE + "<ul>"
    for key, value in languages.items():
        language = key
        bits = value
        languages_str += NEWLINE + "<li>" + str(language) + " (" + str(bits) + " bits)</li>"

    # End the unordered list
    languages_str += NEWLINE + "</ul>"

    return languages_str


def get_contributors(api_url):
    """
    Return a "Contributors" header and a list of contributors to add to the
    README file.
    """
    contributors_str = NEWLINE + "<br>" + NEWLINE + "##Contributors" + NEWLINE + "<br>"
    contributors = requests.get(api_url + "/contributors").json()

    # Create the unordered list element
    contributors_str += NEWLINE + "<ul>"
    for x in range(len(contributors)):
        login = str(contributors[x]["login"])
        contributors_str += NEWLINE + "<li><a href='https://github.com/" + login +"'>" + login + "</a></li>"

    # End the unordered list
    contributors_str += NEWLINE + "</ul>"

    return contributors_str


def get_repo_url():
    """Return the repository origin remote URL via the command line."""
    # TODO: Is there a better way?
    repo_url = str(subprocess.check_output("git remote get-url origin",
                   shell=True))
    repo_url = repo_url[repo_url.index("'") + 1: -3]
    return repo_url


def get_api_url(repo_url):
    """Return the GitHub API URL for the respository."""
    api_url = None
    # If the remote url is set for SSH keys
    if repo_url[:3] == "git":
        api_url = ("https://api.github.com/repos/" +
                   repo_url[repo_url.index(":") + 1: -3])
    # If the remote url is set for http/https
    elif repo_url[:4] == "http":
        api_url = ("https://api.github.com/repos/" +
                   repo_url[repo_url.index(".com/") + 5:-4])

    return api_url


def get_raw_files(repo_contents):
    """
    Scrape the repo_contents response object for all of the names of the
    available files in the repo and return them in a list.
    """
    contents = repo_contents.json()
    raw_files = list()
    for x in range(len(contents)):
        # TODO: Should probably check for a KeyError here
        if contents[x]["name"] != "README.md":          # Skip the readme
            raw_files.append(contents[x].get("download_url"))

    # FIXME: print(raw_files)
    return(raw_files)


def find_in_file(file_url, string):
    """
    Find the location of the given string in the given file URL
    and return the line number of the string if found
    """
    # FIXME: This should probably return -1 if the string is not
    # found in the file for consistency.
    code = requests.get(file_url).text
    if string in code:
        return code[:code.index(string)].count(NEWLINE) + 1
    else:
        return -1;


if __name__ == "__main__":
    main()
