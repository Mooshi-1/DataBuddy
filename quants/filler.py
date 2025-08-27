from PyPDFForm import FormWrapper
import time
import pandas # type: ignore # pandas
import os
import warnings
import openpyxl # type: ignore # openpyxl
import openpyxl.cell._writer #pyinstaller needs this specific line or will be missing dependancy
#import xlsxwriter
import win32com.client as win32

#testing imports
# import sample_sorter
# import aux_func
# import shimadzu_init
# import searcher

warnings.simplefilter(action='ignore', category=FutureWarning)

def ISAR_fill(controls, batch, path):
    low1 = controls[0]
    high1 = controls[1]
    low2 = controls[-2]
    high2 = controls[-1]

    #sort through ISAR_controls.results_ISTD and find values to pass
    def get_indexes(single_control):
        for tuples in single_control.results_ISTD:
            return tuples.index('Area'), len(single_control.results_ISTD)
    
    area_index, length = get_indexes(low1)

    field_low1 = [f'A{i}_L1_1' for i in range(1,length)]
    field_high1 = [f'A{i}_L2_1' for i in range(1,length)]
    field_low2 = [f'A{i}_L1_2' for i in range(1,length)]
    field_high2 = [f'A{i}_L2_2' for i in range(1,length)]

    value_low1 = []
    value_high1 = []
    value_low2 = []
    value_high2 = []

    for tuples in low1.results_ISTD[1:]:
        value_low1.append(tuples[area_index])
    for tuples in high1.results_ISTD[1:]:
        value_high1.append(tuples[area_index])
    for tuples in low2.results_ISTD[1:]:
        value_low2.append(tuples[area_index])
    for tuples in high2.results_ISTD[1:]:
        value_high2.append(tuples[area_index])

    # #map field name to value in dictionary
    low1_dict = dict(zip(field_low1, value_low1))
    high1_dict = dict(zip(field_high1, value_high1))
    low2_dict = dict(zip(field_low2, value_low2))
    high2_dict = dict(zip(field_high2, value_high2))

    pdf = FormWrapper(path)

    pdf.fill({'Batch': batch}, adobe_mode = True)
    pdf.fill(low1_dict, adobe_mode = True)
    pdf.fill(high1_dict, adobe_mode = True)
    pdf.fill(low2_dict, adobe_mode = True)
    pdf.fill(high2_dict, adobe_mode = True)
    
    filled_pdf_path = (path)
    with open(filled_pdf_path, "wb") as output:
        output.write(pdf.read())

    print("ISAR filled and saved successfully!")
    # #calculate own -50 - 200% range unless can read from pdf
    # #don't forget about failed cases/analytes field
    #send ISAR results to txt or csv file

def SR_fill(cases, batch, path):
    pass

