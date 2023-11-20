Name: Soslan Puhaev<br>
E-mail: faceblog22@gmail.com
-----------------------------

Python Spider
Site: thepirate_bay (Torrent site)

What can this spider do?

This spider passes through the site and takes data from there: categories, subcategories, torrent name, torrent link, magnet link, peers, seeds. All data can also be written to MongoDB; when recording, it is checked using a magnet link (it is unique), which helps not to create duplicates in the database.
It can be integrated into a Docker container, attached to your Python project, or used separately.
Command to run: scrapy crawl thepirate_bay
