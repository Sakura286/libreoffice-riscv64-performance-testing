
# libreoffice-riscv64-performance-testing

Some work of LibreOffice performance testing for riscv64 port, also work for other arch on linux.

## Benchmark

![Alt text](pic/benchmark-230630.svg)

||Unmatched|Lichee Pi 4A|SG 2042|Intel i5-4200H|
|---|---|---|---|---|
|Writer_load_doc|10.419|11.227|6.593|1.862|
|Writer_copy_paste|4.829|3.462|1.762|0.33|
|Writer_insert_image|12.234|8.646|4.017|1.372|
|Writer_save_doc|6.155|4.69|3.214|0.728|
|Writer_export_pdf|50.092|20.381|13.588|3.709|
|Calc_load_BuildingDesign|35.503|23.213|1.387|6.645|
|Calc_load_StocksPriceTimeCorrelation|43.768|21.693|1.462|7.649|



## How to run

1. Before running the script, install and run libreoffice one time to close the everyday-tips.
2. run the commands below:

```shell
git clone --depth=1 git://go.suokunlong.cn/lo/core
git clone --depth=1 https://github.com/Sakura286/libreoffice-riscv-port-memo.git
cd libreoffice-riscv-port-memo

# modify SRC_CODE_DIR to cloned source code
vim run.sh
chmod u+x run.sh
./run.sh
```

## Some memo

Please browse the `doc` folder.
