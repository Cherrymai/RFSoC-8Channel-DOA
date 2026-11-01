# Portable RTL reference-project creator.
# This script does not create RFDC/MTS or ANTSDR T510 board configuration.

if {![info exists ::env(FPGA_PART)]} {
    puts stderr "Set FPGA_PART to a valid installed Vivado device part before running."
    exit 2
}

set script_dir [file dirname [file normalize [info script]]]
set project_dir [file join $script_dir build reference_rtl]
create_project -force reference_rtl $project_dir -part $::env(FPGA_PART)

set rtl_files [glob -nocomplain \
    [file join $script_dir rtl common *.sv] \
    [file join $script_dir rtl signal *.sv] \
    [file join $script_dir rtl beamforming *.sv] \
    [file join $script_dir rtl channelizer *.sv] \
    [file join $script_dir rtl top *.sv]]

if {[llength $rtl_files] == 0} {
    puts stderr "No RTL files found."
    exit 3
}

add_files -norecurse $rtl_files
set_property top reference_array_pipeline [current_fileset]
update_compile_order -fileset sources_1

set tb_files [glob -nocomplain [file join $script_dir sim *.sv]]
if {[llength $tb_files] > 0} {
    add_files -fileset sim_1 -norecurse $tb_files
    set_property top tb_beamformer8_q15 [get_filesets sim_1]
    update_compile_order -fileset sim_1
}

puts "Reference RTL project created at: $project_dir"
puts "RFDC, MTS, board clocks, DMA and T510 constraints still require real board integration."

