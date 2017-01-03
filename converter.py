"""
converter.py
Convert those silly plain text readmes to markdown easily!
Authors: Stephen Greene and Matt Dwoncyzk
"""


def main():
    """
    Ideas so far:
    1) new lines == <br>
    2) 2 new lines will make the top line a heading (#)
    3) Somehow figure out which language(s) the repo is using
        Github API or file extensions?
    4) Have segments of written code auto hot link to the actual line in the correct file
        github API for repo link or os.system(git get-url master)....
    """


if __name__ == "__main__":
    main()
