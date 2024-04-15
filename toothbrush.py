import json
import sys
from datetime import datetime

# The current date
today: str = (str)(datetime.now().date())

# Command-line arguments
cliArgs: list[int] = sys.argv[1:]

# Add the time to the toothbrush data
def storeTime(time: int) -> None:

    # Read the data file
    print("Loading existing data...", end="")
    brushData: dict = json.load(open("toothbrush.json", "r"))
    if not brushData:
        print("Failed to load data!")
        return
    print("Success!")

    # Check for existing daily data
    if today in brushData.keys():
        print(f"Updating entry for date: {today}")
        brushData[today]['brush_count'] += 1
        brushData[today]['brush_time_minutes'].append(time)
    else:
        print(f"Creating new entry for date: {today}")
        brushData[today] = {
            'brush_count': 1,
            'brush_time_minutes': [time],
            'historic_brush_time_minutes': 0,
            'historic_brush_count': 0
        }

    # Calculate new historic values
    time_historic: int = 0
    count_historic: int = 0
    total_days: int = len(brushData)
    for day in brushData:
        count_historic += brushData[day]['brush_count']
        for brushTime in brushData[day]['brush_time_minutes']:
            time_historic += brushTime/brushData[today]['brush_count']

    # Write historic values to our data
    brushData[today]['historic_brush_time_minutes'] = time_historic/total_days
    brushData[today]['historic_brush_count'] = count_historic/total_days

    # Write changes back to the data file
    print("Writing changes...", end="")
    json.dump(brushData, open("toothbrush.json", "w"), indent=4)
    print("Success!")


# Check cli arguments and display error text as needed
def main():
    if (len(cliArgs) == 0):
        print("*** No command specified, run -h for information ***")
        return
    elif cliArgs[0] == "--store" and len(cliArgs) > 1:
        storeTime((int)(cliArgs[1]))
    elif cliArgs[0] == "-h":
        print("\nCommand List:")
        print("\t--store [TIME_MINUTES]: store brush time\n")
    else:
        print("*** Unknown Command, run -h for information ***")
        return

# Run main when called
if __name__ == "__main__":
    main()
