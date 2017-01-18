# readme-generator:


<br>
Convert those boring plain text readmes to github markdown automagically
<br>
# Usage:


<br>
<code>python3 converter.py</code> (within a github repo's directory)
<br>
The script will automagically find you README.md and place the completed file in OUTPUT.md.
<br>
Currently, it will also put the languages used at the bottom of the readme, along with how many bits were written in that language.
<br>
Markdown Linebreaks are inserted wherever a "\n" exists in the text file.
<br>
Lines that end with a colon and have a blank padding line below will become markdown headings.
<br>
This readme was generated with the script!
<br>
Test to see if the find functionality works:<a href=https://github.com/sgreene570/readme-generator/blob/master/converter.py#L15>Ideas</a>
<br>
Putting words in underscores tells the script to find the occourence of the word in the repo and return the url to that specific line of code.
<br>
{'Python': 3543}
