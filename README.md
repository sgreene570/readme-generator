#readme-generator [![Build Status](https://travis-ci.org/sgreene570/readme-generator.svg?branch=master)](https://travis-ci.org/sgreene570/readme-generator)
Convert those boring plain text readmes to GitHub markdown automagically.
##Usage
Install the dependencies by typing the following: `pip install -r requirements.txt`. Then, run `python converter.py` (within a GitHub repository's directory), and the script will automagically find your README.md and place the converted file in OUTPUT.md.
###Arguments
| Argument | Function                                                                                                                              |
|----------|---------------------------------------------------------------------------------------------------------------------------------------|
| -l       | Add language information to the README. Added to the end of the file (before contributor data if applicable) unless "BEGIN READMELANG" and "END READMELANG" comment tags are present. |
| -c       | Add contributor information to the README. Added to the end of the file unless "BEGIN READMECONTRIB" and "END READMECONTRIB" comment tags are present.                                    |
| -f       | Fast-forward and do not confirm README.md overwrite. A backup is still made in README.backup.                                         |
- Markdown linebreaks are inserted wherever a "\n" exists in the text file.
- Lines that end with a colon and have a blank padding line below will become markdown headings.
This readme was generated with the script!
It also has a code find functionality: [api](https://github.com/sgreene570/readme-generator/blob/master/converter.py#L25). Putting words in underscores tells the script to find the occurrence of the word in the repository and return the URL to that specific line of code.

<!--BEGIN READMELANG-->
##Languages Used
- Python (100.0%)
<!--END READMELANG-->

<!--BEGIN READMECONTRIB-->
##Contributors
- [sgreene570](https://github.com/sgreene570)
- [mattgd](https://github.com/mattgd)
<!--END READMECONTRIB-->
