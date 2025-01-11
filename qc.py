from objects import QCTYPE
import re

def general_sort_key(sample):
    # extract numerical parts for sorting
    remove_suffix = re.sub(r'_0$', '', sample.ID)
    parts = re.findall(r'\d+', remove_suffix)
    parts = [int(part) for part in parts]
    return parts

def sort_samples(list):
    list.sort(key=general_sort_key)

def control_sort_key(sample):
    #sorts low 1 - high 1 - low 2 etc 
    match = re.match(r'(LOW|HIGH) CTL (\d+)', sample.base)
    if match:
        control_type, num = match.groups()
        #assign weight so low comes first
        weight = 0 if control_type == 'LOW' else 1
        return (int(num), weight)
    return (sample.base,)

def sort_controls(list):
    list.sort(key=control_sort_key)


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
    #note that controls got a seperate sort method
    sort_samples(cal_curve); sort_samples(neg_ctl); sort_samples(shooter)
    sort_controls(controls); sort_samples(dil_controls); sort_samples(SR_cases)
    sort_samples(cases); sort_samples(curve); sort_samples(MOA_cases); sort_samples(sequence)



    return cal_curve, neg_ctl, shooter, controls, dil_controls, SR_cases, cases, curve, MOA_cases, sequence

def batch_pack_handler(curve,shooter,neg_ctl,cal_curve,controls,sequence,dil_controls):
    #get dil_controls inserted properly

    batch_pack = curve + shooter + neg_ctl + cal_curve + controls + sequence
    return batch_pack
