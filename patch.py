import os
import math
from functions import *

def pmtok_patch(patch_folder, ratio_value, scaling_factor, visual_fixes):

    visual_fixesa = visual_fixes[0]

    scaling_factor = float(scaling_factor)
    ratio_value = float(ratio_value)
    print(f"The scaling factor is {scaling_factor}.")
    hex_value = make_hex(ratio_value, 1)
    hex_value2, hex_value3 = pmtok_hex23(ratio_value)
    version_variables = ["1.0.1"]
    for version_variable in version_variables:
        file_name = f"{version_variable}.pchtxt"
        file_path = os.path.join(patch_folder, file_name)

        if version_variable == "1.0.1":
            nsobidid = "E74395F066FD8CCB51EC17B39B3DA2C8CF520089"
            visual_fix = visual_fixesa
            

        patch_content = f'''@nsobid-{nsobidid}

@flag print_values
@flag offset_shift 0x100

@enabled
002665b8 {hex_value}
0026a2c8 {hex_value2}
0026a2d4 {hex_value3}
@stop

{visual_fix}

// Generated using PMTOK-AAR by Fayaz (github.com/fayaz12g/pmtok-aar)'''
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as patch_file:
            patch_file.write(patch_content)
        print(f"Patch file created: {file_path}")

# This works by doing the following:
# fmov s1, #Rounded_Ratio
# movz w9, #0xe38e
# movk w9, #0x4018, lsl #16
# The last two are the floating point in hex, split with the last 4 then the first 4