import fitz  # type: ignore # PyMuPDF
print(fitz.__file__)
from sample_sorter import QCTYPE, Sample

sample1 = Sample(
    "24-3233_BRNCUP_x20_0",
    {<QCTYPE.MOA: 'method of addition'>, <QCTYPE.DL: 'dilution'>},
    "24-3233_BRNCUP_x20",
    [
        ('ID#', 'Name', 'Ret. Time (min)', 'Area', 'Quant Ion (m/z)', '', '', 'Mode'),
        ('1', 'Morphine-D3', '0.412', '1452346', '289.20>165.20', '', '', ''),
        ('3', 'Codeine-D3', '0.946', '1156348', '303.20>165.20', '', '', ''),
        ('5', '6-Acetylmorphine-D3', '1.102', '752387', '331.20>165.20', '', '', ''),
        ('7', 'Benzoylecgonine-D3', '1.554', '1701626', '293.20>171.20', '', '', ''),
        ('9', 'Cocaine-D3', '1.891', '2747661', '307.20>185.20', '', '', ''),
        ('11', 'Cocaethylene-D3', '2.024', '2481478', '321.20>199.20', '', '', ''),
        ('13', 'Fentanyl-D5', '2.120', '2079200', '342.20>188.20', '', '', ''),
        ('15', 'Alprazolam-D5', '2.317', '2105863', '314.20>286.20', '', '', '')
    ],
    [
        ('ID#', 'Name', 'Ret. Time (min)', 'Area', 'Quant Ion (m/z)', 'Conc.', 'Unit', 'Mode'),
        ('14', 'Fentanyl', '2.124', '568634', '337.20>188.20', '3.321', 'ng/mL', '')
    ],
    r"/home/mooshi_1/workspace/github.com/Mooshi-1/Work/locked/private/12786/CASE DATA/24-3233_BRNCUP_x20_0.pdf"
)

sample2 = Sample(
    "24-3233_BRNCUP_x20_L1_0",
    {<QCTYPE.MOA: 'method of addition'>, <QCTYPE.DL: 'dilution'>, <QCTYPE.CAL: 'calibrator'>},
    "24-3233_BRNCUP_x20_L1",
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
    ],
    [
        ('ID#', 'Name', 'Ret. Time (min)', 'Area', 'Quant Ion (m/z)', 'Conc.', 'Unit', 'Mode'),
        ('2', 'Morphine', '0.415', '161400', '286.20>165.20', '0.008', 'mg/L', ''),
        ('4', 'Codeine', '0.955', '135171', '300.20>165.20', '0.009', 'mg/L', ''),
        ('6', '6-Acetylmorphine', '1.108', '86409', '328.20>165.20', '0.910', 'ng/mL', ''),
        ('8', 'Benzoylecgonine', '1.559', '147846', '290.20>168.20', '0.039', 'mg/L', ''),
        ('10', 'Cocaine', '1.894', '244909', '304.20>182.20', '0.010', 'mg/L', ''),
        ('12', 'Cocaethylene', '2.027', '233458', '318.20>196.20', '0.010', 'mg/L', ''),
        ('14', 'Fentanyl', '2.125', '794659', '337.20>188.20', '4.852', 'ng/mL', ''),
        ('16', 'Alprazolam', '2.323', '166212', '309.20>281.20', '0.011', 'mg/L', '')
    ],
    r"/home/mooshi_1/workspace/github.com/Mooshi-1/Work/locked/private/12786/CASE DATA/24-3233_BRNCUP_x20_L1_0.pdf"
)

sample3 = Sample(
    "24-3233_BRNCUP_x20_L2_0",
    {<QCTYPE.MOA: 'method of addition'>, <QCTYPE.DL: 'dilution'>, <QCTYPE.CAL: 'calibrator'>},
    "24-3233_BRNCUP_x20_L2",
    [
        ('ID#', 'Name', 'Ret. Time (min)', 'Area', 'Quant Ion (m/z)', '', '', 'Mode'),
        ('1', 'Morphine-D3', '0.410', '1509281', '289.20>165.20', '', '', ''),
        ('3', 'Codeine-D3', '0.947', '1132383', '303.20>165.20', '', '', ''),
        ('5', '6-Acetylmorphine-D3', '1.101', '749052', '331.20>165.20', '', '', ''),
        ('7', 'Benzoylecgonine-D3', '1.550', '1726075', '293.20>171.20', '', '', ''),
        ('9', 'Cocaine-D3', '1.886', '2747032', '307.20>185.20', '', '', ''),
        ('11', 'Cocaethylene-D3', '2.019', '2463307', '321.20>199.20', '', '', ''),
        ('13', 'Fentanyl-D5', '2.115', '2128659', '342.20>188.20', '', '', ''),
        ('15', 'Alprazolam-D5', '2.312', '2149821', '314.20>286.20', '', '', '')
    ],
    [
        ('ID#', 'Name', 'Ret. Time (min)', 'Area', 'Quant Ion (m/z)', 'Conc.', 'Unit', 'Mode'),
        ('2', 'Morphine', '0.413', '314808', '286.20>165.20', '0.017', 'mg/L', ''),
        ('4', 'Codeine', '0.956', '224105', '300.20>165.20', '0.019', 'mg/L', ''),
        ('6', '6-Acetylmorphine', '1.107', '152560', '328.20>165.20', '1.875', 'ng/mL', ''),
        ('8', 'Benzoylecgonine', '1.554', '298989', '290.20>168.20', '0.079', 'mg/L', ''),
        ('10', 'Cocaine', '1.888', '482118', '304.20>182.20', '0.020', 'mg/L', ''),
        ('12', 'Cocaethylene', '2.020', '509149', '318.20>196.20', '0.021', 'mg/L', ''),
        ('14', 'Fentanyl', '2.118', '957656', '337.20>188.20', '5.533', 'ng/mL', ''),
        ('16', 'Alprazolam', '2.316', '328786', '309.20>281.20', '0.020', 'mg/L', '')
    ],
    r"/home/mooshi_1/workspace/github.com/Mooshi-1/Work/locked/private/12786/CASE DATA/24-3233_BRNCUP_x20_L2_0.pdf"
)
