# PL 端参考工程

本目录包含与器件无关的 SystemVerilog 模块和仿真文件，可用于建立算法数据通路基线。

已实现：

- 16 位 Q1.15 复数乘法；
- 八通道复数加权求和；
- 16 点查表式 CW DDS；
- 可参数化复数 FIR；
- 顶层流接口和波束形成 Testbench。

`build_reference_project.tcl` 可以建立普通 Vivado RTL 工程。运行前需要通过环境变量
`FPGA_PART` 指定合法器件型号。

本目录没有生成 RF Data Converter IP，也没有 T510 板级约束。需要实板资料后补充：

- `constraints/`：板级 XDC；
- `bd/`：Zynq MPSoC、RFDC、时钟、复位及 AXI Block Design；
- `ip/`：RFDC、FFT、DMA 等 IP 配置；
- 顶层：将 RFDC AXI-Stream 接入 `reference_array_pipeline`。

