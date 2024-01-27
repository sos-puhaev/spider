E-mail: faceblog22@gmail.com
Telegram: @JonniLoka
-----------------------------

Python Spider<br>
Site: thepirate_bay (Torrent site)<br>
<br>
What can this spider do?<br>

This spider passes through the site and takes data from there: categories, subcategories, torrent name, torrent link, magnet link, peers, seeds. All data can also be written to <b>MongoDB</b> when recording, it is checked using a magnet link (it is unique), which helps not to create duplicates in the database.<br>
It can be integrated into a Docker container, attached to your Python project, or used separately.<br>
Command to run: <b>scrapy crawl thepirate_bay</b>
