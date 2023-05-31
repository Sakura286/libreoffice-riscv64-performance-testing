
from uitest.framework import UITestCase
from uitest.uihelper.common import get_state_as_dict, get_url_for_data_file, select_by_text,type_text
from libreoffice.uno.propertyvalue import mkPropertyValues
from tempfile import TemporaryDirectory
import time
import os.path


class ExtFunc():
    
    DEFAULT_SLEEP = 0.05

    # TODO: add visible view of the results
    @staticmethod
    def Write(str):
        with open('test_result.txt', 'a') as file:
            file.write(str)

    @staticmethod
    def Time_Record(item, test_time):
        ExtFunc.Write('Item: {0}\t{1:.3f}\n'.format(item, test_time))

    @staticmethod
    def Trim_Average(list_item):

        max_value = max(list_item)
        list_item.remove(max_value)

        min_value = min(list_item)
        list_item.remove(min_value)

        return sum(list_item)/len(list_item)

    # arithmatic average
    @staticmethod
    def Ari_Average(list_item):
        return sum(list_item)/len(list_item)
        

    # An opposite implement of wait_until_property_is_updated
    @staticmethod
    def Wait_Until_Property_Is_Updated_Custom(element, propertyName, value):
        while True:
            if get_state_as_dict(element)[propertyName] != value:
                return
            else:
                time.sleep(ExtFunc.DEFAULT_SLEEP)



class JustAUITest(UITestCase):



    # test LibreOffice writer with a silulation of daily office work
    # such as load a file, copy and paste, insert an image, save the doc,
    # export to pdf
    def test_writer(self):
        ExtFunc.Write('Case: Writer - Common Test')
        try:
            with TemporaryDirectory() as tempdir:
                load_start_time = time.time()
                with self.ui_test.load_file(get_url_for_data_file('writer_doc_1.odt')):
                    load_end_time = time.time()
                    load_time = load_end_time - load_start_time
                    self.xUITest.executeCommand('.uno:SelectAll')
                    self.xUITest.executeCommand('.uno:Copy')
                    load_start_time = time.time()
                    with self.ui_test.load_file(get_url_for_data_file('writer_doc_2.odt')):
                        load_end_time = time.time()
                        load_time += load_end_time - load_start_time
                        ExtFunc.Time_Record('writer_load_doc', load_time)

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
                        while(not os.path.exists(save_path)):
                                time.sleep(ExtFunc.DEFAULT_SLEEP)
                        save_end_time = time.time()
                        list_save_time.append(save_end_time-save_start_time)
                        

                        # test paste
                        list_paste_time = []
                        for i in range(8):
                            paste_start_time = time.time()
                            self.xUITest.executeCommand(".uno:Paste")
                            paste_end_time = time.time()
                            list_paste_time.append(paste_end_time-paste_start_time)
                        ExtFunc.Time_Record('writer_copy_paste',sum(list_paste_time))
                        
                        # save_1
                        modified_time = os.path.getmtime(save_path)
                        save_start_time=time.time()
                        self.xUITest.executeCommand('.uno:Save')
                        while(modified_time == os.path.getmtime(save_path)):
                            time.sleep(ExtFunc.DEFAULT_SLEEP)
                        save_end_time = time.time()
                        list_save_time.append(save_end_time-save_start_time)

                        # test insert pic
                        # TODO: add more pics in differenct position
                        list_pic_time = []
                        for i in range(1,6):
                            pic_start_time = 0.0
                            writer_doc = self.xUITest.getTopFocusWindow()
                            writer_edit = writer_doc.getChild('writer_edit')

                            with self.ui_test.execute_dialog_through_command(".uno:InsertGraphic", close_button="open") as xOpenDialog:
                                x_file_name = xOpenDialog.getChild("file_name")
                                # TODO: edit name
                                x_file_name.executeAction("TYPE", mkPropertyValues({"TEXT": get_url_for_data_file("pic_{0}.jpg".format(i))}))
                                pic_start_time = time.time()
                                # ESC should be pressed to deselect the image.
                            self.xUITest.executeCommand(".uno:Escape")
                            writer_edit.executeAction("TYPE", mkPropertyValues({"KEYCODE":"RETURN"}))
                            pic_end_time = time.time()
                            list_pic_time.append(pic_end_time-pic_start_time)
                            time.sleep(1)
                        ExtFunc.Time_Record('writer_insert_image',sum(list_pic_time))
                            
                        # save_2
                        save_start_time=time.time()
                        modified_time = os.path.getmtime(save_path)
                        self.xUITest.executeCommand('.uno:Save')
                        while(modified_time == os.path.getmtime(save_path)):
                            time.sleep(ExtFunc.DEFAULT_SLEEP)
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
                            time.sleep(ExtFunc.DEFAULT_SLEEP)
                        save_end_time = time.time()
                        list_save_time.append(save_end_time-save_start_time)

                        ## since there is 4 time different saves, we do not need trim_average()
                        ## to remove the max and the min value.
                        ExtFunc.Time_Record('writer_save_doc', ExtFunc.Ari_Average(list_save_time))

                        # export pdf
                        # Export LOOPS times, remove the maximum and minnimum export time,
                        # then make an average of them.
                        list_export_pdf_time = []
                        for i in range(5):
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
                                time.sleep(ExtFunc.DEFAULT_SLEEP)
                            pdf_end_time = time.time()
                            list_export_pdf_time.append(pdf_end_time-pdf_start_time)

                        ExtFunc.Time_Record('writer_export_pdf', ExtFunc.Trim_Average(list_export_pdf_time))
        except IndexError:
            print('Test Message: IndexError Captured. This exception is common in riscv64.')
            print('Test Message: This does not handicap our test. Continue.....')

    


    # test high load of LibreOffice Calc
    # recalculate a huge sheet 5 times,
    # then recalculate the average running time

    def test_calc(self):
        ExtFunc.Write('Case: Calc - Common Test')
        LOOPS = 5
        for filename in ['BuildingDesign.xls','StocksPriceTimeCorrelation.xls']:
            list_calc_time = []
            for i in range(LOOPS):
                try:
                    with self.ui_test.load_file(get_url_for_data_file('BuildingDesign.xls')):

                        start_time = time.time()
                        self.xUITest.executeCommand(".uno:Calculate")
                        end_time = time.time()
                        
                        list_calc_time.append(end_time-start_time)
                except IndexError:
                    print('Test Message: IndexError Captured. This exception is common in riscv64.')
                    print('Test Message: This does not handicap our test. Continue.....')
                    
            ExtFunc.Time_Record('Calc_Load_'+filename[: filename.find('.')], ExtFunc.Trim_Average(list_calc_time))

            
                        
