
# LibreOffice 性能测试

## 概述

基于 UITest 技术对 LibreOffice 进行性能测试，本测试在 Linux 平台的不同架构上通用。

本测试模拟了对 Writer 及 Calc 的日常使用，并测试了 Calc 在重负载下的性能表现。为减少结果的随机性，本测试会尽量运行某些易于复现的操作，并对其取平均值/加和。

本测试的结构仿照了 [PCMark10](https://support.benchmarks.ul.com/support/solutions/folders/44001220280) 在 Windows 下使用 AutoIt3 对 LibreOffice 的测试。

本测试在处理对象的选择及测试方式上也参照了基于 VBA 的 [sheetperf 项目](https://github.com/dataspread/spreadsheet-benchmark)。

## Writer

### 测试过程

1. 载入文档 1
2. 复制文档 1 中约 3 页的内容[1]
3. 载入文档 2
4. 将文档 2 另存为新文件
5. 将复制的内容粘贴进文档 2 [2]
6. 保存文档 2
7. 将本地硬盘中的图片插入到文档 2
8. 保存文档 2
9. 输入文本
10. 保存文档 2
11. 导出 PDF
12. 关闭文档

本测试记录了以下操作的时间

#### 载入文档

第一次加载文档的时间，还包括了打开 LibreOffice 的时间，所以单纯统计两次加载的平均值意义不大。

但由于“打开 LibreOffice”往往是日常操作的第一步，所以依然需要统计这个时间

load_doc = sum(T_1, T_2)

T_1 = T_load_witer_doc_1
T_2 = T_load_writer_doc_2

#### 保存文档

由于采用 docx 存档中途会弹框提醒 msdoc 的版本问题，这个对话框难以获取与关闭，所以使用了 LibreOffice Writer 默认的 odt 文档格式

save_doc = geomean(T_3, T_4, T,5, T_6)

T_3 = T_writer_doc_save_as
T_4 = T_writer_doc_save_1
T_5 = T_writer_doc_save_2
T_6 = T_writer_doc_save_3

#### 粘贴内容

粘贴的操作时间较快，所以取加和的效果更显著

copy_paste = sum(T_7, ..., T_14)

T_7 = T_writer_doc_paste_1
...
T_14 = T_writer_doc_paste_8

#### 插入图片

insert_image = geomean(T_15, T_16, T_17, T_18)

T_15 = T_writer_doc_insert_img_1
T_16 = T_writer_doc_insert_img_2
T_17 = T_writer_doc_insert_img_3
T_18 = T_writer_doc_insert_img_4

#### 导出 pdf

export_pdf = geomean(T_19, T,20, T_21, T_22, T_23)

T_19 = T_writer_doc_export_pdf_1
T_20 = T_writer_doc_export_pdf_2
T_21 = T_writer_doc_export_pdf_3
T_22 = T_writer_doc_export_pdf_4
T_23 = T_writer_doc_export_pdf_5

### 结果汇总

典型值测试环境：

CPU:    i5-4200H
内存:   16G
OS:     Debian Bookworm
Libreoffice ver: 7.5.2

|项目|典型值(s)|备注|
|---|---|---|
|load_doc||
|save_doc||
|copy_paste||
|insert_image||
|export_pdf||

## Calc - 日常使用测试

## Calc - 高负载测试

本测试加载了两个大型 Excel 文档，文档中包含数万行数据，以及包含乘积运算、平均值等在内的十万个以上的公式，记录重新计算其中所有单元格所需的时间

### 测试过程

1. 载入 BuildingDesign.xls
2. 重新计算所有单元格
3. 载入 StocksPrice_time_correlation.xls
4. 重新计算所有单元格

对于每个表格文档，重复计算 5 次，取平均值

### 结果汇总

由于 opencl 对于大量公式计算的过程有显著加速，所以还应当记录开启 opencl 加速的测试

|项目|典型值|典型值(with opencl)|备注|
|---|---|---|---|
|build_design|||
|stocks_price|||
