
def create_visuals(do_120fps, do_60fps):

    fps60 = "disabled"
    dynamic = "disabled"

    visual_fixes = []

    if do_60fps:
        fps60 = "enabled"
    if do_120fps:
        dynamic = "enabled"
        
    visuals1_0_1 = f'''// 60 FPS Mode
@{fps60}
01614954 08008052
01614D84 08F08752
01614DB0 20008052
01614DA4 21000012
@disabled

// 120 FPS Mode (Expiremental)
@{dynamic}
0150ABA4 1F2003D5
@stop
'''


    visual_fixes.append(visuals1_0_1)

    
    return visual_fixes