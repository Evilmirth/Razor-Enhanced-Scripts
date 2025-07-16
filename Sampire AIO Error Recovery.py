while Player.Connected:
    # If you're a ghost, just got into a holding pattern until you're not. 
    if Player.IsGhost:
        Misc.Pause(1000)
        continue
    
    Misc.Pause(1000)
    if not Misc.ScriptRun("Sampire AIO by Smaptastic - edited by Galeamar - auto weapon swapping.py"):
        Misc.ScriptRun("Sampire AIO by Smaptastic - edited by Galeamar - auto weapon swapping.py")
        Misc.Pause(150)