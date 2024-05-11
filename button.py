import time
import json
import os
import filepath

# Pull button state data from JSON file
buttonData: dict = json.load(open(f"{filepath.path}button_state.json", "r"))
if not buttonData:
    print("Failed to Load Data!")
activeBrushing: str = buttonData["active_brushing"]
start_time: float = (float)(buttonData["start_time"])

# Toggle the toothbrush
os.system("echo 'a' > /dev/rfcomm0")
time.sleep(0.1)

# Update based on state data
if activeBrushing == "True":
    print("Turning off the toothbrush")
    # Get the elapsed time
    brushtime = (time.time() - start_time) / 60
    stopwatch_data = (f"python {filepath.path}toothbrush.py --store ")+(str)(brushtime)
    print("STORING: ", stopwatch_data)
    os.system(stopwatch_data)
    # Take a moment for the toothbrush data to update, then display it to the user
    time.sleep(0.2)
    os.system(f"python {filepath.path}toothbrush.py --show")
    # Set brushing to inactive
    buttonData["active_brushing"] = "False"
else:
    print("Starting the toothbrush timer")
    buttonData["start_time"] = time.time()
    buttonData["active_brushing"] = "True"

# Write button state changes back to JSON
json.dump(buttonData, open(f"{filepath.path}button_state.json", "w"), indent=4)
