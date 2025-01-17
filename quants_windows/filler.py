from PyPDFForm import FormWrapper # type: ignore # pypdfform

def ISAR_fill(controls, batch, method):
    #change to controls.results_ISTD
    low1 = controls[0]
    high1 = controls[1]
    low2 = controls[-1]
    high2 = controls[-2]

    #sort through ISAR_controls.results_ISTD and find values to pass
    def get_indexes(single_control):
        for tuples in single_control:
            return tuples.index('Area'), len(single_control)
    
    area_index, length = get_indexes(low1)

    field_low1 = [f'A{i}_L1_1' for i in range(1,length)]
    field_high1 = [f'A{i}_L2_1' for i in range(1,length)]
    field_low2 = [f'A{i}_L1_2' for i in range(1,length)]
    field_high2 = [f'A{i}_L2_2' for i in range(1,length)]

    value_low1 = []
    value_high1 = []
    value_low2 = []
    value_high2 = []

    for tuples in low1[1:]:
        value_low1.append(tuples[area_index])
    for tuples in high1[1:]:
        value_high1.append(tuples[area_index])
    for tuples in low2[1:]:
        value_low2.append(tuples[area_index])
    for tuples in high2[1:]:
        value_high2.append(tuples[area_index])

    # #map field name to value in dictionary
    low1_dict = dict(zip(field_low1, value_low1))
    high1_dict = dict(zip(field_high1, value_high1))
    low2_dict = dict(zip(field_low2, value_low2))
    high2_dict = dict(zip(field_high2, value_high2))


    # #find and import/copy ISAR for method
    # def find_form(*args):
    #     pass
    # #make sure that it can find it even if revision changes

    pdf = FormWrapper(r'C:\Users\e314883\Desktop\python pdf\quants_windows\pdf1.pdf')

    pdf.fill({'Batch': batch}, adobe_mode = True)
    pdf.fill(low1_dict, adobe_mode = True)
    pdf.fill(high1_dict, adobe_mode = True)
    pdf.fill(low2_dict, adobe_mode = True)
    pdf.fill(high2_dict, adobe_mode = True)
    
    filled_pdf_path = (r'C:\Users\e314883\Desktop\python pdf\quants_windows\filled_pdf1.pdf')
    with open(filled_pdf_path, "wb") as output:
        output.write(pdf.read())

    # #calculate own -50 - 200% range unless can read from pdf
    # #don't forget about failed cases/analytes field
    #send ISAR results to txt or csv file

if __name__ == '__main__':
    controls = [
[
        ('ID#', 'Name', 'Ret. Time (min)', 'Area', 'Quant Ion (m/z)', '', '', 'Mode'),
        ('1', 'Morphine-D3', '0.412', '1600408', '289.20>165.20', '', '', ''),
        ('3', 'Codeine-D3', '0.945', '1295371', '303.20>165.20', '', '', ''),
        ('5', '6-Acetylmorphine-D3', '1.102', '853868', '331.20>165.20', '', '', ''),
        ('7', 'Benzoylecgonine-D3', '1.555', '1781774', '293.20>171.20', '', '', ''),
        ('9', 'Cocaine-D3', '1.892', '2836682', '307.20>185.20', '', '', ''),
        ('11', 'Cocaethylene-D3', '2.026', '2480191', '321.20>199.20', '', '', ''),
        ('13', 'Fentanyl-D5', '2.122', '2008895', '342.20>188.20', '', '', ''),
        ('15', 'Alprazolam-D5', '2.319', '2090488', '314.20>286.20', '', '', '')
    ],[
        ('ID#', 'Name', 'Ret. Time (min)', 'Area', 'Quant Ion (m/z)', '', '', 'Mode'),
        ('1', 'Morphine-D3', '0.412', '1600408', '289.20>165.20', '', '', ''),
        ('3', 'Codeine-D3', '0.945', '1295371', '303.20>165.20', '', '', ''),
        ('5', '6-Acetylmorphine-D3', '1.102', '853868', '331.20>165.20', '', '', ''),
        ('7', 'Benzoylecgonine-D3', '1.555', '1781774', '293.20>171.20', '', '', ''),
        ('9', 'Cocaine-D3', '1.892', '2836682', '307.20>185.20', '', '', ''),
        ('11', 'Cocaethylene-D3', '2.026', '2480191', '321.20>199.20', '', '', ''),
        ('13', 'Fentanyl-D5', '2.122', '2008895', '342.20>188.20', '', '', ''),
        ('15', 'Alprazolam-D5', '2.319', '2090488', '314.20>286.20', '', '', '')
    ],[
        ('ID#', 'Name', 'Ret. Time (min)', 'Area', 'Quant Ion (m/z)', '', '', 'Mode'),
        ('1', 'Morphine-D3', '0.412', '1600408', '289.20>165.20', '', '', ''),
        ('3', 'Codeine-D3', '0.945', '1295371', '303.20>165.20', '', '', ''),
        ('5', '6-Acetylmorphine-D3', '1.102', '853868', '331.20>165.20', '', '', ''),
        ('7', 'Benzoylecgonine-D3', '1.555', '1781774', '293.20>171.20', '', '', ''),
        ('9', 'Cocaine-D3', '1.892', '2836682', '307.20>185.20', '', '', ''),
        ('11', 'Cocaethylene-D3', '2.026', '2480191', '321.20>199.20', '', '', ''),
        ('13', 'Fentanyl-D5', '2.122', '2008895', '342.20>188.20', '', '', ''),
        ('15', 'Alprazolam-D5', '2.319', '2090488', '314.20>286.20', '', '', '')
    ],[
        ('ID#', 'Name', 'Ret. Time (min)', 'Area', 'Quant Ion (m/z)', '', '', 'Mode'),
        ('1', 'Morphine-D3', '0.412', '1600408', '289.20>165.20', '', '', ''),
        ('3', 'Codeine-D3', '0.945', '1295371', '303.20>165.20', '', '', ''),
        ('5', '6-Acetylmorphine-D3', '1.102', '853868', '331.20>165.20', '', '', ''),
        ('7', 'Benzoylecgonine-D3', '1.555', '1781774', '293.20>171.20', '', '', ''),
        ('9', 'Cocaine-D3', '1.892', '2836682', '307.20>185.20', '', '', ''),
        ('11', 'Cocaethylene-D3', '2.026', '2480191', '321.20>199.20', '', '', ''),
        ('13', 'Fentanyl-D5', '2.122', '2008895', '342.20>188.20', '', '', ''),
        ('15', 'Alprazolam-D5', '2.319', '2090488', '314.20>286.20', '', '', '')
    ],
    ]
    batch = 111
    method = 'QTABUSE'
    ISAR_fill(controls, batch, method)