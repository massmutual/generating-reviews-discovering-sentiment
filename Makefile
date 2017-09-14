# the dependencies of .PHONY will always be run as targets (never "up to date")
# see https://www.gnu.org/software/make/manual/html_node/Special-Targets.html
.PHONY: clean data lint requirements

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROFILE = default
PROJECT_NAME = 05-channel-routing
PYTHON_VENV=pyenv
PYTHON_INTERPRETER = $(PYTHON_VENV)/bin/python

NOCAT_PARTIAL_PATH = NOCAT_GALI-RMM-TERMDTC
CAT_PARTIAL_PATH = GALI-RMM-TERMDTC
ACXIOM_VALUE_MAP_JSON := src/data/acxiom_value_map.json

# this file exports the passwords needed for each database
include ./config.mk

#################################################################################
# COMMANDS                                                                      #
#################################################################################



#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

$(ACXIOM_VALUE_MAP_JSON):
	wget "https://raw.githubusercontent.com/massmutual/acxiom_features/master/acxiom_features/acxiom_metadata_output/features_map_2017_q1_short.json?token=AC33CTDtWDjGo414qaHFjF5TudTdu3Zvks5ZwWOCwA%3D%3D" -O $@

data/raw/$(NOCAT_PARTIAL_PATH)_RAW: src/data/pull_dataset.py src/data/acxiom_value_map.json
	@echo "Getting the full dataset...fresh from vertica"
	$(PYTHON_INTERPRETER) $< --categorical False --overwrite True --valuemap src/data/acxiom_value_map.json --output_data $@
