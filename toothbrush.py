import json
import sys
from datetime import datetime, timedelta
import filepath

# The current date
today: str = (str)(datetime.now().date())

# Command-line arguments
cliArgs: list[int] = sys.argv[1:]


def getStartOfWeek (date: str) -> str:
    """ Finds the first day in the week containing the user-input date.

    Args:
        date (str): string representation of the current date

    Returns:
        start_week (str): Monday of the week containing the input date
    """
    # Convert input to a datetime object
    given_date = datetime.strptime(date, '%Y-%m-%d')

    # Find and return first day of week containing the input date
    start_week =  given_date - timedelta(days=given_date.weekday())
    return (str)(start_week.date())


def calculateWeeklyData () -> None:
    """ Groups daily brush data into weeks and calculates weekly averages.
    Results are written to toothbrush_weekly.json
    """
    # Pull daily brush statistics
    daily_brush_data: dict = json.load(open(f"{filepath.path}toothbrush_daily.json"))
    if not daily_brush_data:
        print("Failed to load data!")
        return

    # This will store the average weekly data
    ave_week: dict = {}

    """ Calculate average for every week
        - iterate through each day's brush data
        - calculate the average brush time for the day
        - finds the start of the week for that day and update weekly brush data in the ave_week
    """
    for day in daily_brush_data.keys():
        info_date = daily_brush_data[day]
        brush_time = info_date['brush_time_minutes']
        brush_count = info_date['brush_count']
        average_brush_time = (sum(brush_time) / len(brush_time))

        # map all days in a week to the first weekday
        firstWeekday: str = getStartOfWeek(day)

        # update the data if is not in the start week in the ave_week dictionary
        if firstWeekday in ave_week.keys():
            ave_week[firstWeekday]['days_brushed'] += 1
            ave_week[firstWeekday]['average_brush_count'] += brush_count
            ave_week[firstWeekday]['average_brush_time'] += average_brush_time
        else:
            ave_week[firstWeekday]: dict[str, int] = {}
            ave_week[firstWeekday]['days_brushed'] = 1
            ave_week[firstWeekday]['average_brush_count'] = brush_count
            ave_week[firstWeekday]['average_brush_time'] = average_brush_time

    # divide brush time/count by days brushed in a week
    for week in ave_week.keys():
        ave_week[week]['average_brush_count'] /= ave_week[week]['days_brushed']
        ave_week[week]['average_brush_time']  /= ave_week[week]['days_brushed']

    json.dump(ave_week, open(f"{filepath.path}toothbrush_weekly.json", "w"), indent=4)


def storeTime(time) -> None:
    """ Store user-input time into daily statistics, then recalculate the
    weekly and global historic averages.

    Args:
        time: duration of brush session
    """

    # Read the data file
    print("Loading existing data...", end="")
    brushData: dict = json.load(open(f"{filepath.path}toothbrush_daily.json", "r"))
    if not brushData:
        print("Failed to load data!")
        return
    print("Success!")

    # Check for existing daily data
    if today in brushData.keys():
        print(f"Updating entry for date: {today}")
        brushData[today]['brush_count'] += 1
        brushData[today]['brush_time_minutes'].append((float)(time))
    else:
        print(f"Creating new entry for date: {today}")
        brushData[today] = {
            'brush_count': 1,
            'brush_time_minutes': [time]
        }

    # Calculate new historic values
    time_historic: int = 0
    count_historic: int = 0
    total_days: int = len(brushData)
    for day in brushData:
        count_historic += brushData[day]['brush_count']
        for brushTime in brushData[day]['brush_time_minutes']:
            time_historic += brushTime/brushData[day]['brush_count']

    # Write historic values to our data
    averageBrushData: dict = json.load(open(f"{filepath.path}toothbrush_average.json", "r"))
    if not averageBrushData:
        print("Failed to load average data!")
        return
    averageBrushData['historic_brush_time_minutes'] = time_historic/total_days
    averageBrushData['historic_brush_count'] = count_historic/total_days

    # Write changes back to the data file
    print("Writing changes...", end="")
    json.dump(brushData, open(f"{filepath.path}toothbrush_daily.json", "w"), indent=4)
    json.dump(averageBrushData, open(f"{filepath.path}toothbrush_average.json", "w"), indent=4)
    print("Success!")

    # Recalculate weekly data as well
    calculateWeeklyData()


