#!/bin/bash

find /Users/alilimon/Documents/Research/RegulatoryComplexity/001_raw_data/pdf/ -name "*.pdf" | while read file;
do
curl --data-binary @"$file" -H "Content-Type: application/pdf" -L "http://pdfx.cs.man.ac.uk" > "${file}x.xml";
done
