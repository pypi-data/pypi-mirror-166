from datetime import timedelta, date
from datetime import datetime as dt

def convert_decimal_time_to_time(time: int) -> str:
    time /= 3600   # convert to hours
    hours = int(time)
    minutes = (time * 60) % 60
    seconds = (time * 3600) % 60
    return "%d:%02d:%02d" % (hours, minutes, seconds)


def add_seconds_to_time(time_to_treat, seconds_to_add: int, subtract: bool = False) -> dt.time:
    datified = dt.combine(date.today(), time_to_treat)
    if subtract:
        new_dt = datified - timedelta(seconds=seconds_to_add)
    else:
        new_dt = datified + timedelta(seconds=seconds_to_add)
    return new_dt.time()


def is_overlapping(first_inter: list, second_inter: list) -> bool:
    for straight, backward in ((first_inter, second_inter), (second_inter, first_inter)):
        # will check both ways
        try:
            for time in (straight[0], straight[1]):
                if backward[0] < time < backward[1]:
                    return True
        except (TypeError, IndexError):
            print('One or more of the intervals_of_used_hypes inputs is of the wrong type')
            raise
    else:
        return False


def return_valid_intervals_only(input_intervals: list, blocker_intervals: list) -> list:
    invalid_intervals = []
    for input_interval in input_intervals:
        for blocker_interval in blocker_intervals:
            if is_overlapping(input_interval, blocker_interval):
                invalid_intervals.append(input_interval)
    return [interval for interval in input_intervals if interval not in invalid_intervals]


def remove_duplicates(lst: list) -> list:
    dup_free = []
    for x in lst:
        if x not in dup_free:
            dup_free.append(x)
    return dup_free


def convert_time_to_seconds(time):
    return timedelta(hours=time.hour, minutes=time.minute, seconds=time.second).total_seconds()

