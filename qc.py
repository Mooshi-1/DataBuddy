from objects import Sample, QCTYPE
import re

def QC_handler(all_samples):
    cal_curve = []
    neg_ctl = []
    shooter = []
    controls = []
    dil_controls = []
    SR_cases = []
    cases = []
    curve = []
    MOA_cases = []
    sequence = []
    for sample in all_samples:
        if sample.type == {QCTYPE.CAL}:
            cal_curve.append(sample)
        elif sample.type == {QCTYPE.SEQ}:
            sequence.append(sample)
        elif sample.type == {QCTYPE.CUR}:
            curve.append(sample)
        elif sample.type == {QCTYPE.SH}: 
            shooter.append(sample)
        elif sample.type.issuperset({QCTYPE.NEG,QCTYPE.CTL}):
            neg_ctl.append(sample)
        elif sample.type == {QCTYPE.CTL}:
            controls.append(sample)
        elif sample.type.issuperset({QCTYPE.DL,QCTYPE.CTL}):
            dil_controls.append(sample)
        elif QCTYPE.SR in sample.type:
            SR_cases.append(sample)
        elif QCTYPE.MOA in sample.type:
            MOA_cases.append(sample)
        else:
            cases.append(sample)
    return cal_curve, neg_ctl, shooter, controls, dil_controls, SR_cases, cases, curve, MOA_cases, sequence

def extract_key(sample):
    # extract numerical parts for sorting
    remove_suffix = re.sub(r'_0$', '', sample.ID)
    parts = re.findall(r'\d+', remove_suffix)
    parts = [int(part) for part in parts]
    return parts

def sort_samples(list):
    list.sort(key=extract_key)
