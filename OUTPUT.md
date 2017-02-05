#readme-generator
<br>

<br>

<br>
<br>
<br>
Convert those boring plain text readmes to GitHub markdown automagically.
<br>
<br>
<br>
##Usage
<br>
<br>
<br>
Run <code>python3 converter.py</code> (within a GitHub repository's directory),
<br>
and the script will automagically find your README.md and place the completed
<br>
file in OUTPUT.md.
<br>
<br>
<br>
It also puts the languages used at the bottom of the README.md file, along with
<br>
how many bits were written in that language.
<br>
<br>
<br>
Markdown Linebreaks are inserted wherever a "\n" exists in the text file.
<br>
<br>
<br>
Lines that end with a colon and have a blank padding line below will become markdown headings.
<br>
<br>
<br>
This readme was generated with the script!
<br>
<br>
<br>
Test to see if the find functionality works:<a href=https://github.com/sgreene570/readme-generator/blob/master/converter.py#L25>api</a>
<br>
<br>
<br>
Putting words in underscores tells the script to find the occurrence of the word
<br>
in the repository and return the URL to that specific line of code.
<br>
<br>
<br>
{'Python': 3882}
<br>
