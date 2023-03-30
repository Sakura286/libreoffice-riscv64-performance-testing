# UITest 笔记

需要准备好 libreoffice 的源代码，并将其编译完毕

## 记录自定义操作

可以在根目录下运行如下命令记录下自己在 libreoffice UI 中的操作

```shell
LO_COLLECT_UIINFO="test.log" SAL_USE_VCLPLUGIN=gen instdir/program/soffice
```

查看`instdir/uitest/test.log`文件可以获得刚才操作的记录，注意，重复运行该命令，`test.log`不会被覆写，所以如果需要重复生成，则需要删掉原有的。在 writer 中插入一个表格所产生的日志[如链接所示](https://gist.github.com/Sakura286/fd123c4495aa718693f0ac32fbd81085)，将其写成的对应的 python 文件[如链接所示](https://gist.github.com/Sakura286/783a0ca4a49f9c6642f4e40f5e68f71f)

## 运行测试（外部）

运行该脚本

```shell
export SRCDIR=<path_to_libreoffice_source_code>
export PYTHONPATH=$SRCDIR/instdir/program
export PYTHONPATH=$PYTHONPATH:$SRCDIR/unotest/source/python
export URE_BOOTSTRAP=file://$SRCDIR/instdir/program/fundamentalrc
export SAL_USE_VCLPLUGIN=gen
export TDOC=$SRCDIR/sw/qa/uitest/data
export TestUserDir=file:///tmp 
export LC_ALL=C

rm -rf /tmp/libreoffice/4

python3 "$SRCDIR/uitest/test_main.py" --soffice=path:"$SRCDIR/instdir/program/soffice" --userdir=file:///tmp/libreoffice/4 --file=<path_of_python_file>
```

注意替换尖括号里的内容

## 运行测试（内部）

最简单的运行 UITest 的方法是`make check uickeck`，但是这会把所有的 UITest 运行一遍，我们只需要直接运行单个的 UITest

对于已存在于源代码中的 UITest，可以使用如下命令进行测试

```shell
cd sw
make -srj1 UITest_<module> UITEST_TEST_NAME="<py_file>.<class_name>.<def_name>"
```

我们以命令`make -srj1 UITest_sw_table UITEST_TEST_NAME="sheetToTable.sheetToTable.test_sheet_to_table_without_hidden_rows"` 为例，

`<module>`指明了要测试的模组名，对于上面这个例子来说，那么模组名`sw_table`就是`sw`文件夹下的`UITest_sw_table.mk`，该`.mk`中指定了一个叫做`table`的文件夹，该文件夹的路径是`sw/qa/uitest/table`

`<py_file>` `<class_name>` `<def_name>`分别指明了要测试的 python 文件名、python 文件中的类名、类中的方法名，文件名、类名、方法名不必一致

如果要新增一个测试模块，应当在`sw`文件夹下新增对应的`UITest_<module_name>.mk`文件，然后在`Module_sw.mk`文件中添加该模块，然后在`sw/qa/uitest`目录下添加对应的文件目录，并放入 python 文件

## 写测试时需要注意的问题

### 初始化新窗口与关闭

以刚才“打开writer插入表格后退出”的测试为例

第一版（[LibreOffice 官方教程中的示例代码](https://www.youtube.com/watch?v=khN0kNi9b98)）

```python
def test_insertTable(self):
    self.ui_test.create_doc_in_start_center("writer"):

    self.ui_test.execute_dialog_through_command(".uno:InsertTable")
    xDialog = self.xUITest.getTopFocusWindow()

    xNameEdit = xDialog.getChild("nameedit")
    self.assertEqual("Table1", get_state_as_dict(xNameEdit)['Text'])

    xNameEdit.executeAction("TYPE", mkPropertyValues({"KEYCODE":"CTRL+A"}))
    xNameEdit.executeAction("TYPE", mkPropertyValues({"KEYCODE":"MyTable"}))
    
    xOkBtn = xDialog.getChild("ok")
    self.ui_test.close_dialog_through_button(xOkBtn)

    document = self.ui_test.get_component()

    self.assertEqual(1, len(document.TextTables))
    self.assertEqual("MyTable", document.TextTables[0].TableName)

    self.ui_test.close_doc()
```

第二版

```python
def test_insertTable(self):
    with self.ui_test.create_doc_in_start_center("writer") as document:
        with self.ui_test.execute_dialog_through_command(".uno:InsertTable") as xDialog:
            xNameEdit = xDialog.getChild("nameedit")
            self.assertEqual("Table1", get_state_as_dict(xNameEdit)['Text'])
            xNameEdit.executeAction("TYPE", mkPropertyValues({"KEYCODE":"CTRL+A"}))
            xNameEdit.executeAction("TYPE", mkPropertyValues({"KEYCODE":"MyTable"}))
        self.assertEqual(1, len(document.TextTables))
        self.assertEqual("MyTable", document.TextTables[0].TableName)
```

第一版（官方版）的代码可能比较老旧，新窗口是无法创建的，导致后面的一系列操作都变成了非法操作。
根据现在的源代码，关闭文档、关闭窗口的命令不再手动编写，而是直接使用 python 的 with as 处理。

自动生成版

```python
def test_function(self):
    with self.ui_test.create_doc_in_start_center("writer") as document:
        MainWindow = self.xUITest.getTopFocusWindow()
        self.xUITest.executeCommand(".uno:UpdateInputFields")
            btnOk = TipOfTheDayDialog.getChild("btnOk")
            self.ui_test.close_dialog_through_button(btnOk)
        self.xUITest.executeCommand(".uno:InsertTable")
            nameedit = InsertTableDialog.getChild("nameedit")
        nameedit.executeAction("SELECT", mkPropertyValues({"FROM": "6", "TO": "5"}))
        nameedit.executeAction("SELECT", mkPropertyValues({"FROM": "6", "TO": "4"}))
        nameedit.executeAction("SELECT", mkPropertyValues({"FROM": "6", "TO": "2"}))
        nameedit.executeAction("SELECT", mkPropertyValues({"FROM": "6", "TO": "1"}))
        nameedit.executeAction("SELECT", mkPropertyValues({"FROM": "6", "TO": "0"}))
            nameedit.executeAction("TYPE", mkPropertyValues({"KEYCODE": "SHIFT+M"}))
            nameedit.executeAction("TYPE", mkPropertyValues({"KEYCODE": "SHIFT+Y"}))
            nameedit.executeAction("TYPE", mkPropertyValues({"KEYCODE": "SHIFT+F"}))
            nameedit.executeAction("TYPE", mkPropertyValues({"KEYCODE": "SHIFT+A"}))
            nameedit.executeAction("TYPE", mkPropertyValues({"KEYCODE": "SHIFT+U"}))
            nameedit.executeAction("TYPE", mkPropertyValues({"KEYCODE": "SHIFT+L"}))
            nameedit.executeAction("TYPE", mkPropertyValues({"KEYCODE": "SHIFT+T"}))
            ok = InsertTableDialog.getChild("ok")
            self.ui_test.close_dialog_through_button(ok)
```

**MARK**：这个脚本使用后，程序卡在插入表格对话框处

参考链接：

1. [Development/UITests - The Document Foundation Wiki](https://wiki.documentfoundation.org/Development/UITests)
2. [LibreOffice QA - how to write your first test](https://archive.fosdem.org/2021/schedule/event/lo_qualityassurance/)
3. [Things you can test in a UITest](https://archive.fosdem.org/2022/schedule/event/lotech_somethingaboutqa/)
4. [Development/DispatchCommands - The Document Foundation Wiki](https://wiki.documentfoundation.org/Development/DispatchCommands)
5. [UITest Service Reference](https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1ui_1_1test_1_1UITest.html)
6. [Writing a LibreOffice Calc UI test](https://mmohrhard.wordpress.com/2016/09/10/writing-a-libreoffice-calc-ui-test/)
7. [UITest_demo_ui.mk](https://git.libreoffice.org/core/+/refs/heads/master/uitest/UITest_demo_ui.mk)
