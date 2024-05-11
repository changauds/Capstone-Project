import json
import calendar
from datetime import datetime, timedelta

# open toothbrush_daily_json file
f = open('toothbrush_daily.json')
data_we_need = json.load(f)
 

def find_start_week(Date):
    # Convert the input date string to a datetime object
    given_date = datetime.datetime.strptime(Date, '%Y %m %d')
    start_week =  given_date - datetime.timedelta(days = given_date.weekday())
    done_find = start_week.strptime('%Y %m %d')
    return done_find


def group_weekly_average(data_we_need):

    ave_week = {}   
    for date_brush in  data_we_need.keys( ):
        info_date =  data_we_need[date_brush]
        brush_time = info_date['brush_time_minutes']
        brush_count = info_date['brush_count']
        average_brush_time = (sum(brush_time)  / len( brush_time))
        # calling the function from what we get from which day is the start of week
        which_start = find_start_week(date_brush) 
        # update the data if is not in the start week in the ave_week dictionary
        updated_data = ave_week.get(which_start, {"t_time":0 , "t_counts":0, "num_days:":0 })
        updated_data["t_counts"] = updated_data["t_counts"] +  brush_count
        updated_data["t_time"] = updated_data["t_time"] +  brush_time 
        updated_data["num_days"] = updated_data["num_days"] + 1
        ave_week[which_start] = updated_data


#calculate average for every week
# - iterate through each day's brush data
# - calculate the average brush time for the day
# - finds the start of the week for that day and update weekly brush data in the ave_week
for which_start, updated_data in ave_week.keys():
    ave_c = updated_data["t_counts"] /  updated_data["num_days"]
    ave_t = updated_data["t_time"]   /  updated_data["num_days"]
    updated_data = { 
        "ave_time" : ave_t , "ave_count" : ave_c , 
    }
    ave_week[which_start] =  updated_data


# Compare weekly data
pre_week_data = {} 

curr_week = ave_week[which_start]

for i in curr_week:
    diff = curr_week - pre_week_data
    print(f"diff")

pre_week_data = ave_week[which_start]


return ave_week


