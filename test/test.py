# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_priority_encoder(dut):

    dut._log.info("Start")

    clock = Clock(dut.clk, 10, units="us")  
    cocotb.start_soon(clock.start())

    # Reset
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)  
    dut.rst_n.value = 1  

    dut._log.info("Test project behavior")
    
    test_vectors = [
        ((0b00101010, 0b11110001), 13),  
        ((0b00000000, 0b00000001), 0),   
        ((0b00000000, 0b00000000), 240), 
        ((0b10000000, 0b00000000), 15),  
        ((0b00010000, 0b00000000), 12),  
    ]

    for (a, b), expected_out in test_vectors:
        dut.uio_in.value = a  
        dut.ui_in.value = b  
        

        # Wait for one clock cycle to see the output values
        await ClockCycles(dut.clk, 1)  
        output = int(dut.uo_out.value)

        if output == expected_out:
            dut._log.info(f"PASS: A={a:08b}, B={b:08b}, Output={output}, Expected={expected_out}")
        else:
            dut._log.warning(f"FAIL: A={a:08b}, B={b:08b}, Output={output}, Expected={expected_out}")

    dut._log.info("Priority Encoder Test Completed!")
