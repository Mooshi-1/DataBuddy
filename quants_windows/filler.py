#import pypdfform # type: ignore # pypdfform

def ISAR_fill(controls, batch, method):
    ISAR_controls = controls[:2] + controls[-2:]
    #maybe keep controls split individually for simplicity?

    #sort through self.results_ISTD and find values to pass
    def get_index(ISAR_controls):
        for control in ISAR_controls:
            for tuples in control:
                return tuples.index('Area')
    
    area_index = get_index(ISAR_controls)
    print(area_index)

    area_list = []

    for control in ISAR_controls:
        for tuples in control[1:]:
            area_list.append(tuples[area_index])

    print(area_list)
    #currently in 1 big list
    # can create new list each time control gets iterated?



    #define field names in the pdf
    #give good thought to how we can adapt the field names for multiple methods
    #probably set length based off of analytes in self.results_ISTD and then match field names to follow
    #field_names = [f'field{i}' for i in range(1,11)]

    # #map field name to value in dictionary
    # data_dict = dict(zip(field_names, sorted_ISAR))
    # #or
    # data_dict = {field: sorted_ISAR[i] for i, field in enumerate(field_names)}
    # #enum(field_names) provides the index i and value field of each element in field_names
    # #uses index to get element from sorted_ISAR and and field_names


    # #find and import/copy ISAR for method
    # def find_form(*args):
    #     pass
    # #make sure that it can find it even if revision changes
    # pdf = pypdfform('ISAR.pdf')

    # pdf.fill(data_dict)

    # with open('ISAR.pdf', 'wb') as output_pdf:
    #     output_pdf.write(pdf.read())


    # #calculate own -50 - 200% range unless can read from pdf
    # #don't forget about failed cases/analytes field
    # #positive control matrix checkbox?

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