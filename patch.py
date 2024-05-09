import os
import math
from functions import *

def BOTW_patch(patch_folder, ratio_value, scaling_factor, visual_fixes):

    visual_fixesa = visual_fixes[0]

    scaling_factor = float(scaling_factor)
    ratio_value = float(ratio_value)
    print(f"The scaling factor is {scaling_factor}.")
    hex_value = make_hex(ratio_value, 0)
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
00e0ad68 {hex_value}
01271870 {hex_value}
015c2148 {hex_value}
@stop

{visual_fix}

// Generated using BOTW-AAR by Fayaz (github.com/fayaz12g/BOTW-aar)'''
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as patch_file:
            patch_file.write(patch_content)
        print(f"Patch file created: {file_path}")

