"""
converter.py
Convert those silly plain text readmes to markdown easily!
"""


import sys
import subprocess
import requests
import json
import argparse
import getpass
from shutil import copyfile
from requests.auth import HTTPBasicAuth


# Project information
__author__ = "Stephen Greene, and Matt Dzwonczyk"
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

    copyfile(INPUT_FILE, BACKUP_FILE)    # Make a backup copy

    # Parse the file and remove any info that must be regenerated
    lines = parse_lines(INPUT_FILE)
    readmemd = open(OUTPUT_FILE, "w")

    wroteLangBlock = False    # Whether a lang block has been generated
    wroteContribBlock = False    # Whether a contrib block has been generated

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
                        # print(line_number)
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
        if not line.strip():
            continue

        if args.lang and "<!--END READMELANG-->" in line:
            # Write new lang block
            readmemd.write(get_languages(api_url, False))
            wroteLangBlock = True
        elif args.contrib and "<!--END READMECONTRIB-->" in line:
            # Write new contrib block
            readmemd.write(get_contributors(api_url, False))
            wroteContribBlock = True

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
    if not wroteLangBlock and args.lang:
        readmemd.write(get_languages(api_url, True))

    # Add repository contributor info at the bottom
    # if the user used the contrib parameter
    if not wroteContribBlock and args.contrib:
        readmemd.write(get_contributors(api_url, True))

    # Wrap up file IO
    readmemd.flush()
    readmemd.close()

    # Confirmation message for OUTPUT.md generation completetion
    print("Formatted README generated to OUTPUT.md.")

    # Fast argument for automatically replacing the old README with the new
    if args.fast:
        copyfile(OUTPUT_FILE, INPUT_FILE)    # Make a backup copy
    else:
        replace = input("Replace the README.md with the new OUTPUT.md " +
                        " contents? (A backup can be found in README.backup): ")
        if replace == "y" or replace == "yes":
            copyfile(OUTPUT_FILE, INPUT_FILE)    # Make a backup copy
            print("README.md replaced with OUTPUT.md contents.")
        else:
            print("README.md not replaced with OUTPUT.md contents.")


def clean_line(line):
    """
    Removes existing <br> line breaks from the file so they don't multiply.
    """
    return line.replace("<br>", "")


def parse_lines(file_name):
    """
    Returns a list of all text in file file_name, but with text between the
    start and end strings (repository-generated data) removed.
    """
    in_file = open(INPUT_FILE, "r")
    break_strings = [("<!--BEGIN READMELANG-->", "<!--END READMELANG-->"),
                     ("<!--BEGIN READMECONTRIB-->", "<!--END READMECONTRIB-->")]
    lines = list()
    inTag = False
    for line in in_file:
        if not inTag:
            for start, end in break_strings:
                if start in line.strip():
                    line = start
                    inTag = True

            lines.append(line)

        for start, end in break_strings:
            if end in line.strip():
                line = end
                inTag = False
                lines.append(line)

    in_file.close()
    return lines


def get_languages(api_url, add_tags):
    """
    Return a "Languages Used" header and a list of languages used to add to the
    and the number of bits of that language to the README file.
    """
    languages_str = NEWLINE + "<br>" + NEWLINE + "##Languages Used" + NEWLINE + "<br>"
    languages = requests.get(api_url + "/languages").json()

    total_bits = 0
    # Add up total bits for percentages
    for key, value in languages.items():
        total_bits += value

    # Create the unordered list element
    languages_str += NEWLINE + "<ul>"
    for key, value in languages.items():
        language = key
        bits = value
        languages_str += NEWLINE + "<li>" + str(language) + " (" + get_bit_percentage(bits, total_bits) + ")</li>"

    # End the unordered list
    languages_str += NEWLINE + "</ul>"

    # Add the BEGIN/END comment tags
    if add_tags:
        languages_str = NEWLINE + "<!--BEGIN READMELANG-->" + languages_str + NEWLINE + "<!--END READMELANG-->"

    return languages_str


def get_bit_percentage(bits, total_bits):
    """
    Return a formatted percentage of bits out of the total_bits.
    """
    percentage = bits / total_bits * 100.0
    return '{0:.1f}'.format(percentage) + "%"


def get_contributors(api_url, add_tags):
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
        contributors_str += NEWLINE + "<li><a href='https://github.com/" + login + "'>" + login + "</a></li>"

    # End the unordered list
    contributors_str += NEWLINE + "</ul>"

    # Add the BEGIN/END comment tags
    if add_tags:
        contributors_str = NEWLINE + "<!--BEGIN READMECONTRIB-->" + contributors_str + NEWLINE + "<!--END READMECONTRIB-->"

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
        try:
            if contents[x]["name"] != "README.md":          # Skip the readme
                raw_files.append(contents[x].get("download_url"))
        except KeyError:
            print("Call to GitHub API failed.")
            sys.exit(0)

    # FIXME: print(raw_files)
    return raw_files


def find_in_file(file_url, string):
    """
    Find the location of the given string in the given file URL
    and return the line number of the string if found. Returns -1 if the given
    string is not found.
    """
    code = requests.get(file_url).text
    if string in code:
        return code[:code.index(string)].count(NEWLINE) + 1
    else:
        return -1


def make_request(api_url, api_ext, github_username):
    """
    Function to make api calls with or without authentication.
    Returns request object in json form.
    """
    call_url = api_url + api_ext            #call the api with proper ext.
    ret_data = None
    if github_username is not None:
        # Make an authenticated request to the github api using the getpass()
        # function to allow password input via the command line
        ret_data = requests.get(call_url, auth=(github_username, 
                            getpass.getpass())).json()
    else:
        # Backup call for an unauthenticated request.
        ret_data =  requests.get(call_url).json()

    return ret_data



if __name__ == "__main__":
    main()
