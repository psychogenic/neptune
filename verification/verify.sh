#!/bin/bash

CURSCRIPT=$0
MODULEFILEPATH=$1

PYTHONEXE=python3
SBYCONFIG_TPL=basicverify_tpl.sby

if [ "x$MODULEFILEPATH" = "x" ]
then
	echo "Usage: $0 PATH_TO_MODULE"
	exit 1
fi

if [ -f $MODULEFILE ]
then
	echo "Verifying $MODULEFILEPATH"
else
	echo "Can't find $MODULEFILEPATH"
	exit 2
fi

OUTDIR=$(dirname $CURSCRIPT)
MODFILE=$(basename $MODULEFILEPATH)
MODULEBASE=${MODFILE/.py/}
OUT_IL_FNAME="$MODULEBASE.il"
OUT_IL_PATH="$OUTDIR/$OUT_IL_FNAME"
OUT_SBY_CONFIG="$OUTDIR/$MODULEBASE.sby"

if [ -f $OUT_SBY_CONFIG ]
then
	echo "sby config exists for $MODULEBASE"
else
	echo "generating sby config for $MODULEBASE"
	cat "$OUTDIR/$SBYCONFIG_TPL" | sed -e "s|ILFILENAME|$OUT_IL_FNAME|g" > $OUT_SBY_CONFIG
	#echo $OUT_IL >> $OUT_SBY_CONFIG
fi

echo "$PYTHONEXE $MODULEFILEPATH generate -t il > $OUT_IL_PATH"
$PYTHONEXE $MODULEFILEPATH generate -t il > $OUT_IL_PATH
sby -f $OUT_SBY_CONFIG
