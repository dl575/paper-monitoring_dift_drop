# Add a list of home-made PDF figures here.
PDFFIGURES=figs/*.pdf

.SUFFIXES: .fig .eps .ps .dvi .bbl .bib .tex .pdf

FIGURES=${wildcard *.fig}
TEXFILES=*.tex tabs/*.tex
BIBFILES=*.bib

all: pdf   

force: rmdone all

dvi: paper.dvi

xdvi: paper.dvi
	xdvi paper.dvi

gv: paper.ps
	gv paper.ps

ps: paper.ps 

pdf: paper.pdf

rmdone:
	rm -f done.flag

done.flag:
	touch done.flag

printerrors:
	@echo "*****************************"; \
	echo Overview of typeset warnings: ; \
        echo "****************************"; \
	grep "Underfull" paper.log; \
	grep "Overfull" paper.log; \
	echo ; \
        echo "***************************"; \
	echo Overview of latex warnings: ; \
        echo "***************************"; \
	grep "LaTeX Warning" paper.log; \
        echo "***************************"; \
	echo ; \
        echo "***************************"; \
	echo Overview of bibtex warnings: ; \
        echo "***************************"; \
        grep ^Warning-- paper.blg; \
	echo "***************************"; \
	echo ; \
        echo "*************************"; \
	echo Overview of latex errors: ; \
        echo "*************************"; \
	grep "^!" paper.log; \
        echo "*************************"; \
	echo

paper.bbl: $(BIBFILES) $(TEXFILES) Makefile done.flag
	pdflatex -interaction=batchmode paper.tex || true
	rm -f $*.pdf
	bibtex -terse $*

paper.pdf: $(TEXFILES) $(PDFFIGFILES) paper.bbl Makefile done.flag
	@echo Running latex once.; \
	while ( pdflatex -interaction=nonstopmode paper.tex; grep "Rerun to get cross" paper.log ) ; do \
          echo; \
          echo "*********************************"; \
          echo "*********************************"; \
          echo Reruning to complete compilation.; \
          echo "*********************************"; \
          echo "*********************************"; \
	done; \
        echo "***************************"; \
	echo DVI file generated.; \
        echo "***************************"; \
	echo ; \
	make printerrors 
			
clean:
	rm -f *.lof *.lot *.pfg *~ *.aux *.dvi *.blg *.log *.bbl *.bak paper.ps paper.pdf *.toc *.swp done.flag paper.out


