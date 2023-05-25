
from uitest.framework import UITestCase
from uitest.uihelper.common import get_state_as_dict, get_url_for_data_file, select_by_text,type_text
from libreoffice.uno.propertyvalue import mkPropertyValues
from libreoffice.calc.document import is_row_hidden
from uitest.uihelper.calc import enter_text_to_cell
from tempfile import TemporaryDirectory
import time
import os.path

DEFAULT_SLEEP = 0.05

# TODO: add visible view of the results
def time_record(item, test_time):
    with open('test_result.txt', 'a') as file:
        file.write('{0}\t{1:.3f}\n'.format(item, test_time))

def trim_average(list_item):

    max_value = max(list_item)
    list_item.remove(max_value)

    min_value = min(list_item)
    list_item.remove(min_value)

    return sum(list_item)/len(list_item)

# arithmatic average
def ari_average(list_item):
    return sum(list_item)/len(list_item)
    

# An opposite implement of wait_until_property_is_updated
def wait_until_property_is_updated_custom(element, propertyName, value):
    while True:
        if get_state_as_dict(element)[propertyName] != value:
            return
        else:
            time.sleep(DEFAULT_SLEEP)

class JustAUITest(UITestCase):

    # test LibreOffice writer with a silulation of daily office work
    # such as load a file, copy and paste, insert an image, save the doc,
    # export to pdf
    def test_writer(self):
        LOOPS = 8
        with TemporaryDirectory() as tempdir:
            load_start_time = time.time()
            with self.ui_test.load_file(get_url_for_data_file('writer_doc_1.odt')):
                load_end_time = time.time()
                load_time = load_end_time - load_start_time
                for i in range(3):
                    self.xUITest.executeCommand('.uno:GoToEndOfPageSel')
                self.xUITest.executeCommand('.uno:Copy')
                load_start_time = time.time()
                with self.ui_test.load_file(get_url_for_data_file('writer_doc_2.odt')):
                    load_end_time = time.time()
                    load_time += load_end_time - load_start_time
                    time_record('load file', load_time)

                    # TODO: test doc and writerdoc diff
                    writer_doc = self.xUITest.getTopFocusWindow()
                    writer_edit = writer_doc.getChild('writer_edit')

                    # test save_0
                    list_save_time = []
                    save_path = os.path.join(tempdir, "writer_doc_2_saveas.odt")
                    save_start_time = 0.0
                    with self.ui_test.execute_dialog_through_command(".uno:SaveAs", close_button="open") as x_save_dialog:
                        x_file_name = x_save_dialog.getChild("file_name")
                        x_file_name.executeAction("TYPE", mkPropertyValues({"KEYCODE":"CTRL+A"}))
                        x_file_name.executeAction("TYPE", mkPropertyValues({"TEXT": save_path}))
                        x_file_type = x_save_dialog.getChild("file_type")
                        # TODO: there is a dialog to close when save to docx at first time
                        select_by_text(x_file_type, "ODF Test Document (.odt)")
                        save_start_time = time.time()
                    time.sleep(10)
                    while(not os.path.exists(save_path)):
                            time.sleep(DEFAULT_SLEEP)
                    save_end_time = time.time()
                    list_save_time.append(save_end_time-save_start_time)
                    

                    # test paste
                    list_paste_time = []
                    for i in range(LOOPS):
                        paste_start_time = time.time()
                        self.xUITest.executeCommand(".uno:Paste")
                        paste_end_time = time.time()
                        list_paste_time.append(paste_end_time-paste_start_time)
                    time_record('paste',sum(list_paste_time))
                    
                    # save_1
                    modified_time = os.path.getmtime(save_path)
                    save_start_time=time.time()
                    self.xUITest.executeCommand('.uno:Save')
                    while(modified_time == os.path.getmtime(save_path)):
                        time.sleep(DEFAULT_SLEEP)
                    save_end_time = time.time()
                    list_save_time.append(save_end_time-save_start_time)

                    # test insert pic
                    # TODO: add more pics in differenct position
                    list_pic_time = []
                    for _ in range(2):
                        pic_start_time = 0.0
                        writer_doc = self.xUITest.getTopFocusWindow()
                        writer_edit = writer_doc.getChild('writer_edit')

                        with self.ui_test.execute_dialog_through_command(".uno:InsertGraphic", close_button="open") as xOpenDialog:
                            x_file_name = xOpenDialog.getChild("file_name")
                            # TODO: edit name
                            x_file_name.executeAction("TYPE", mkPropertyValues({"TEXT": get_url_for_data_file("pic1.jpg")}))
                            pic_start_time = time.time()
                            # ESC should be pressed to deselect the image.
                        self.xUITest.executeCommand(".uno:Escape")
                        writer_edit.executeAction("TYPE", mkPropertyValues({"TEXT":" "}))
                        writer_edit.executeAction("TYPE", mkPropertyValues({"KEYCODE":"RETURN"}))
                        
                        ## After ESC pressed, 'Size' property will change a bit, but it takes a little time to update.
                        ## The open_dialog could not be created during this time.
                        ## This might be caused by that the image is not totally ready.
                        ## So we need to wait for writer_edit until updated.
                        abs_position_value = get_state_as_dict(writer_edit)['AbsPosition']
                        while True:
                            if get_state_as_dict(writer_edit)['AbsPosition'] != abs_position_value:
                                break
                            else:
                                time.sleep(DEFAULT_SLEEP)
                        
                        pic_end_time = time.time()
                        list_pic_time.append(pic_end_time-pic_start_time)
                    time_record('insert pic',sum(list_pic_time))
                        
                    # save_2
                    save_start_time=time.time()
                    modified_time = os.path.getmtime(save_path)
                    self.xUITest.executeCommand('.uno:Save')
                    while(modified_time == os.path.getmtime(save_path)):
                        time.sleep(DEFAULT_SLEEP)
                    save_end_time = time.time()
                    list_save_time.append(save_end_time-save_start_time)

                    ## Do some edit.
                    ## This is a pre-stage for save_3
                    ## get_url_for_data_file() returns the pattern like 'file://...'.
                    ## This does not fit for open() method, so we need to trim the first 7 characters.
                    with open(get_url_for_data_file('char_doc.txt')[7:], 'r') as char_file:
                        lines = char_file.readlines()
                        for line in lines:
                            for one_char in line:
                                writer_edit.executeAction("TYPE", mkPropertyValues({"TEXT" : one_char}))

                    # save_3

                    
                    modified_time = os.path.getmtime(save_path)
                    save_start_time=time.time()
                    self.xUITest.executeCommand('.uno:Save')
                    while(modified_time == os.path.getmtime(save_path)):
                        time.sleep(DEFAULT_SLEEP)
                    save_end_time = time.time()
                    list_save_time.append(save_end_time-save_start_time)

                    ## since there is 4 time different saves, we do not need trim_average()
                    ## to remove the max and the min value.
                    time_record('save', ari_average(list_save_time))

                    # export pdf
                    # Export LOOPS times, remove the maximum and minnimum export time,
                    # then make an average of them.
                    list_export_pdf_time = []
                    for i in range(LOOPS):
                        pdf_start_time = 0.0
                        export_path = os.path.join(tempdir, "test_doc{0}.pdf".format(i))
                        with self.ui_test.execute_dialog_through_command('.uno:ExportToPDF', close_button="") as pdf_dialog:
                            ok_button = pdf_dialog.getChild("ok")
                            with self.ui_test.execute_dialog_through_action(ok_button, "CLICK", close_button="open") as save_dialog:
                                xFileName = save_dialog.getChild('file_name')
                                xFileName.executeAction('TYPE', mkPropertyValues({'KEYCODE':'CTRL+A'}))
                                xFileName.executeAction('TYPE', mkPropertyValues({'KEYCODE':'BACKSPACE'}))
                                xFileName.executeAction('TYPE', mkPropertyValues({'TEXT': export_path}))

                            ## The import time should be from user clicking the "open" button
                            ## to LibreOffice Writer exporting file and being responsive.
                            ## So the start_time should be initialized before the pdf_dialog closed.
                            pdf_start_time = time.time()

                        ## Though the export_to_pdf dialog closed,
                        ## the export process still works background.
                        ## So we need to detect if the file is already exported.
                        while(not os.path.exists(export_path)):
                            time.sleep(DEFAULT_SLEEP)
                        pdf_end_time = time.time()
                        list_export_pdf_time.append(pdf_end_time-pdf_start_time)

                    time_record('export pdf',trim_average(list_export_pdf_time))
    


    # test high load of LibreOffice Calc
    # recalculate a huge sheet ten times,
    # then recalculate the average running time

    def test_calc(self):
        return
        LOOPS = 10

        list_calc_time = []
        for i in range(LOOPS):
            with self.ui_test.load_file(get_url_for_data_file('BuildingDesign.xls')):

                start_time = time.time()
                self.xUITest.executeCommand(".uno:Calculate")
                end_time = time.time()
                
                list_calc_time.append(end_time-start_time)
                
        time_record("building_design", trim_average(list_calc_time))

        list_calc_time = []
        for i in range(LOOPS):
            with self.ui_test.load_file(get_url_for_data_file('StocksPrice_time_correlation.xls')):

                start_time = time.time()
                self.xUITest.executeCommand(".uno:Calculate")
                end_time = time.time()

                list_calc_time.append(end_time-start_time)

        time_record("stocks_price", trim_average(list_calc_time))
            
                        