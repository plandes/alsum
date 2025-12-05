##@meta {desc: 'build and deployment for python projects', date: '2024-04-30'}


## Build system
#
#
# type of project
PROJ_TYPE =		python
PROJ_MODULES =		python/doc python/package python/deploy
PY_TEST_PRE_TARGETS +=	$(MICRO_CORP_FILE)
ADD_CLEAN_ALL += 	data download corpus/micro/amr.txt


## Project
#
MICRO_CORP_FILE ?=	download/micro.txt.bz2


## Includes
#
include ./zenbuild/main.mk


## Targets
#
# recreate the micro corpus using adhoc source/summary sentences in a JSON file
$(MICRO_CORP_FILE):
			@mkdir -p corpus/amr-rel
			$(eval outfile := download/micro.txt.bz2)
			@$(MAKE) pyharn ARG="mkadhoc"
			@mkdir -p download
			@( cat corpus/micro/amr.txt | bzip2 > $(MICRO_CORP_FILE) )
			@$(call loginfo,created $(MICRO_CORP_FILE))
.PHONY:			micro
micro:			$(MICRO_CORP_FILE)
