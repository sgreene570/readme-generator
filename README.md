#readme-generator
<br>
Convert those boring plain text readmes to GitHub markdown automagically.
<br>
##Usage
<br>
First, to install any dependencies, simply type the following:
<br>
<code>pip install -r requirements.txt</code>
<br>
Then, run <code>python converter.py</code> (within a GitHub repository's directory),
<br>
and the script will automagically find your README.md and place the completed
<br>
file in OUTPUT.md.
<br>
Use the <code>-l</code> argument to include a list of languages used in the
<br>
README.md file, along with how many bits were written in that language.
<br>
Use the <code>-c</code> argument to include a list of repository contributors
<br>
in the README.md file.
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
<br>
in the repository and return the URL to that specific line of code.
<br>
##Languages Used
<br>
<ul>
<li>Python (6570 bits)</li>
</ul>
<br>
##Contributors
<br>
<ul>
<li><a href='https://api.github.com/users/sgreene570'>sgreene570</a></li>
</ul>
