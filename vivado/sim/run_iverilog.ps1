$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$rtl = @(
    (Join-Path $root 'rtl\beamforming\beamformer8_q15.sv'),
    (Join-Path $PSScriptRoot 'tb_beamformer8_q15.sv')
)
iverilog -g2012 -s tb_beamformer8_q15 -o (Join-Path $PSScriptRoot 'tb_beamformer8.vvp') $rtl
vvp (Join-Path $PSScriptRoot 'tb_beamformer8.vvp')

