# Overviews

This directory contains three files:

- `generateOverviews.py` - a Python script used to generate an overview for each MARC 21 field in `LWL_export.xml` with statistics about usage and frequency ordered lists of 1-8grams. (local name is analyseXML2.py). NB this code is not properly commented (yet).
- `overviewsPart1.txt` - for each MARC 21 field in `LWL_export.xml` this file gives its frequency, its average “word” count, and a sample of up to 20 examples. The fields are ordered by their frequency. (local name is XML_analysis2.txt)
- `overviewsPart2.zip` - a compressed folder that contains a folder for each of the 90 MARC 21 fields used in `LWL_export.xml`, each of which contains eight frequency ordered lists of 1-grams to 8-grams. (local name of folder is /allNgrams), 48MB.
