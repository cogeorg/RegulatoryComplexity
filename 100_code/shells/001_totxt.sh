#!/bin/bash
FILES=~001_raw_data/pdf/*.pdf
for f in $FILES
do
 echo "Processing $f file..."
 pdftotext -enc UTF-8 $f
done
