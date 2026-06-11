# UCSD_Schedulizer
A command-line tool that takes a class schedule and generates a file that can be imported to Google Calendar.

## USAGE
### Step 1: Install:
```bash
uv add "git+https://github.com/vGoyal413/UCSD_Schedulizer.git"
```

### Step 2: Create A File Containing Your Schedule:
Create a text file (.txt) containing information about the course - like the following example:

DSC 190 - Tools of the Trade
Days: MWF
Time: 11:00am - 11:50pm
Location: PODEM 1A18

DSC 80 - Practice and Application of Data Science
Days: TuTh
Time: 9:30am - 10:50am
Location: PCYNH 106

Days can be any combination of: 'M','Tu','W','Th','F'

### Step 3: Run the program:
```bash
schedulizer -i schedule.txt -s [start_date] -e [end_date]
```
This will write `schedule.ics` in your current directory.

Where `start_date` and `end_date` are the first and last day of the quarter in `YYYY-MM-DD` format (e.g. `2025-03-31`). This writes `schedule.ics` to your current directory.

### Step 4: Import into Google Calendar
Go to Google Calendar, then Settings, then Import and Export, and then select the .ics file!