#attempting to plug sqvol init into quantmain....

import fitz  # type: ignore # PyMuPDF
import os

from aux_func import table_converter
from sample_sorter import QCTYPE, Sample

def sqvol_init(batch_dir):
    samples = [] #will hold sample objects created here
    curves = {}
    curve_count = 0
    # Iterate through directory defined by filepath
    for filename in os.listdir(batch_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(batch_dir, filename)        
            doc = fitz.open(pdf_path)
            # Extract text from the first page
            page = doc[0]
            text = page.get_text().strip()
            #print(text)
            lines = text.split('\n')
            #print(lines)
            case_number = None
            #init curves count to handle multiple curves
            #print(lines)

            try:
                #take care of special cases
                if " 0:Unknown " in lines:
                    Sequence = Sample("Sequence", pdf_path, "sequence", {QCTYPE.SEQ}, None, None)
                    print("found sequence")
                    samples.append(Sequence)
                    doc.close()
                    continue
                if "Calibration Curve Report" in lines:
                    tuples_list = []
                    #get LJ info from all pages of curve report
                    for page_num in range(len(doc)):
                        page = doc[page_num]
                        text = page.get_text()
                        lines = text.split('\n')
                        for index, line in enumerate(lines):
                            if line.startswith('Analyte:'):
                                analyte_index = index
                                analyte = line.split(': ')[1]
                                r_squared = lines[analyte_index + 1].split('=')[1]
                                equation = lines[analyte_index + 2]
                                fit_type_line = lines[analyte_index + 3]
                                fit_type = fit_type_line.split('Fit Type: ')[1].split()[0]
                                weight = fit_type_line.split('Weight: ')[1]
                                # Create a tuple and add it to the list
                                curve_tuple = (analyte, r_squared, equation, fit_type, weight)
                                #print(curve_tuple)
                                tuples_list.append(curve_tuple)
                    #uses dictionary key to ensure unique object name
                    curve_count += 1
                    curve_key = f"curve_{curve_count}"
                    curves[curve_key] = Sample(curve_key, pdf_path, curve_key, {QCTYPE.CUR}, None, tuples_list)
                    print("found curve")
                    samples.append(curves[curve_key])
                    doc.close()
                    continue
                # Find case number using sample name index + 1
                try:
                    sample_name_index = lines.index("Sample Name")
                    results_index = lines.index("Quantitative Results: FID 1")
                except ValueError:
                    print(f"invalid sample {filename}")
                    doc.close
                    continue
                case_number = lines[sample_name_index + 1]
                # Trim characters off case number string
                case_number = case_number[2:].upper()
                analytes_data = []

                analytes_data.extend(lines[(results_index + 2):])
                
                def convert_table(analytes_data):
                    # Extracting values from the list
                    names = analytes_data[0:6]
                    rt_values = analytes_data[6:12]
                    rrt_values = analytes_data[12:18]
                    area_values = analytes_data[18:24]
                    conc_values = analytes_data[24:30]
                    unit_values = analytes_data[30:36]
                    # Creating tuples
                    analytes_list = []
                    ISTD_list = []
                    for i in range(0,5):
                        analytes_list.append((names[i].strip(), rt_values[i].strip(), rrt_values[i].strip(), 
                                            area_values[i].strip(), conc_values[i].strip(), unit_values[i].strip()))
                    for i in [0, 5]:
                        ISTD_list.append((names[i].strip(), rt_values[i].strip(), rrt_values[i].strip(), 
                                            area_values[i].strip(), conc_values[i].strip(), unit_values[i].strip()))
                    return ISTD_list, analytes_list
                
                format_ISTDs, format_analytes = convert_table(analytes_data)

                case_ID = f"{case_number}_0"
                #change case number if it already exists as an object
                duplicate_count = 1
                while any(case_ID == sample.ID for sample in samples):
                    case_ID = f"{case_ID.rsplit('_', 1)[0]}_{duplicate_count}"
                    duplicate_count += 1
                    print(f"recognized duplicate, new ID: {case_ID}")
                
                #create sample object
                case_ID = Sample(case_ID, pdf_path, case_number, None, format_ISTDs, format_analytes)
                #print(case_ID)
                samples.append(case_ID)
            except Exception as e:
                print(f"--ERROR-- FAILED TO INIT SAMPLE (VERY BAD) {filename}: {e}")
                doc.close()
                continue
            doc.close()  

    #return list of sample objects
    print(f"{len(samples)} samples initialized from directory {batch_dir}")        
    return samples

if __name__ == "__main__":

    batch = 12786
    
    batch_dirs = [
        r"C:\Users\e314883\Desktop\locked_git_repo"
    ]


    for batch in batch_dirs:
        sqvol_init(batch)

