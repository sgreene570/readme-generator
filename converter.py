"""
converter.py
Convert those silly plain text readmes to markdown easily!
Authors: Stephen Greene and Matt Dwoncyzk
"""


import subprocess
import requests


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

    readmetxt = open("README.md", "r")
    readmemd = open("output.md", "w")
    lines = readmetxt.readlines()
    for x in range (len(lines)):
        if (x + 1 < len(lines) and len(lines[x]) > 2  and lines[x][-2] == ":" 
            and lines[x+1] == "\n"):
            readmemd.write("#" + lines[x] + "<br>")
            x += 1
        else:
            readmemd.write(lines[x] + "<br>")

    repo_url = get_repo_url()
    api_url = get_api_url(repo_url)
    languages = requests.get(api_url + "/languages")
    readmemd.write(str(languages.json()))

    readmemd.flush()
    readmemd.close()
    readmetxt.close()


def get_repo_url():
    # Get the repo origin remote via command line (is there a better way?)
    repo_url = str(subprocess.check_output("git remote get-url origin",
         shell=True))
    repo_url = repo_url[repo_url.index("'") + 1: -3]
    return repo_url


def get_api_url(repo_url):
    api_url = None
    # If the remote is set for SSH keys
    if repo_url[:3] == "git":
        api_url = ("https://api.github.com/repos/" +
            repo_url[repo_url.index(":") + 1: -3])
    # If the remote is set for http/https
    elif repo_url[:4] == "http":
        api_url = ("https://api.github.com/repos/" +
            repo_url[repo_url.index(".com/") + 5:])

    return api_url


if __name__ == "__main__":
    main()