def output_LJ_2(controls, serum_controls, batch, path, extraction_date):
    analyte_dataframes = {}

    single_control = controls[0] or serum_controls[0]
    def get_indexes(single_control):
        for tuples in single_control.results_analyte:
            return tuples.index('Conc.'), tuples.index('Name')

    conc_index, name_index = get_indexes(single_control)   
    
    for i in range(0, len(controls), 2):
        low_control = controls[i]
        high_control = controls[i+1]

        for low_result, high_result in zip(low_control.results_analyte[1:], high_control.results_analyte[1:]):
            analyte_name = low_result[name_index]
            low_conc_value = float(low_result[conc_index])
            high_conc_value = float(high_result[conc_index])

            if analyte_name not in analyte_dataframes:
                analyte_dataframes[analyte_name] = []

            analyte_dataframes[analyte_name].append({"Batch": f"{extraction_date} - {batch}",
                                                     "CTL Low Conc.": low_conc_value, 
                                                     "CTL High Conc.": high_conc_value,
                                                     "Matrix": "Blood",
                                                     "Analyte": analyte_name})
    for i in range(0, len(serum_controls), 2):
        low_serum_control = serum_controls[i]
        high_serum_control = serum_controls[i+1]

        for low_result_serum, high_result_serum in zip(low_serum_control.results_analyte[1:], high_serum_control.results_analyte[1:]):
            analyte_name = low_result_serum[name_index]
            low_conc_value = float(low_result_serum[conc_index])
            high_conc_value = float(high_result_serum[conc_index])

            if analyte_name not in analyte_dataframes:
                analyte_dataframes[analyte_name] = []

            analyte_dataframes[analyte_name].append({"Batch": f"{extraction_date} - {batch}",
                                                     "CTL Low Conc.": low_conc_value, 
                                                     "CTL High Conc.": high_conc_value,
                                                     "Matrix": "Serum",
                                                     "Analyte": analyte_name})
                                  
    # Combine all analyte DataFrames into one
    combined_data = []
    for analyte_name, data in analyte_dataframes.items():
        combined_data.extend(data)
    
    combined_df = pandas.DataFrame(combined_data)

    output_path = os.path.join(path, "LJ.xlsx")

    with pandas.ExcelWriter(output_path, engine='openpyxl') as writer:
        combined_df.to_excel(writer, sheet_name="All Analytes", index=False)

    workbook = openpyxl.load_workbook(output_path)
    sheet = workbook["All Analytes"]

    column_widths = {
        "A": 18,
        "B": 18,
        "C": 18,
        "D": 18,
        "E": 18
    }

    for col, width in column_widths.items():
        sheet.column_dimensions[col].width = width

    for cell in sheet["B"]:
        cell.number_format = '0.000'
    for cell in sheet["C"]:
        cell.number_format = '0.000'

    workbook.save(output_path)
    return output_path

#currently not in use -- will use if JK/MF want analytes on separate tabs again
# def output_LJ(controls, serum_controls, batch, path, extraction_date):
#     analyte_dataframes = {}

#     single_control = controls[0]

#     def get_indexes(single_control):
#         for tuples in single_control.results_analyte:
#             return tuples.index('Conc.'), tuples.index('Name')

#     conc_index, name_index = get_indexes(single_control)   
    
#     for i in range(0, len(controls), 2):
#         low_control = controls[i]
#         high_control = controls[i+1]

#         for low_result, high_result in zip(low_control.results_analyte[1:], high_control.results_analyte[1:]):
#             analyte_name = low_result[name_index]
#             low_conc_value = float(low_result[conc_index])
#             high_conc_value = float(high_result[conc_index])

#             if analyte_name not in analyte_dataframes:
#                 analyte_dataframes[analyte_name] = pandas.DataFrame(columns=[
#                     "Batch", "CTL Low Conc.", "CTL High Conc.", "Matrix"])

#             analyte_dataframes[analyte_name] = pandas.concat(
#                 [analyte_dataframes[analyte_name], pandas.DataFrame({"Batch": f"{extraction_date} - {batch}",
#                                                                     "CTL Low Conc.": [low_conc_value], 
#                                                                     "CTL High Conc.": [high_conc_value],
#                                                                     "Matrix": "Blood"
#                                                                     })], ignore_index=True
#             )

#     for i in range(0, len(serum_controls), 2):
#         low_serum_control = serum_controls[i]
#         high_serum_control = serum_controls[i+1]

#         for low_result_serum, high_result_serum in zip(low_serum_control.results_analyte[1:], high_serum_control.results_analyte[1:]):
#             analyte_name = low_result_serum[name_index]
#             low_conc_value = float(low_result_serum[conc_index])
#             high_conc_value = float(high_result_serum[conc_index])

#             if analyte_name not in analyte_dataframes:
#                 analyte_dataframes[analyte_name] = pandas.DataFrame(columns=[
#                     "Batch", "CTL Low Conc.", "CTL High Conc.", "Matrix"])

