# 上位机与离线分析

根目录的 `run_demo.py`、`run_ui.py` 和 `rfsoc8_ref/` 构成当前上位机及离线算法代码。
`analyze_capture.py` 用于读取八通道 CSV 并执行 MUSIC 扫描。

真实采集文件仍采用以下列名：

```text
sample,ch0_real,ch0_imag,...,ch7_real,ch7_imag
```

接入硬件后应在采集端完成 ADC 码值到归一化 IQ 的转换，并保存采样率、载频、通道
顺序和校准版本。

