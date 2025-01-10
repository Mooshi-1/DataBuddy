from objects import Sample, QCTYPE

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
    for sample in all_samples:
        if sample.type == {QCTYPE.CAL}:
            cal_curve.append(sample)
        elif sample.type == {QCTYPE.CUR}:
            curve.append(sample)
        elif sample.type == {QCTYPE.SH}: 
            shooter.append(sample)
        elif sample.type == {QCTYPE.NEG}:
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