#!/bin/bash

BASEDIR=$1

###### MAKE BIAS #####
echo `date` "Stage 1. BIAS"
echo `date` "Convert RAW to FITS"

cd $BASEDIR/bias/raw
for A in *.CR2; do echo $A; rawtran -A "-t 0" -c Gi -o ${A%CR2}fits $A; done
mv *.fits ../fits

echo `date` "Make bias from fits"
cd ../fits
munipack bias -o master_bias.Gi.fits IMG_*.fits
mv master_bias.Gi.fits $BASEDIR


###### MAKE DARK #####
echo `date` "Stage 2. DARK"
echo `date` "Convert RAW to FITS"

cd $BASEDIR/dark/raw
for A in *.CR2; do echo $A; rawtran -A "-t 0" -c Gi -o ${A%CR2}fits $A; done
mv *.fits ../fits

echo `date` "Make dark from fits"
cd ../fits
munipack dark -o master_dark.Gi.fits IMG_*.fits
mv master_dark.Gi.fits $BASEDIR


###### MAKE FLAT #####
echo `date` "Stage 2. FLAT"
echo `date` "Convert RAW to FITS"

cd $BASEDIR/flat/raw
for A in *.CR2; do echo $A; rawtran -A "-t 0" -c Gi -o ${A%CR2}fits $A; done
mv *.fits ../fits

echo `date` "Make flat from fits"
cd ../fits
munipack flat -o master_flat.Gi.dark.fits -gain 1 -dark ../../master_dark.Gi.fits IMG_*.fits
mv master_flat.Gi.dark.fits $BASEDIR
