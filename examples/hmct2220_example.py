import bench.hittite as hittite

# Connect to the device
sg = hittite.HMCT2220()

print("\n\nConnected to Hittite HMCT2220\n\n")

# Print the IDN
print(sg._instr.query("*IDN?"))

print(sg.frequency)

sg.power_level_dBm = -50
print(sg.power_level_dBm)

sg.output_enabled = True
print(sg.output_enabled)
sg.output_enabled = False
