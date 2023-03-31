
# LibreOffice UITest 笔记

需要准备好 libreoffice 的源代码，并将其编译完毕

## 一个简单的例子

接下来将试着用 UITest 写一个用例，该用例将打开一个空白文档，插入一个名为`TestTable`的表格后关闭退出。

### 1. 录制自己的操作

```shell
LO_COLLECT_UIINFO="test.log" SAL_USE_VCLPLUGIN=gen instdir/program/soffice
```

在源代码根目录下执行上面的命令后，LibreOffice 会打开自己的首页，接下来我们对 LibreOffice 的绝大部分交互都会被记录在`instdir/uitest/test.log`中。

在上面的命令里，`LO_COLLECT_UIINFO`指定了生成 log 的名字，`SAL_USE_VCLPLUGIN`指定了使用什么样的 VCL 插件运行 UI，有`gen` `gtk3` `kf5`[三个值可供选用](https://wiki.archlinux.org/title/LibreOffice#Theme)

重复运行命令，`test.log`不会被覆写，所以第二次使用的时候，需要删掉原来的`test.log`，或者指定一个新的名字。

在这个例子中，产生的日志[如链接所示](https://gist.github.com/Sakura286/fd123c4495aa718693f0ac32fbd81085)，将其写成的对应的 python 文件[如链接所示](https://gist.github.com/Sakura286/783a0ca4a49f9c6642f4e40f5e68f71f)

### 2. 将操作日志转化为 python 测试脚本

```shell
cd uitest/ui_logger_dsl
PYTHONPATH=<path_of_src>/instdir/program/ URE_BOOTSTRAP=file:///<path_of_src>/instdir/program/fundamentalrc python dsl_core.py <path_to_log_file> <path_to_a_new_python_file>
```

上面的命令调用了 ui_logger_dsl 将上一步操作录制的操作转换为对应的 python 脚本，python 可能需要安装 testX 库，注意替换掉尖括号里的内容。

这个工具需要维护了，有一些指令不识别，会产生大量的错误，请在错误输出的最后一段找到报错的行，并在`test.log`中删掉。在这个例子中，无报错的的`test.log`是这样的：

```log
Start writer
Send UNO Command (".uno:UpdateInputFields") 
Send UNO Command (".uno:InsertTable") 
Open Modal InsertTableDialog
Select in 'nameedit' {"FROM": "6", "TO": "4"} from InsertTableDialog
Select in 'nameedit' {"FROM": "6", "TO": "3"} from InsertTableDialog
Select in 'nameedit' {"FROM": "6", "TO": "1"} from InsertTableDialog
Select in 'nameedit' {"FROM": "6", "TO": "0"} from InsertTableDialog
Type on 'nameedit' {"KEYCODE": "SHIFT+T"} from InsertTableDialog
Type on 'nameedit' {"TEXT": "e"} from InsertTableDialog
Type on 'nameedit' {"TEXT": "s"} from InsertTableDialog
Type on 'nameedit' {"TEXT": "t"} from InsertTableDialog
Type on 'nameedit' {"KEYCODE": "SHIFT+T"} from InsertTableDialog
Type on 'nameedit' {"TEXT": "a"} from InsertTableDialog
Type on 'nameedit' {"TEXT": "b"} from InsertTableDialog
Type on 'nameedit' {"TEXT": "l"} from InsertTableDialog
Type on 'nameedit' {"TEXT": "e"} from InsertTableDialog
Click on 'ok' from InsertTableDialog
Create Table with  Columns : 2 , Rows : 2 
Close Dialog
Open Modal QuerySaveDialog
Click on 'discard' from QuerySaveDialog
Close Dialog
```

生成的 python 文件是这样的：

```python
from uitest.framework import UITestCase
from libreoffice.uno.propertyvalue import mkPropertyValues
from uitest.uihelper.common import get_state_as_dict
import importlib

class TestClass(UITestCase):
    def test_function(self):
        with self.ui_test.create_doc_in_start_center("writer") as document:
            MainWindow = self.xUITest.getTopFocusWindow()
            self.xUITest.executeCommand(".uno:UpdateInputFields")
                btnOk = TipOfTheDayDialog.getChild("btnOk")
                self.ui_test.close_dialog_through_button(btnOk)
            self.xUITest.executeCommand(".uno:InsertTable")
                nameedit = InsertTableDialog.getChild("nameedit")
            nameedit.executeAction("SELECT", mkPropertyValues({"FROM": "6", "TO": "4"}))
            nameedit.executeAction("SELECT", mkPropertyValues({"FROM": "6", "TO": "3"}))
            nameedit.executeAction("SELECT", mkPropertyValues({"FROM": "6", "TO": "1"}))
            nameedit.executeAction("SELECT", mkPropertyValues({"FROM": "6", "TO": "0"}))
                nameedit.executeAction("TYPE", mkPropertyValues({"KEYCODE": "SHIFT+T"}))
                nameedit.executeAction("TYPE", mkPropertyValues({"TEXT": "e"}))
                nameedit.executeAction("TYPE", mkPropertyValues({"TEXT": "s"}))
                nameedit.executeAction("TYPE", mkPropertyValues({"TEXT": "t"}))
                nameedit.executeAction("TYPE", mkPropertyValues({"KEYCODE": "SHIFT+T"}))
                nameedit.executeAction("TYPE", mkPropertyValues({"TEXT": "a"}))
                nameedit.executeAction("TYPE", mkPropertyValues({"TEXT": "b"}))
                nameedit.executeAction("TYPE", mkPropertyValues({"TEXT": "l"}))
                nameedit.executeAction("TYPE", mkPropertyValues({"TEXT": "e"}))
                ok = InsertTableDialog.getChild("ok")
                self.ui_test.close_dialog_through_button(ok)
```

ui_logger_dsl 生成的代码只能说是“草稿”，距离“能用”还差很远，上面的代码整理生能用的并且添加检测的 assert 语句后是这样的：

```python
from uitest.framework import UITestCase
from libreoffice.uno.propertyvalue import mkPropertyValues
from uitest.uihelper.common import get_state_as_dict

class TestClass(UITestCase):
    def test_insertTable(self):
        with self.ui_test.create_doc_in_start_center("writer") as document:
            with self.ui_test.execute_dialog_through_command(".uno:InsertTable") as xDialog:
                xNameEdit = xDialog.getChild("nameedit")
                self.assertEqual("Table1", get_state_as_dict(xNameEdit)['Text'])
                xNameEdit.executeAction("SELECT", mkPropertyValues({"FROM": "6", "TO": "4"}))
                xNameEdit.executeAction("SELECT", mkPropertyValues({"FROM": "6", "TO": "3"}))
                xNameEdit.executeAction("SELECT", mkPropertyValues({"FROM": "6", "TO": "1"}))
                xNameEdit.executeAction("SELECT", mkPropertyValues({"FROM": "6", "TO": "0"}))
                xNameEdit.executeAction("TYPE", mkPropertyValues({"KEYCODE": "SHIFT+T"}))
                xNameEdit.executeAction("TYPE", mkPropertyValues({"TEXT": "e"}))
                xNameEdit.executeAction("TYPE", mkPropertyValues({"TEXT": "s"}))
                xNameEdit.executeAction("TYPE", mkPropertyValues({"TEXT": "t"}))
                xNameEdit.executeAction("TYPE", mkPropertyValues({"KEYCODE": "SHIFT+T"}))
                xNameEdit.executeAction("TYPE", mkPropertyValues({"TEXT": "a"}))
                xNameEdit.executeAction("TYPE", mkPropertyValues({"TEXT": "b"}))
                xNameEdit.executeAction("TYPE", mkPropertyValues({"TEXT": "l"}))
                xNameEdit.executeAction("TYPE", mkPropertyValues({"TEXT": "e"}))
            self.assertEqual(1, len(document.TextTables))
            self.assertEqual("TestTable", document.TextTables[0].TableName)
```

至于要做哪些修改，请参见[修改草稿](#修改草稿)

### 3. 执行测试

#### 运行测试（外部）

运行该脚本

```shell
export SRCDIR=<path_to_libreoffice_source_code>
export PYTHONPATH=$SRCDIR/instdir/program
export PYTHONPATH=$PYTHONPATH:$SRCDIR/unotest/source/python
export URE_BOOTSTRAP=file://$SRCDIR/instdir/program/fundamentalrc
export SAL_USE_VCLPLUGIN=gen
export TDOC=<data_path>
export TestUserDir=file:///tmp 
export LC_ALL=C

rm -rf /tmp/libreoffice/4

python3 "$SRCDIR/uitest/test_main.py" --soffice=path:"$SRCDIR/instdir/program/soffice" --userdir=file:///tmp/libreoffice/4 --file=<path_of_python_file>
```

注意替换尖括号里的内容，其中`TDOC`应该是 [Transient Document](https://www.openoffice.org/api/docs/common/ref/com/sun/star/ucb/TransientDocumentsContentProvider.html) (过渡文件)的意思，测试用的文档及测试输出的文档都会放在该文件夹内，默认该路径为`$SRCDIR/sw/qa/uitest/data`

#### 运行测试（内部）

最简单的运行 UITest 的方法是`make check uickeck`，但是这会把所有的 UITest 运行一遍，我们只需要直接运行单个的 UITest

对于已存在于源代码中的 UITest ，可以使用如下命令进行测试

```shell
export SAL_USE_VCLPLUGIN=gen
cd sw
make -srj1 UITest_<module_name> UITEST_TEST_NAME="<py_file>.<class_name>.<def_name>"
```

其中`sw`指的是 LibreOffice writer 的文件夹，另外，`sc`指的是 Calc 的文件夹，其他请查阅[LibreOffice Modules](https://docs.libreoffice.org/)

我们以命令`make -srj1 UITest_sw_table UITEST_TEST_NAME="sheetToTable.sheetToTable.test_sheet_to_table_without_hidden_rows"` 为例，

`<module_name>`指明了要测试的模组名，对于上面这个例子来说，那么模组名`sw_table`源自`sw`文件夹下的`UITest_sw_table.mk`，该`.mk`中指定了一个叫做`table`的文件夹，该文件夹的路径是`sw/qa/uitest/table`

`<py_file>` `<class_name>` `<def_name>`分别指明了要测试的 python 文件名、python 文件中的类名、类中的方法名。文件名、类名、方法名不必一致。

生成的日志在`workdir/UITest/<module>`文件夹下。

##### 新增测试模块

如果要新增一个测试模块，应当在`sw`文件夹下新增对应的`UITest_<module_name>.mk`文件，然后在`Module_sw.mk`文件中添加该模块(`<module_name>`)，之后在`sw/qa/uitest`目录下添加对应的文件目录(`<module_name>`)，并放入 python 文件(`<py_file>`)

至此，一个基本的 UITest 便糊出来了。

## 修改草稿

自动生成的 python 脚本是无法运行的，需要经过一定的修改，首先解决对齐问题，并把无用的 importlib 去掉。

```python
from uitest.framework import UITestCase
from libreoffice.uno.propertyvalue import mkPropertyValues
from uitest.uihelper.common import get_state_as_dict

class TestClass(UITestCase):
    def test_function(self):
        with self.ui_test.create_doc_in_start_center("writer") as document:
            MainWindow = self.xUITest.getTopFocusWindow()
            self.xUITest.executeCommand(".uno:UpdateInputFields")
            self.xUITest.executeCommand(".uno:InsertTable")
            nameedit = InsertTableDialog.getChild("nameedit")
            nameedit.executeAction("SELECT", mkPropertyValues({"FROM": "6", "TO": "4"}))
            nameedit.executeAction("SELECT", mkPropertyValues({"FROM": "6", "TO": "3"}))
            nameedit.executeAction("SELECT", mkPropertyValues({"FROM": "6", "TO": "1"}))
            nameedit.executeAction("SELECT", mkPropertyValues({"FROM": "6", "TO": "0"}))
            nameedit.executeAction("TYPE", mkPropertyValues({"KEYCODE": "SHIFT+T"}))
            nameedit.executeAction("TYPE", mkPropertyValues({"TEXT": "e"}))
            nameedit.executeAction("TYPE", mkPropertyValues({"TEXT": "s"}))
            nameedit.executeAction("TYPE", mkPropertyValues({"TEXT": "t"}))
            nameedit.executeAction("TYPE", mkPropertyValues({"KEYCODE": "SHIFT+T"}))
            nameedit.executeAction("TYPE", mkPropertyValues({"TEXT": "a"}))
            nameedit.executeAction("TYPE", mkPropertyValues({"TEXT": "b"}))
            nameedit.executeAction("TYPE", mkPropertyValues({"TEXT": "l"}))
            nameedit.executeAction("TYPE", mkPropertyValues({"TEXT": "e"}))
            ok = InsertTableDialog.getChild("ok")
            self.ui_test.close_dialog_through_button(ok)
```

执行上面的代码，程序会卡在了对话框的部分，文本框里的内容没有被选中，那么有可能插入表格的对话框生成时出了问题，在其他 UITest 中查找生成表格的 UNO 命令`.uno:InsertTable`，会发现有两种用法

第一种：

```python
with self.ui_test.execute_dialog_through_command(".uno:InsertTable") as xDialog:
```

第二种：

```python
self.xUITest.executeCommand(".uno:InsertTable?Columns:short=2&Rows:short=2")
```

第一种使用了`execute_dialog_through_command`方法，并将返回的窗体赋值给了 xDialog 命令，窗体的销毁是直接通过 with as 实现的；
第二种使用了`executeCommand`方法， UNO 命令中附带了参数，并没有查看到后面窗体销毁的命令，所以判断这可能是一种类似于命令行的方式在后台执行的代码

由于我们实际上是需要打开窗体模拟输入的，所以应当将这个改写成第一种写法，并且由于第一种写法会自动销毁窗体，所以不需要最后两行的点击“ok”的操作

修改后的代码如下（省略了 import 和 class 部分）：

```python
def test_function(self):
    with self.ui_test.create_doc_in_start_center("writer") as document:
        MainWindow = self.xUITest.getTopFocusWindow()
        self.xUITest.executeCommand(".uno:UpdateInputFields")
        with self.ui_test.execute_dialog_through_command(".uno:InsertTable") as InsertTableDialog:
            nameedit = InsertTableDialog.getChild("nameedit")
            nameedit.executeAction("SELECT", mkPropertyValues({"FROM": "6", "TO": "4"}))
            nameedit.executeAction("SELECT", mkPropertyValues({"FROM": "6", "TO": "3"}))
            nameedit.executeAction("SELECT", mkPropertyValues({"FROM": "6", "TO": "1"}))
            nameedit.executeAction("SELECT", mkPropertyValues({"FROM": "6", "TO": "0"}))
            nameedit.executeAction("TYPE", mkPropertyValues({"KEYCODE": "SHIFT+T"}))
            nameedit.executeAction("TYPE", mkPropertyValues({"TEXT": "e"}))
            nameedit.executeAction("TYPE", mkPropertyValues({"TEXT": "s"}))
            nameedit.executeAction("TYPE", mkPropertyValues({"TEXT": "t"}))
            nameedit.executeAction("TYPE", mkPropertyValues({"KEYCODE": "SHIFT+T"}))
            nameedit.executeAction("TYPE", mkPropertyValues({"TEXT": "a"}))
            nameedit.executeAction("TYPE", mkPropertyValues({"TEXT": "b"}))
            nameedit.executeAction("TYPE", mkPropertyValues({"TEXT": "l"}))
            nameedit.executeAction("TYPE", mkPropertyValues({"TEXT": "e"}))
```

如果我们希望功能正常的话，应当设置一些 assert 语句来检查表格是否正常生成。

## 参考链接

1. [Development/UITests - The Document Foundation Wiki](https://wiki.documentfoundation.org/Development/UITests)
1. [LibreOffice QA - how to write your first test](https://archive.fosdem.org/2021/schedule/event/lo_qualityassurance/)
1. [Things you can test in a UITest](https://archive.fosdem.org/2022/schedule/event/lotech_somethingaboutqa/)
1. [Development/DispatchCommands - The Document Foundation Wiki](https://wiki.documentfoundation.org/Development/DispatchCommands)
1. [UITest Service Reference](https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1ui_1_1test_1_1UITest.html)
1. [Writing a LibreOffice Calc UI test](https://mmohrhard.wordpress.com/2016/09/10/writing-a-libreoffice-calc-ui-test/)
1. [UITest_demo_ui.mk](https://git.libreoffice.org/core/+/refs/heads/master/uitest/UITest_demo_ui.mk)
