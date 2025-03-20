# add test suite

# openpyxl==3.1.5
# pandas==2.2.3
# PyAutoGUI==0.9.54
# PyGetWindow==0.0.9
# PyMsgBox==1.0.9
# PyMuPDF==1.25.3
# pynput==1.7.7
# pypdf==5.1.0
# PyPDF2==3.0.1
# PyPDFForm==1.5.1
# python-dateutil==2.9.0.post0
# pywin32==308
# XlsxWriter==3.2.1


# logging_config.py
import logging

# Configure the logging
logging.basicConfig(
    filename="log.log",
    format="%(asctime)s-%(name)s-%(levelname)s:%(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    encoding="utf-8",
    level=logging.DEBUG,
)
