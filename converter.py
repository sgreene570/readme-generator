"""
converter.py
Convert those silly plain text readmes to markdown easily!
Authors: Stephen Greene
"""


import subprocess
import requests
import json


# Important strings
NEWLINE = "\n"
NEWLINE_MD = "<br>"
HEADING_MD = "#"
INPUT_FILE = "README.md"
OUTPUT_FILE = "OUTPUT.md"
# Character used to enclose code segments where href tags should be inserted
LINK_CHAR = "_"     


def main():
    repo_url = get_repo_url()
    api_url = get_api_url(repo_url)
    repo_contents = requests.get(api_url + "/contents")
    raw_files = get_raw_files(repo_contents)    # List of available files

    readmetxt = open(INPUT_FILE, "r")
    readmemd = open(OUTPUT_FILE, "w")
    lines = readmetxt.readlines()

    for x in range (len(lines)):
        line = lines[x]     # create a copy of the current line
        for y in range(len(line)):      #Iterate over each char
            # Check if a line has LINK_CHARs to denote url zone
            if line[y]  == LINK_CHAR and line[y+1:].count(LINK_CHAR) % 2 == 1:
                find_string = line[y+1:line[y+1:].index(LINK_CHAR) + y+1]
                print(find_string)
                for file_url in raw_files:
                    line_number = find_in_file(file_url, find_string)
                    if line_number is not None:
                        print(line_number)
                        # Insert the href link to the correct line number
                        lines[x] = (line[:y-1] + "<a href=" +
                            repo_contents.json()[raw_files.index(file_url) + 1]
                            ["html_url"] + "#L" + str(line_number) + ">" +
                            line[y+1:y+len(find_string)+1] + "</a>" +
                            line[y+len(find_string)+2:])
                        break

        line = lines[x]     # update the copied line
        # If line is a heading
        if (x+1 < len(lines) and len(line) > 2  and line[-2] == ":"
            and lines[x+1] == NEWLINE):
            readmemd.write(HEADING_MD + line)
            x += 1
        else:
            readmemd.write(line + NEWLINE_MD)
        # Insert a normal new line for viewing the markdown file in a text editor
        readmemd.write(NEWLINE)

    # Add repo language info at the bottom
    languages = requests.get(api_url + "/languages")
    readmemd.write(str(languages.json()))

    # Wrap up file IO
    readmemd.flush()
    readmemd.close()
    readmetxt.close()


def get_repo_url():
    # Get the repo origin remote url via command line (is there a better way?)
    repo_url = str(subprocess.check_output("git remote get-url origin",
        shell=True))
    repo_url = repo_url[repo_url.index("'") + 1: -3]
    return repo_url


def get_api_url(repo_url):
    api_url = None
    # If the remote url is set for SSH keys
    if repo_url[:3] == "git":
        api_url = ("https://api.github.com/repos/" +
            repo_url[repo_url.index(":") + 1: -3])
    # If the remote url is set for http/https
    elif repo_url[:4] == "http":
        api_url = ("https://api.github.com/repos/" +
            repo_url[repo_url.index(".com/") + 5:])

    return api_url


def get_raw_files(repo_contents):
    # scrape the repo_contents response object for all of the names of the
    # available files in the repo and return them in a list.
    contents = repo_contents.json()
    raw_files = list()
    for x in range(len(contents)):
        if contents[x]["name"] != "README.md":          # Skip the readme
            raw_files.append(contents[x].get("download_url"))

    print(raw_files)
    return(raw_files)


def find_in_file(file_url, string):
    # find the location of the given string in the given file url
    # returns the line number of the string if found
    code = requests.get(file_url).text
    if string in code:
        return code[:code.index(string)].count(NEWLINE) + 1


if __name__ == "__main__":
    main()
