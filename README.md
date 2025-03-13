# Laboratory Data Automation

Automated naming, binding, data handling, sheet generation, and more for laboratory pdf data.

This program is used by the Miami-Dade Medical Examiner Toxicology Laboratory staff.

## Program Structure
A GUI written with tkinter is launched from main.py. The DataBuddy.bat file can be launched if a python interpreter is not installed on your computer. The necessary dependencies are located in the .venv folder, and automatically called when using the program.
Within the GUI, there are notebook tabs corresponding to different scripts, which are launched as a separate thread when pressing the "RUN" button.


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

### Z Carryover
- Check AMDIS reports for carryover
- Create summary sheet of AMDIS results
- Prepare new sequence based on carryover results

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
### Overall
- track total number of times used, usage statistics, etc

### Aux/Searcher algorithms
- refactor shuttle/shuttlehome, sometimes they don't work properly... move QC to batch pack data, etc

### Screens
- Reinject handling
- SCRNZ - new report, addition of unknown spectra

### Z carryover
- expand 2 instrument run, with 1 doing bases and 1 doing acids, with additional functionality
- automate transfer of results from 1 computer to another and transfer to TA-DATA directory on G-drive
- then bring batch from G drive to local computer for processing

### Sequence
- method dictionary for LF-23 creation not using .startswith() properly
- Handle multiple quants gracefully, while not impacting multiple screen batches
- Urine handling
- Scion-specific sequences
- Reinject creation
- Additional statistics related to batch

### Quants
- SQVOL reinject aggregator
- some sort of recognition of undiluted MSA's (Gx0) and other non-routine tissue specimens
- Scion init, then work into QuantMain
