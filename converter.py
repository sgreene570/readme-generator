"""
converter.py
Convert those silly plain text readmes to markdown easily!
Authors: Stephen Greene
"""


import subprocess
import requests
import json


def main():
    """
    Ideas so far:
    1) new lines == <br>
    2) 2 new lines will make the top line a heading (#)
    3) Somehow figure out which language(s) the repo is using
        Github API or file extensions?
    4) Have segments of written code auto hot link to the actual line in repo
        github API for repo link or os.system(git get-url master)....
    """

    repo_url = get_repo_url()
    api_url = get_api_url(repo_url)
    repo_contents = requests.get(api_url + "/contents")
    raw_files = get_raw_files(repo_contents)

    readmetxt = open("README.md", "r")
    readmemd = open("output.md", "w")
    lines = readmetxt.readlines()
    for x in range (len(lines)):
        line = lines[x]
        for y in range(len(line)):
            if line[y]  == "_" and line[y+1:].count("_") % 2 == 1:
                find_string = line[y+1:line[y+1:].index("_") + y+1]
                print(find_string)
                for file_url in raw_files:
                    line_number = find_in_file(file_url, find_string)
                    if line_number is not None:
                        print(line_number)
                        lines[x] = (line[:y-1] + "<a href=" + 
                            repo_contents.json()[raw_files.index(file_url) + 1]
                            ["html_url"] + "#L" + str(line_number) + ">" +
                            line[y+1:y+len(find_string)+1] + "</a>" + 
                            line[y+len(find_string)+2:])
                        break

        line = lines[x]     # update the pointer
        if (x+1 < len(lines) and len(line) > 2  and line[-2] == ":"
            and lines[x+1] == "\n"):
            readmemd.write("# " + line)
            x += 1
        else:
            readmemd.write(line + "<br>")
        readmemd.write("\n")

    languages = requests.get(api_url + "/languages")
    readmemd.write(str(languages.json()))

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
        if contents[x]["name"] != "README.md":
            raw_files.append(contents[x].get("download_url"))

    print(raw_files)
    return(raw_files)


def find_in_file(file_url, string):
    # find the location of the given string in the given file url
    # returns the line number of the string if found
    code = requests.get(file_url).text
    if string in code:
        return code[:code.index(string)].count("\n") + 1


if __name__ == "__main__":
    main()
