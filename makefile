##@meta {desc: 'build and deployment for python projects', date: '2024-04-30'}


## Build system
#
#
# type of project
PROJ_TYPE =		python
PROJ_MODULES =		git python-resources python-cli python-doc python-doc-deploy
INFO_TARGETS +=		appinfo


## Project
#
ENTRY = 		./alsum




## Includes
#
include ./zenbuild/main.mk


## Targets
#
.PHONY:			appinfo
appinfo:
			@echo "app-resources-dir: $(RESOURCES_DIR)"


# recreate the micro corpus using adhoc source/summary sentences in a JSON file
.PHONY:			micro
micro:			clean
			$(ENTRY) mkadhoc --override calamr_corpus.name=adhoc
			mkdir -p download
			( cat corpus/micro/amr.txt | bzip2 > download/micro.txt.bz2 )
