#!/usr/bin/env python3
"""SIMULATION/REFERENCE ONLY. Small educational UI; not a T510 host application."""

import tempfile
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from rfsoc8_ref.config import SimulationConfig
from rfsoc8_ref.pipeline import run_reference_pipeline


class ReferenceUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("八通道 UCA / MUSIC 算法验证")
        self.geometry("650x360")
        ttk.Label(
            self,
            text="当前模式：软件仿真（未接入 ANTSDR T510 实板）",
            foreground="#b00020",
            font=("Microsoft YaHei UI", 12, "bold"),
        ).pack(pady=14)

        form = ttk.Frame(self)
        form.pack(fill="x", padx=28)
        self.az = self._row(form, 0, "合成方位角 (deg)", "35")
        self.el = self._row(form, 1, "合成俯仰角 (deg)", "15")
        self.snr = self._row(form, 2, "信噪比 (dB)", "15")
        self.out = self._row(form, 3, "输出目录", str(Path.cwd() / "ui_demo"), width=45)
        ttk.Button(self, text="运行软件仿真", command=self.run_simulation).pack(pady=20)
        self.status = ttk.Label(self, text="等待运行")
        self.status.pack()

    @staticmethod
    def _row(parent, row, label, default, width=18):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=7)
        var = tk.StringVar(value=default)
        ttk.Entry(parent, textvariable=var, width=width).grid(row=row, column=1, sticky="w")
        return var

    def run_simulation(self) -> None:
        try:
            cfg = SimulationConfig(
                source_az_deg=float(self.az.get()),
                source_el_deg=float(self.el.get()),
                snr_db=float(self.snr.get()),
            )
            result = run_reference_pipeline(cfg, Path(self.out.get()))
            text = (
                f"软件仿真完成：MUSIC 方位 {result['estimated_az_deg']:.1f}°，"
                f"俯仰 {result['estimated_el_deg']:.1f}°"
            )
            self.status.configure(text=text)
            messagebox.showinfo("运行完成", text + "\n当前结果为软件仿真数据。")
        except Exception as exc:  # UI boundary: show input/runtime errors to learner.
            messagebox.showerror("运行失败", str(exc))


if __name__ == "__main__":
    ReferenceUI().mainloop()

