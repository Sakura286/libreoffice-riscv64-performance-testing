
# GUI test tools

最近要测试并优化 LibreOffice 在 TH1520 上的性能表现

如果以 PCMark 10 对于生产力工具的测试为基准，那么应当在 GUI 环境下测试，以文档操作为例，PCMark 测试了打开两个文档，在两个文档中进行大面积复制与剪切，调整窗口大小，输入文字，插入图片，保存文档，保存文档等多种操作，那么应当使用什么工具来进行这样的测试呢？

## AutoIt

这是 PCMark 10 测试使用的脚本工具，支持直接与窗口的标准控件进行交互，有详细的中文文档。

理论上 AutoIt 不应该叫做 GUI 自动化工具，只是恰巧支持 GUI 自动化而已。

这个软件仅支持 winshit ，无法支持本次测试的平台， pass 。

## SikuliX1 与 PyAutoGUI

这两个 GUI 自动化工具对于控件的获取都是使用截图元素定位——所以效率极为低下。举个例子，i7-12700kf 打开 libreoffice writer 并关闭共需约 3s 的时间，而单纯的由 PyAutoGUI 在首页识别到 writer 的按钮就需要花费大约 400~500ms 的时间，对于操作时间更短的一些操作，截图元素定位效率低下的问题更为显著。

测试工具消耗了过多的算力，难以反映出真实的性能， pass 。

## Selenium

这是浏览器自动化测试框架，对某些 QT 应用也有支持。

不支持 LibreOffice ， pass 。

## PyWinAuto

对 Win 友好，不少功能 Linux 不支持， pass 。

## Dogtail

使用 a11y 技术与桌面应用进行交互，所以可以通过代码的方式直接获得控件的位置。

然而可能是因为长久的不维护，其 sniff 插件能够嗅探到的控件的信息相当少，无法使用， pass 。

## LibreOffice UITest

这是 LibreOffice 自己的测试框架，软件的 UI 封装在 C++ 库里，然后使用用 python 写的测试代码去调用。

有大量的已有的实例进行参照，并且大体上有活跃的开发者在维护这些实例，所以学习与书写会比较方便。由于控件的获取是以代码指定的方式进行的，免去了截图元素定位所占用的时间，并且能够方便地获取程序当前的状态，执行效率也非常高。

现阶段这种方式有两个问题，一个是不能完全实现 PCMark 10 在 Windows 端上的部分操作，比如同时开两个窗口进行操作、调整窗口的大小等；另一个是由于测试是直接作用于 vcl 控件的，与实际的用户输入仍然隔着一定的层级（所以有人建议使用 Dogtail 补充测试，然而这个建议不了了之了）

要用什么进行测试，显而易见了。

即使是不进行 GUI 方面的测试，LibreOffice 这边自身也有 Cpp Unit Test 以及 Java Unit Test 框架，以及大量的实例。

## 部分参考链接

1. [PCMark 10 - Productivity test group - Writing](https://support.benchmarks.ul.com/support/solutions/articles/44002162316)
1. [PCMark 10 Word test - Benchmarks](https://support.benchmarks.ul.com/support/solutions/articles/44002171213)
1. [Debugged / enhanced UDF Files for Open Office - AutoIt Forum](https://www.autoitscript.com/forum/topic/118280-debugged-enhanced-udf-files-for-open-office/)
1. [Comparison of GUI testing tools - WikiPedia](https://en.wikipedia.org/wiki/Comparison_of_GUI_testing_tools)
1. [gedit-test-utf8-procedural-api.py - Dogtail - Github](https://github.com/vhumpa/dogtail/blob/master/examples/gedit-test-utf8-procedural-api.py)
1. [Automation Test for LibreOffice](https://lists.freedesktop.org/archives/libreoffice/2015-December/071318.html)
1. [Extending subsequent tests with dogtail tests?](https://lists.freedesktop.org/archives/libreoffice/2019-February/082088.html)
1. [LibreOffice UITest Development - Document Foundation Wiki](https://wiki.documentfoundation.org/Development/UITests)
1. [Things you can test in a UITest](https://archive.fosdem.org/2022/schedule/event/lotech_somethingaboutqa/)
1. [LibreOffice QA - how to write your first test](https://archive.fosdem.org/2021/schedule/event/lo_qualityassurance/)
