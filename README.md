# Laboratory Data Automation

Automated naming, binding, and Excel sheet generation for laboratory data.

This program is used by the Miami-Dade Medical Examiner Toxicology Laboratory staff.

## Program Structure
The program is split into 3 separate `MAIN.py` entry-points, in 3 separate folders:

### Screens
- Find batch data on networked drive by searching batch number
- Convert raw PDF instrument data reports into bound and named files by case
- Create batch pack with corresponding QC data

### Quants
- Find batch data on networked drive by searching batch number
- Convert raw PDF instrument data reports into bound and named files by case
- Create batch pack with corresponding QC data
- Generate Levey-Jennings Excel file to assist with QC tracking
- Find and fill controlled documents LF-10/LF-11 MSA and TA Worksheets, and Internal Standard Area Response (ISAR)

### Sequence
- Convert CMS generated 'TEST BATCH REPORT' into instrument-specific sequence
- Output sequence as an Excel file, CSV or XLSX depending on method
- Create year/month/date directory in LF-23 INSTRUMENT CHECKLISTS
- Copy new sequence, test batch report, and specific LF-23 form into the new directory

## Technical Details
The program is built in Python 3.12 and packaged into an executable (EXE) for use by other analysts on a networked drive. The packaged EXE is not included in this repository.

## Python Libraries Used
A number of Python libraries are used for different functions throughout the script:
- **os**: Windows filepath and searching manipulation
- **sys**: Recognizing additional command-line arguments (not part of the user workflow)
- **warnings**: Hide auto-generated warnings created from the pandas library
- **time**: Get current date to create folders/filenames
- **re**: Regex string matching to find case-numbers, file-folders, and dilutions
- **shutil**: Used in conjunction with os for file copy and move
- **itertools**: For incrementing vial numbers in sequence generation
- **pyinstaller**: Used for packaging the program for use by colleagues without needing Python or dependencies installed
- **fitz (PyMuPDF)**: Opens PDF files, reads/interprets the data, and converts it into a list; also reads annotations in sequence generation
- **pyPDFForm**: Write data into fillable PDFs
- **pandas**: Convert raw data into DataFrames for writing into Excel
- **openpyxl**: Engine for writing DataFrames into Excel and manipulating other elements of a workbook
- **win32com.client**: Engine for Excel manipulation used specifically for writing into LF-10 and LF-11

## TODO List
### Screens
- Reinject handling

### Sequence
- Urine handling
- Scion-specific sequences
- Reinject creation
- Additional statistics related to batch

### Quants
- Scion init, then work into QuantMain
