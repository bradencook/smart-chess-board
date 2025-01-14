from machine import Pin
import time

# GPIO pins for MUX control
mux_select_pins = [Pin(3, Pin.OUT), Pin(2, Pin.OUT), Pin(1, Pin.OUT), Pin(0, Pin.OUT)]  # S0, S1, S2, S3
mux_enable_pins = [Pin(4, Pin.OUT), Pin(5, Pin.OUT), Pin(6, Pin.OUT), Pin(7, Pin.OUT)]  # EN0-EN3
signal_pin = Pin(8, Pin.IN, Pin.PULL_UP)  # Shared signal pin for all MUX outputs

def read_mux(mux_index, row):
    """
    Reads all 8 signals for a specific row (even or odd) of the given MUX.
    
    Args:
        mux_index (int): Index of the MUX to enable (0-3).
        row (int): Row to read (0 for even, 1 for odd).

    Returns:
        list: List of 8 signal values (0 or 1).
    """
    # Enable the desired MUX
    for i, pin in enumerate(mux_enable_pins):
        pin.value(1 if i != mux_index else 0)  # Active low enable

    # Read 16 inputs for the selected row
    signals = []
    for i in range(8):
        # Set the select lines (S0, S1, S2, S3)
        select_value = (i << 1) | row  # Shift to select the correct input
        for bit, pin in enumerate(mux_select_pins):
            pin.value((select_value >> bit) & 1)

        # Short delay for stability
        time.sleep_us(10)

        # Read the signal
        signals.append(signal_pin.value())

    return signals

def read_all_signals():
    """
    Reads all 64 signals across 4 MUXes and 2 rows per MUX.

    Returns:
        list: List of 64 signal values (0 or 1).
    """
    all_signals = []
    for mux_index in range(4):
        for row in [1, 0]:  # 0 for even, 1 for odd
            group = read_mux(mux_index, row)
            group.reverse()
            all_signals.extend(group)
       
    return all_signals


