# python-pdf
Automated naming, binding, and excel sheet generation for laboratory data.

This program is used by the Miami-Dade Medical Examiner Toxicology Laboratory staff.

The program is split into 3 separate 'MAIN' entry-points, in 3 separate folders.
screens:
    find batch data on networked drive by searching batch number
    convert raw pdf instrument data reports into bound and named files by case
    create batch pack with corresponding QC data
quants:
    find batch data on networked drive by searching batch number
    convert raw pdf instrument data reports into bound and named files by case
    create batch pack with corresponing QC data
    generate levey-jennings excel file to assist with QC tracking
    find and fill controlled documents LF-10, LF-11, and Interal Standard Area Response (ISAR)
sequence:
    convert CMS generated 'TEST BATCH REPORT' into instrument-specific sequence
    output sequence as an excel file, csv or xlsx depending on method
    create year/month/date directory in LF-23 INSTRUMENT CHECKLISTS
    copy new sequence, test batch report, and specific LF-23 form into the new directory


