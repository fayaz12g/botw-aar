
def create_visuals(do_graphics_increase, do_120fps, do_60fps):

    graphics = "disabled"
    fps60 = "disabled"
    fps120 = "disabled"

    do_island = False
    
    visual_fixes = []

    if do_graphics_increase:
        graphics = "enabled"
    if do_60fps:
        fps60 = "enabled"
    if do_120fps:
        fps120 = "enabled"
        
    visuals1_0_1 = f'''// 1920x1080 Internal Resolution
@{graphics}
00605de4 01F08052
00605de8 02878052
0062c798 01F08052
0062c79c 02878052
00959dac 01F08052
00959db0 02878052
005f17fc 02F08052
005f1800 03878052
005f1858 02F08052
005f185c 03878052
005f18b4 02F08052
005f18b8 03878052
005bf4a4 09878052
005bf4a8 08F08052
005bf63c 09878052
005bf640 08F08052
005bf45c 09F08052
005bf468 0A878052
005bf4a4 09878052
005bf4a8 08F08052
005bf578 09F08052
005bf584 0A878052
0081502c 09F08052
0081504c 0A878052
005b984c 08F080D2
@stop

// 60 FPS Mode
@{fps60}
001babdc 35008052
@stop

// 120 FPS Mode (Expiremental)
@{fps120}
0058110c 0310211E
00581120 0310381E
00581138 03102E1E
@stop
'''


    visual_fixes.append(visuals1_0_1)

    
    return visual_fixes