def showData() -> None:
    """ Print formatted statistics for the daily brush data.
    If no data is found, alert the user.
    """
    # Read the data file
    brushData: dict = json.load(open(f"{filepath.path}toothbrush_daily.json", "r"))
    averageBrushData: dict = json.load(open(f"{filepath.path}toothbrush_average.json", "r"))
    averageWeekData: dict = json.load(open(f"{filepath.path}toothbrush_weekly.json", "r"))

    if not brushData or not averageBrushData or not averageWeekData:
        print("Failed to load data!")
        return
    # Check for existing daily data
    if today in brushData.keys():
        count: int = brushData[today]['brush_count']
        timeSum: float = 0
        for time in brushData[today]['brush_time_minutes']:
            timeSum += time;
           
        timeSum_sec = (int)(timeSum*60)
        timeSum_min, timeSum_sec = divmod(timeSum_sec, 60)
        timeSum_format = '{:02d}:{:02d}'.format(timeSum_min, timeSum_sec)

        print(f"\nStats for {today}:\n")
        print(f"You brushed {count} time(s) for a total of {timeSum_format}")
        print("\nHere's your daily breakdown:")
        for i in range(len(brushData[today]['brush_time_minutes'])): 
            timeSum_sec = (int)(brushData[today]['brush_time_minutes'][i] * 60)
            timeSum_min, timeSum_sec = divmod(timeSum_sec, 60)
            timeSum_format = '{:02d}:{:02d}'.format(timeSum_min, timeSum_sec)
            print(f"\tBrush {i+1} -> {timeSum_format}")
    else:
        print(f"\nNo brush data for {today}\n")

    # Grab data from most recent week
    if (len(list(averageWeekData.items())) == 0):
        print("\nNo weekly data available\n")
    else:
        # Try and display data for current and previous week
        today_datetime = datetime.strptime(today, '%Y-%m-%d')
        this_week = (str)((today_datetime - timedelta(days=today_datetime.weekday())).date())
        last_week = (str)((today_datetime - timedelta(days=today_datetime.weekday()+7)).date())
        if (this_week in averageWeekData.keys()):
            thisWeekData: dict = averageWeekData[this_week]
            print(f"\nStats for This Week (week of {this_week}):\n\tDays Brushed: {thisWeekData['days_brushed']}\n\tBrushes Per Day: {thisWeekData['average_brush_count']}")
        else:
            print(f"\nNo stats for this week (week of {this_week})\n")
        if (last_week in averageWeekData.keys()):
            lastWeekData: dict = averageWeekData[last_week]
            print(f"\nStats for Last Week (week of {last_week}):\n\tDays Brushed: {lastWeekData['days_brushed']}\n\tBrushes Per Day: {lastWeekData['average_brush_count']}")
        else:
            print(f"\nNo stats for last week (week of {last_week})\n")

    # Display all-time averages
    histCnt: int = averageBrushData['historic_brush_count']
    histTime: int = averageBrushData['historic_brush_time_minutes'] 
    histTime_sec = (int)(histTime*60)
    histTime_min, histTime_sec = divmod(histTime_sec, 60)
    histTime_format = '{:02d}:{:02d}'.format(histTime_min, histTime_sec)
    print(f"\nHistoric Summary:\n\tOn average, you brush {round(histCnt, 3)} times a day for {histTime_format} minutes per brush\n")


def main():
    """ Handle Command-Line arguments and run appropriate functions """
    if (len(cliArgs) == 0 or cliArgs[0] == "-h" or cliArgs[0] == "--help"):
        print("\nCommand List:\n\t--store [TIME_MINUTES]: store brush time\n\t--show: show daily brushing data\n")
        return
    elif cliArgs[0] == "--store" and len(cliArgs) > 1:
        storeTime((float)(cliArgs[1]))
    elif cliArgs[0] == "--show":
        showData()
    else:
        print("\n*** Unknown Command, run -h for information ***\n")
        return

# Run main when called
if __name__ == "__main__":
    main()
