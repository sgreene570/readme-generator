#readme-generator


<br>
Convert those boring plain text readmes to GitHub markdown automagically.
<br>
##Usage
<br>
Run <code>python3 converter.py</code> (within a GitHub repository's directory),
and the script will automagically find your README.md and place the completed
file in OUTPUT.md.
<br>
It also puts the languages used at the bottom of the README.md file, along with
how many bits were written in that language.
<br>
Markdown Linebreaks are inserted wherever a "\n" exists in the text file.
<br>
Lines that end with a colon and have a blank padding line below will become markdown headings.
<br>
This readme was generated with the script!
<br>
Test to see if the find functionality works:<a href=https://github.com/sgreene570/readme-generator/blob/master/converter.py#L25>api</a>
<br>
Putting words in underscores tells the script to find the occurrence of the word
in the repository and return the URL to that specific line of code.
<br>
{'Python': 3882}
