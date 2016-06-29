import bin_info,trash_info
import time

BIN_SHEET = "trashbins.csv"
LEVEL_SHEET = "realTrash.csv"
FILENAME = "realTrash.csv"


while (True):
    test_trash = trash_info.trash_info(FILENAME)
    test_trash.updateCsv(FILENAME)
    bins = bin_info.bin_info(BIN_SHEET, LEVEL_SHEET)
    bins.update_response()
    time.sleep(1000)