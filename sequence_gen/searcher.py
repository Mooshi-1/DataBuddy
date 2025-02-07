import os
import time
import shutil


def LF_plumbing(seq_dir, instrument, initials):
    LF_dir = r'G:\LABORATORY OPERATIONS\06 - LABORATORY FORMS\LF-23 INSTRUMENT CHECKLISTS'
    LF_path = os.path.join(LF_dir, instrument)

    for item in os.listdir(LF_path):
        if item.endswith('.pdf'):
            checklist_path = os.path.join(LF_path, item)
            checklist = item
    
    batch_path = create_LF_directories(LF_path, initials)

    copy_from_generater(seq_dir, batch_path)

    new_checklist = os.path.join(batch_path, checklist)
    if os.path.exists(new_checklist):
        print('checklist already in batch folder')
        return
    else:
        shutil.copy2(checklist_path, new_checklist)

#called by LF_plumbing
def create_LF_directories(base_path, initials):
    current_time = time.localtime()
    formatted_date = time.strftime("%m%d%y", current_time)
    year = time.strftime('%Y', current_time)
    month = time.strftime('%m', current_time)
    final_location = formatted_date + '_' + initials
    date_path = os.path.join(base_path, year, month, final_location)
    print(date_path)
    print('you can copy/paste the path printed above')

    if not os.path.exists(date_path):
        os.makedirs(date_path)
    
    return date_path

#called by LF_plumbing
def copy_from_generater(seq_dir, batch_path):
    for files in os.listdir(seq_dir):
        if files.endswith('.pdf') or files.endswith('.xlsx') or files.endswith('.csv'):
            src_path = os.path.join(seq_dir, files)
            dst_path = os.path.join(batch_path, files)
            shutil.copy2(src_path, dst_path)

    





if __name__ == '__main__':
    batch = '1111'
    instr = 'LF-23.9 Shimadzu 8060 LC-MSMS #1'
    tp_dir = r'C:\Users\e314883\Desktop\LF-23 INSTRUMENT CHECKLISTS'
    LF_plumbing(instr, tp_dir, batch)
