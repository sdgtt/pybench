from bench import keysight


def test_e36233a_auto():
    ps = keysight.E36233A()
    # Read all properties from all channels
    for chan in ps.channels():
        print(f"Channel {chan.channel_number}:")
        print(f"Voltage: {chan.voltage}")
        print(f"Current: {chan.current}")
        print(f"Output Enabled: {chan.output_enabled}")
        print(f"Operational Mode: {chan.operational_mode}")
