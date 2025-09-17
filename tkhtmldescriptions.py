
HTML_WRAPPER_STYLE = (
    "font-size:10px; color:#f8f9fa; background-color:#2c2c54; "
    "padding:10px; border-radius:6px; font-family:Segoe UI, sans-serif;"
)

HEADER_STYLE = "color:#33d9b2;" ##33d9b2  ##2ecc71
LINK_STYLE = "color: #ffb142; text-decoration: underline;" #cd6133 #227093
NOTE_STYLE = "color:#adb5bd;"
LIST_STYLE = "margin-left:15px;"

def wrap_html(content: str) -> str:
    return f'<div style="{HTML_WRAPPER_STYLE}">{content}</div>'

def styled_header(text: str) -> str:
    return f'<h5 style="{HEADER_STYLE}">{text}</h5>'

def styled_link(url: str, label: str) -> str:
    return f'<a href="{url}" style="{LINK_STYLE}">{label}</a>'

def styled_note(text: str) -> str:
    return f'<span style="{NOTE_STYLE}">{text}</span>'

def styled_list(items: list[str]) -> str:
    list_items = ''.join(f'<li>{item}</li>' for item in items)
    return f'<ul style="{LIST_STYLE}">{list_items}</ul>'

sequence_description_3 = wrap_html(
    styled_header("Quick Links:") +
    styled_list([
        f'{styled_link("file:///G:/LABORATORY%20OPERATIONS/06%20-%20LABORATORY%20FORMS/LF-23%20INSTRUMENT%20CHECKLISTS", "Instrument Checklist Directory")}',
        f'{styled_link("file:///G:/PDF%20DATA/TEST%20BATCH%20REPORTS", "Test Batch Reports Directory")}',
        f'{styled_link("file:///G:/LABORATORY OPERATIONS/07%20-%20TESTING PROCEDURES", "Testing Procedure Directory")}',
    ]) +
    styled_header("Requirements:") +
    styled_list([
        f'This script looks in the directory {styled_link("file:///G:/PDF%20DATA/TEST%20BATCH%20REPORTS", "Test Batch Reports")} for PDF-printed Test Batches',
        "You can make extra directories, <em>'Archive'</em>, <em>'Old batches'</em>, etc., without issue",
        "Getting an error? Make sure that the only PDF files in your directory are Test Batches"
    ]) +
    styled_header("Full Instructions:") +
    styled_link("https://mdcme.qualtraxcloud.com/Default.aspx?ID=3883", "Sequence Generator Procedure") + "<br>" +
    styled_note('This will open the IQM document in your default browser.')
)

screens_description = wrap_html(
    styled_header("Quick Links: ") +
    styled_list([
        f'{styled_link("file:///G:/PDF DATA", "PDF Data Directory")}',
        f'{styled_link("file:///G:/LABORATORY OPERATIONS/07 - TESTING PROCEDURES", "Testing Procedure Directory")}',
        f'{styled_link("https://mdcme.qualtraxcloud.com/Workflow/Instance.aspx?defid=2043", "IQM Test Batch Review Workflow")}',
    ]) +
    styled_header("Requirements: ") +
    styled_list([
        "Data must be in BATCH PACK DATA, CASE DATA, or auto-generated CASE DATA subfolders",
        "Data that is not in the directories listed above will be ignored by the script",]) + "<br>" +
    styled_list([
        "Close the file explorer preview window and any open PDF files",
        "Manually bind reinjects manually before or after running the script",
        "Manually bind sequence to batch pack after running the script"
    ])
)

quants_description = wrap_html(
    styled_header("Quick Links: ") +
    styled_list([
        f'{styled_link("file:///G:/PDF DATA", "PDF Data Directory")}',
        f'{styled_link("file:///G:/LABORATORY OPERATIONS/07 - TESTING PROCEDURES", "Testing Procedure Directory")}',
        f'{styled_link("https://mdcme.qualtraxcloud.com/Workflow/Instance.aspx?defid=2043", "IQM Test Batch Review Workflow")}',
    ]) +
    styled_header("Requirements: ") +
    styled_list([
        "Data must be in BATCH PACK DATA, CASE DATA, or auto-generated CASE DATA subfolders",
        "Data that is not in the directories listed above will be ignored by the script",
        "Close the file explorer preview window and any open PDF files",]) 
    + "<br>" +
    styled_list([
        "If you have MSA's, Excel must be closed on your computer to fill the LF-10/LF-11 forms",
    ])
)

Z_description = wrap_html(
    styled_header("Quick Links: ") + 
    styled_list([
        f'Full Procedure: {styled_link("https://mdcme.qualtraxcloud.com/Default.aspx?ID=3923", "SCRNZ Data Guide")}',
        f'{styled_link("file:///G:/TA-DATA", "Tox-Analyzer Raw Data Directory")}'
    ]) +
    styled_header("Requirements: ") +
    styled_note(f"See the full procedure for detailed information on how to use this tab (Section 1.3 - 9)") +
    styled_list([
        "Your files must be processed by AMDIS before starting the Printer",
        "The computer that runs the Printer script will be unusable for up to 1 hour",])
    + "<br>" +
    styled_list([
        "The network path must only contain AMDIS files",
        "The printed order must match the sequence order",
        "Do not rename AMDIS files after being printed until the Carryover Check is complete",
    ])
)