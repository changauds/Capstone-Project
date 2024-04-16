match activeBrushing:
    case True:
        # Stop the timer, get timer value
        # Convert value to minutes (as a float)
        # call toothbrush --store [time]
        # set activeBrushing to false
        # delay
        # run toothbrush --show

    case False:
        # switch activeBrushing to True
        # start timer

    case other:
        print("Error")
