# biblio_mapper
A pipeline for capturing citation data from publications and mapping cross-referencing. Effective for MLA/APA and Vancouver/Harvard. Chicago and IEEE TBC.


pdf_crusher.py -> uses pdfminer to capture text from all .pdf files in directory. Outputs captured text in .txt

ref_capture.py -> processes .txt files to extract citation data, outputs scraped citations in .csv

ann_train.py -> trains a basic artificial neural network to classify citation strings from non-citation strings, outputs ANN parameters in .csv

build_network.py -> loads ANN parameters and scraped citations, classifies citations, outputs master node table in .csv

output_graphics.py -> loads master table, filters and sorts for significance, outputs filtered data in .csv and .json

index.html -> loads .json and builds force-directed node graph [TBC]

build_svg.py -> loads filtered data and outputs custom .svg
