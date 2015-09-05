#!/bin/bash

NOSEBIN="env/bin/nosetests"
if [ ! -f "$NOSEBIN" ]; then
    NOSEBIN=nosetests
fi

$NOSEBIN -v tests --rednose --with-cover --cover-package=tap/ --cover-erase