#             analyte_dataframes[analyte_name] = pandas.concat(
#                 [analyte_dataframes[analyte_name], pandas.DataFrame({"Batch": f"{extraction_date} - {batch}",
#                                                                     "CTL Low Conc.": [low_conc_value], 
#                                                                     "CTL High Conc.": [high_conc_value],
#                                                                     "Matrix": "Serum"
#                                                                     })], ignore_index=True
#             )

#     output_path = os.path.join(path, "LJ.xlsx")

    # with pandas.ExcelWriter(output_path, engine='openpyxl') as writer:
    #     for analyte, df in analyte_dataframes.items():
    #         df.to_excel(writer, sheet_name=analyte, index=False)


        # formatted_date = time.strftime("%m%d%y", time.localtime())
        # output_path = os.path.join(output_dir, f"{name}_{batch}_{formatted_date}.pdf")
        # doc1.save(output_path)
        # print(f"completed binding Batch Pack - {name}_{batch}_{formatted_date}")

def interpret_MSA(case_list):
    #find out how many analytes there are and send to fill_MSA appropriately
    #return how many copies of excel to create and the name for each one
    #right now, specific to SHIMADZU
    base_pdf = case_list[0]
    #print(len(base_pdf.results_analyte))

    def get_indexes(single_control):
        for tuples in single_control.results_ISTD:
            return tuples.index('Name')

    positive_analytes = []
    if len(base_pdf.results_analyte) > 1:
        for tuples in base_pdf.results_analyte[1:]:
            positive_analytes.append(tuples[get_indexes(base_pdf)])

    #print(positive_analytes)

    return positive_analytes

def fill_MSA(case_list, batch, MSA_path, analyte, method):

    base_pdf = case_list[0]
    def get_indexes(base_pdf):
        for tuples in base_pdf.results_analyte:
            return tuples.index('Area'), tuples.index('Name')
    area_index, name_index = get_indexes(base_pdf)  
    
    ISTD_peak_area = []
    analyte_peak_area = []

    for pdf in case_list:
        #print(analyte)
        for tuples in pdf.results_ISTD[1:]:
            if tuples[name_index].startswith(analyte):
                ISTD_peak_area.append(float(tuples[area_index]))
                #print('found area ISTD')
        for tuples in pdf.results_analyte[1:]:
            if analyte in tuples:
                analyte_peak_area.append(float(tuples[area_index]))

    # print(ISTD_peak_area)
    # print(analyte_peak_area)
    # print(MSA_path)

    d = {"ISTD Peak Area": ISTD_peak_area, "Analyte Peak Area": analyte_peak_area}
    df = pandas.DataFrame(d)

    try:
        print(f"filling in your MSA for {analyte}...")
        excel = win32.Dispatch('Excel.Application')
        print(f"opened {excel}")
        workbook = excel.Workbooks.Open(MSA_path)

        sheet = workbook.Sheets('LF-10 MSA Worksheet')

        parts = base_pdf.base.split('_')
        case_number = parts[0]
        specimen_type = parts[1]
        dilution = parts[2].replace('X','')
        formatted_date = time.strftime("%m/%d", time.localtime())

        sheet.Range('F4').Value = method
        sheet.Range('C4').Value = case_number
        sheet.Range('C6').Value = batch
        sheet.Range('F8').Value = analyte
        sheet.Range('C10').Value = specimen_type
        sheet.Range('F12').Value = dilution
        sheet.Range('C8').Value = formatted_date

        # Write DataFrame to the specified location
        startrow = 15
        startcol = 4
        for i, row in df.iterrows():
            for j, value in enumerate(row):
                cell = sheet.Cells(startrow + i, startcol + j)
                cell.Value = value


        workbook.Save()
        workbook.Close()
        excel.Quit()
        print(f'completed filling {MSA_path}')
        # #
        # # with pandas.ExcelWriter(MSA_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        # #     df.to_excel(writer, sheet_name='Data', header=False, startrow=14, startcol=3, index=False)

    except Exception as e:
        workbook.Close()
        excel.Quit()
        print(f"excel fill error {analyte} | {e}")

