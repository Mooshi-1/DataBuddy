# python-pdf
Automated naming, binding, and excel sheet generation for laboratory data.

This program is used by the Miami-Dade Medical Examiner Toxicology Laboratory staff.

The program is split into 3 separate 'MAIN.py' entry-points, in 3 separate folders.
screens:
    find batch data on networked drive by searching batch number
    convert raw pdf instrument data reports into bound and named files by case
    create batch pack with corresponding QC data
quants:
    find batch data on networked drive by searching batch number
    convert raw pdf instrument data reports into bound and named files by case
    create batch pack with corresponing QC data
    generate levey-jennings excel file to assist with QC tracking
    find and fill controlled documents LF-10/LF-11 MSA and TA Worksheets, and Interal Standard Area Response (ISAR)
sequence:
    convert CMS generated 'TEST BATCH REPORT' into instrument-specific sequence
    output sequence as an excel file, csv or xlsx depending on method
    create year/month/date directory in LF-23 INSTRUMENT CHECKLISTS
    copy new sequence, test batch report, and specific LF-23 form into the new directory


The program is built in python 3.12 and packaged into an exe for use by other analysts on a networked drive
The packaged exe is not included in this repo

A number of pylibs are used for different functions throughout the script
    OS - windows filepath and searching manipulation
    sys - for recognizing additional command-line arguments (not part of the user workflow)
    warnings - hide auto-generated warnings created from pandas library
    time - get current date to create folders/filenames
    re - regex string matching to find case-numbers, file-folders, and dilutions
    shutil - used in conjunction with OS for file copy and move
    itertools - for incrementing vial numbers in sequence generation
    pyinstaller - used for packaging the program for use by colleagues without needing python or dependencies installed
    fitz (pymupdf) - opens pdf files, then reads/interprets the data and converts it into a list; 
        also reads annotations in sequence generation
    pyPDFForm - write data into fillable PDFs    
    pandas - convert raw data into dataframes for write into excel
    openpyxl - engine for writing dataframes into excel and manipulating other elements of a workbook
    win32com.client - engine for excel manipulation used specifically for writing into LF-10 and LF-11

TODO list:
screens:
    reinject handling
sequence:
    urine handling
    scion-specific sequences
    reinject creation
    additional statistics related to batch
quants:
    scion init, then work-into quantmain