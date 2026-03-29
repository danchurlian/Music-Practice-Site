# Music Practice Site
This is a web application that I began working on during January 2026 in my winter break.

Before I began my project on this website, I had to find a way to render music on a web page. I actually made a test workspace to experiment before I transferred my work on this website. 

## Researching Music Notation Generation 
From my research on programming and music, I realized I had to learn about MusicXML, an XML language that conveys information about a piece of music, such as note letters, their durations, their octave, and much more. A single XML file is sufficient to contain all the information of single piece of music. Although such files can get increasingly huge for larger pieces of music, I believed MusicXML still holds merit for my purposes.

I then had to figure out how to render MusicXML information onto the webpage. For that I settled on Verovio, an open-source library that generates svg (scalable vector graphic) images of music notes, a general process called music engraving. This library accepts MusicXML as input, which was perfect for my project.

## Website Development Process
After getting familiar with it, I began building the website. The first type problem I worked on was the scales web page, where a user can analyze a randomly generated scale and identify what type of scale it is. I found the logic to be challenging to think about because I had to account for accidentals.

The second type problem were the chrods and I faced similar challenges.

Afterwards was the key signature problem, which was easier to implement than placing the scales. This was because in MusicXML, the key of a single piece can be dictated by a single number, which is something that I use the Python random library to generate.

The last two problems were the most challenging to implement for me. Those were the pitch audio problems. This was because I had to use Javascript in order to respond to the listen buttons and to play audio to the end user. At the same time it required me to learn about the web audio API, which is something I still have yet to have a clear understanding of. 

Working on the front-end, I learned more about the flexbox model which I mainly used for centering HTML elements. More generally speaking, I gained a lot of practice with CSS fundamentals such as understanding the differences between margin and padding, CSS selectors, CSS variables, and more. I'm glad I'm taking the time to learn how to use raw CSS first before I learn the basics of front-end frameworks such as React.

## Notable Things and Concerns 
Most random generation if not all comes from the backend using Flask. What I believe is more concerning is the use of global variables in app.py that stores the current answers of the questions of all the web pages. This could be a problem when more than one person is on the web page at the same time, which can lead to incorrect user evaluation and possible "undefined behavior". This concern I don't know how serious it really is.

## Contact:
Email: chudaniel400@gmail.com
LinkedIn: https://www.linkedin.com/in/daniel-chu-13a107387/