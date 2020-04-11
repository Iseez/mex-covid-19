#!/bin/bash

OPTIND=1

while getopts ":m:f:" opt; do
    case "$opt" in
    m)
        MODE=$OPTARG
        ;;
    \?)
        echo "Invalid option: -$OPTARG". >&2
        exit 1
        ;;
    :)
        echo "Option -$OPTARG requires an argument, either 'all' or 'update'.">&2
        exit 1
        ;;
    f)
        FOLDER=$OPTARG
        ;;
    esac
done

if [ $# -eq 0 ]
then
    printf "No arguments were given:\n    -m 'all'/'update' is necessary\n    -f folder/path is optional.\n"
    exit 1
fi
if [ $MODE != 'all' ]&&[ $MODE != 'update' ]
then
     echo "Value of argument -m must be either 'all' or 'update'."
     exit 1
 fi
if [ $# -lt 4 ]
then
    FOLDER="$( pwd )"
    echo "Option -f wasn't specified, files will be generated at '$FOLDER'.">&2
elif [ ! -d $FOLDER ]
then
    echo "specified path '$FOLDER' doesn't exist, use a valid path."
fi
SCDIR="$( cd "$( dirname "$0" )" && pwd )"
PYVER="$(python -c 'import sys; print(sys.version_info[:][0])')"
if [ $PYVER -lt 3 ]
then
    if ( type "python3" > /dev/null)
    then
        PY="python3"
    else
        PY="python"
    fi
else
    PY="python"
fi

if [ ! -e $FOLDER"/data" ]
then
    mkdir $FOLDER"/data"
fi
if [ ! -e $FOLDER"/data/pdf" ]
then
    mkdir $FOLDER"/data/pdf"
fi
if [ ! -e $FOLDER"/data/pdf/CTD" ]
then
    mkdir $FOLDER"/data/pdf/CTD"
fi
$PY $SCDIR"/scraping/get-pdfs-ctd.py" $MODE "-f" $FOLDER"/data/pdf/CTD"

if [ ! -e $FOLDER"/data/pdf/cases" ]
then
    mkdir $FOLDER"/data/pdf/cases"
fi
$PY $SCDIR"/scraping/get-pdfs-cases.py" "-f" $FOLDER"/data/pdf/cases"
$PY $SCDIR"/scraping/pdf2csv.py" $MODE "-f" $FOLDER"/data/pdf/cases"
