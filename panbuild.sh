#pandoc --toc -s -N -V fontsize=12pt -V geometry:margin=1in --filter pandoc-citeproc --biblio bericht.bib --csl chicago-author-date.csl --include-in-header titlesec.tex -o bericht_hodel_remus.pdf bericht_hodel_remus.md

pandoc --filter pandoc-citeproc --toc -s -N -V fontsize=12pt -V geometry:margin=1in bericht_hodel_remus.md --biblio bericht.bib --include-in-header titlesec.tex --csl springer-lecture-notes-in-computer-science_modified.csl -o bericht_hodel_remus.pdf