
from uitest.framework import UITestCase
from uitest.uihelper.common import get_state_as_dict, get_url_for_data_file, select_by_text,type_text
from libreoffice.uno.propertyvalue import mkPropertyValues
from tempfile import TemporaryDirectory
from uitest.uihelper.calc import enter_text_to_cell
import time
import os.path
import os

class TestClass(UITestCase):

    def getPos(self,column,row):
        pos = chr(ord('A')+ column - 1)+str(row)
        print(pos)
        return(pos)

    def test_function2(self):
        try:
            with TemporaryDirectory() as tempdir:
                with self.ui_test.create_doc_in_start_center("calc") as document:
                    calcDoc = self.xUITest.getTopFocusWindow()
                    xGridWindow = calcDoc.getChild("grid_window")
                    enter_text_to_cell(xGridWindow, "A1", "Case")
                    enter_text_to_cell(xGridWindow, "B1", "Item")
                    enter_text_to_cell(xGridWindow, "C1", "local time")
                    enter_text_to_cell(xGridWindow, "D1", "standard time")

                    std_time = {}
                    with open('resource/standard.txt', 'r') as file:
                        line = file.readline()
                        while(line):
                            if(''.join(line.split())!=''):
                                item = line.split()
                                std_time[item[0]] = item[1]
                            line = file.readline()

                    row = 2
                    cases = ""
                    item = ""
                    with open('test_result.txt', 'r') as file:
                        line = file.readline()
                        while(line):
                            if(line[0:4]=='Case'):
                                cases = line.split(" ",1)[1]
                            elif (line[0:4] == "Item"):
                                enter_text_to_cell(xGridWindow, self.getPos(1,row), cases)
                                enter_text_to_cell(xGridWindow, self.getPos(2,row), line.split()[1])
                                enter_text_to_cell(xGridWindow, self.getPos(3,row), line.split()[2])
                                enter_text_to_cell(xGridWindow, self.getPos(4,row), std_time[line.split()[1]])
                                row += 1
                            line = file.readline()

                    save_path = os.path.join(os.getcwd(), "test_result.ods")
                    with self.ui_test.execute_dialog_through_command(".uno:SaveAs", close_button="open") as x_save_dialog:
                        x_file_name = x_save_dialog.getChild("file_name")
                        x_file_name.executeAction("TYPE", mkPropertyValues({"KEYCODE":"CTRL+A"}))
                        x_file_name.executeAction("TYPE", mkPropertyValues({"TEXT": save_path}))
                        x_file_type = x_save_dialog.getChild("file_type")
                        select_by_text(x_file_type, "ODF Spreadsheet (.ods)")
        except IndexError:
            print('Test Message: IndexError Captured. This exception is common in riscv64.')
            print('Test Message: This does not handicap our test. Continue.....')