def append_LJ_curve(curve, batch, path, extraction_date, initials):
    #[('Amphetamine', 0.999334, 'y=21.561360*x-0.007798', 'Linear', '1/C^2'), 
    #('Benzoylecgonine', 0.999354, 'y=-0.044906*x^2+2.409508*x-0.009472', 'Quadratic', '1/C^2')]
    linear_columns = ['Date - Batch', 'r^2', 'Slope (MX)', 'Y-Intercept (b)', 'Analyst', 'Analyte']
    linear_rows = []

    quadratic_columns = ['Date - Batch', 'r^2', 'Quadratic Coefficient (ax^2)', 'Linear Coefficient (bx)', 'Constant (c)', 'Analyst', 'Analyte']
    quadratic_rows = []
    for obj in curve:
        for tuples in obj.results_analyte:
            if 'Linear' in tuples:
                analyte = tuples[0]
                r2 = float(tuples[1])
                equation = tuples[2]
                mx = float(equation.split('*x')[0].replace('y=',''))
                b = float(equation.split('*x')[1])
                linear_rows.append((f"{extraction_date} - {batch}", r2, mx, b, initials, analyte))

            if 'Quadratic' in tuples:
                analyte = tuples[0]
                r2 = float(tuples[1])
                equation = tuples[2]
                ax2 = float(equation.split('*x^2')[0].replace('y=',''))
                bx = float(equation[equation.find('*x^2') + len('*x^2'):equation.find('*x', equation.find('*x^2') + len('*x^2'))])
                c = float(equation.split('*x')[-1])
                quadratic_rows.append((f"{extraction_date} - {batch}", r2, ax2, bx, c, initials, analyte))                


    df1 = pandas.DataFrame(linear_rows, columns=linear_columns)
    df2 = pandas.DataFrame(quadratic_rows, columns=quadratic_columns)

    output_path = os.path.join(path, "LJ.xlsx")
    if os.path.exists(output_path):
        with pandas.ExcelWriter(output_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            df1.to_excel(writer, sheet_name='Curves_Linear', index=False)
            df2.to_excel(writer, sheet_name='Curves_Quadratic', index=False)

    else:
        with pandas.ExcelWriter(output_path, engine='openpyxl') as writer:
            df1.to_excel(writer, sheet_name='Curves_Linear', index=False)
            df2.to_excel(writer, sheet_name='Curves_Quadratic', index=False)

    return output_path

#make super clean, use index, build up dataframe
def append_new_LJ(controls, serum_controls, batch, path, extraction_date):
    analyte_dataframes = {}

    single_control = controls[0]
    def get_indexes(single_control):
        for tuples in single_control.results_analyte:
            return tuples.index('Conc.'), tuples.index('Name')

    conc_index, name_index = get_indexes(single_control)   
    
    for i in range(0, len(controls), 2):
        low_control = controls[i]
        high_control = controls[i+1]

        for low_result, high_result in zip(low_control.results_analyte[1:], high_control.results_analyte[1:]):
            analyte_name = low_result[name_index]
            low_conc_value = float(low_result[conc_index])
            high_conc_value = float(high_result[conc_index])

            if analyte_name not in analyte_dataframes:
                analyte_dataframes[analyte_name] = []

            analyte_dataframes[analyte_name].append({"Batch": f"{extraction_date} - {batch}",
                                                     "CTL Low Conc.": low_conc_value, 
                                                     "CTL High Conc.": high_conc_value,
                                                     "Matrix": "Blood",
                                                     "Analyte": analyte_name})

    rows_indexes = [
        'Date - Batch',
        'Matrix',
        'Analyst',
        analyte_name
        #2 spaces
        #repeat for high control
    ]

if __name__ == '__main__':
    batch = 111
    method = 'QTABUSE'
    path = r"C:\Users\e314883\Desktop\locked_git_repo\12786"
    #output_LJ(controls, [], batch, path)
    #ISAR_fill(controls_ISTD, batch, method)