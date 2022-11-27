## coding:utf-8
# not used
import os
import sys
sys.path.append('..')
from Implementation.ProjectDir import SLICES_DIR, LABEL_SOURCE_DIR, SARD_SOURCE_DATA

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata 
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

def trim_slice_lists(slicelists):
    if slicelists[0] == '':
        del slicelists[0]
    if slicelists[-1] == '' or slicelists[-1] == '\n' or slicelists[-1] == '\r\n':
        del slicelists[-1]

def trim_sentence_list(sentences):
    if sentences[0] == '\r' or sentences[0] == '':
        del sentences[0]
    if sentences[-1] == '':
        del sentences[-1]
    if sentences[-1] == '\r':
        del sentences[-1]

def main():
    from make_label_nvd import write_label_to_file as NVD_write_label
    from make_label_sard import write_label_to_file as SARD_write_label
    
    for file in os.listdir(SLICES_DIR):
        abs_file_path = os.path.join(SLICES_DIR, file)
        file_name = file.split('.')[0] # <file_name>.txt
        target_file_path = os.path.join(LABEL_SOURCE_DIR, file_name + '_label.pkl')
        
        f = open(abs_file_path, 'r')
        slicelists = f.read().split('------------------------------')
        f.close()
        
        NVD_write_label(slicelists, target_file_path)
        SARD_write_label(slicelists, target_file_path, 'ab')


if __name__ == '__main__':
    main()