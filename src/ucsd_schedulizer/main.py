import click
from pathlib import Path
from datetime import datetime, timedelta, date
from icalendar import Calendar, Event
import uuid

def parse_schedule(text):
    courses = []
    for block in text.strip().split("\n\n"):
        lines = [l.strip() for l in block.strip().splitlines() if l.strip()]
        if len(lines) < 3:
            continue
        course = {"name": lines[0]}
        for line in lines[1:]:
            key, _, val = line.partition(":")
            course[key.strip().lower()] = val.strip()
        courses.append(course)
    return courses

def next_weekday(start, weekday):
    days_ahead = weekday - start.weekday()
    if days_ahead < 0:
        days_ahead += 7
    return start + timedelta(days=days_ahead)

DAY_MAP = {"M": 0, "Tu": 1, "W": 2, "Th": 3, "F": 4}

def parse_days(day_str):
    days = []
    i = 0
    while i < len(day_str):
        if day_str[i:i+2] in DAY_MAP:
            days.append((day_str[i:i+2], DAY_MAP[day_str[i:i+2]]))
            i += 2
        elif day_str[i] in DAY_MAP:
            days.append((day_str[i], DAY_MAP[day_str[i]]))
            i += 1
        else:
            i += 1
    return days

def parse_time(t):
    t = t.strip().lower()
    pm = "pm" in t
    t = t.replace("am", "").replace("pm", "")
    h, m = map(int, t.split(":"))
    if pm and h != 12:
        h += 12
    if not pm and h == 12:
        h = 0
    return h, m

@click.command()
@click.option("--input", "-i", "input_file", required=True)
@click.option("--output", "-o", "output_file", default="schedule.ics")
@click.option("--start", "-s", "qstart", required=True, help="Start Date of Quarter YYYY-MM-DD")
@click.option("--end", "-e", "qend", required=True, help="End Date of Quarter YYYY-MM-DD")
def main(input_file, output_file, qstart, qend):
    """Convert a UCSD schedule text file to a .ics calendar file."""
    quarter_start = date.fromisoformat(qstart)
    quarter_end = date.fromisoformat(qend)

    courses = parse_schedule(Path(input_file).read_text())
    cal = Calendar()
    cal.add("prodid", "-//UCSD Schedulizer//EN")
    cal.add("version", "2.0")

    for course in courses:
        for day_str, weekday_int in parse_days(course["days"]):
            sh, sm = parse_time(course["time"].split("-")[0])
            eh, em = parse_time(course["time"].split("-")[1])
            first_day = next_weekday(quarter_start, weekday_int)

            event = Event()
            event.add("summary", course["name"])
            event.add("location", course.get("location", ""))
            event.add("uid", str(uuid.uuid4()))
            event.add("dtstart", datetime(first_day.year, first_day.month, first_day.day, sh, sm))
            event.add("dtend",   datetime(first_day.year, first_day.month, first_day.day, eh, em))
            event.add("rrule", {"FREQ": "WEEKLY", "UNTIL": datetime(quarter_end.year, quarter_end.month, quarter_end.day, 23, 59)})
            cal.add_component(event)

    Path(output_file).write_bytes(cal.to_ical())
    click.echo(f"Written to {output_file}")