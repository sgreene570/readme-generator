readme-generator:

Convert those boring plain text readmes to github markdown automagically
Usage:

<code>python 3 converter.py</code>
The script will automagically find you README.md and place the completed file in OUTPUT.md.
Currently, it will also put the languages used at the bottom of the readme, along with how many bits were written in that language.
Markdown Linebreaks are inserted wherever a "\n" exists in the text file.
Lines that end with a colon and have a blank padding line below will become markdown headings.
This readme was generated with the script!
Test to see if the find functionality works: _Ideas_
Putting words in underscores tells the script to find the occourence of the word in the repo and return the url to that specific line of code.
