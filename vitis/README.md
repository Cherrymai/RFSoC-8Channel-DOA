# PS 端参考程序

`src/` 提供与平台无关的数据采集接口和一个可在普通 C 编译器下运行的模拟后端。
它用于固定 PL/PS 数据结构及调用顺序。

接入 T510 时，需要用 Vitis 2022.2 创建真实平台工程，并将 `mock_platform.c` 替换为
基于 `XRFdc`、MTS 和 DMA 的板级实现。当前目录没有伪造这些驱动调用。

普通 GCC 验证示例：

```text
gcc -std=c11 -O2 src/main.c src/mock_platform.c -lm -o reference_ps
```

