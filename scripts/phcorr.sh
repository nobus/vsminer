#!/bin/bash

PHCORR=$1
BASEDIR=$2

MASTER_BIAS=$PHCORR/master_bias.Gi.fits
MASTER_DARK=$PHCORR/master_dark.Gi.fits
MASTER_FLAT=$PHCORR/master_flat.Gi.dark.fits

: '
http://munipack.physics.muni.cz/phcorrtut.html
'

cd $BASEDIR

mkdir fits
touch fits/url.txt

echo "CONVERT"
for FILE in `ls *.CR2`; do
    echo $FILE
    rawtran -A "-t 0" -c Gi -o fits/${FILE%CR2}Gi.fits $FILE
done

echo "PHCORR"
cd fits

for FILE in `ls *.fits`; do
    echo $FILE
    munipack phcorr -dark $MASTER_DARK -bias $MASTER_BIAS -flat $MASTER_FLAT -gain 1 $BASEDIR/fits/$FILE
done

for FILE in `ls $BASEDIR/fits/*.fits~`; do
    mv $FILE ${FILE%fits~}phcorr.fits
    echo ${FILE%fits~}phcorr.fits >> url.txt
    echo >> url.txt
done
