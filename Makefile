include .common_makefiles/python_makefile.mk

APP_DIRS=ghtc
TEST_DIRS=tests

.PHONY: pyinstaller
pyinstaller: devvenv
	$(ENTER_VENV) && pyinstaller --add-data ghtc/templates/CHANGELOG.md:ghtc/templates --onefile ghtc/infra/cli.py 
