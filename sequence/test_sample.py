import os
import pytest
import pandas
import seq_main
import seq_init


TEST_FILES_DIR = r"./test/"

def test_quants():
    def test_file_1():
        samples, method, batch = seq_init.read_sequence(os.path.join(TEST_FILES_DIR, 'quant_g_b_dil.pdf'))
        assert samples[0].bad == True
        assert samples[0].MSA == True
        seq_main.build_and_export(samples, method, batch, TEST_FILES_DIR)
        return
    test_file_1()
    return