# Nmae : Vishnu Shankar
# Roll No: 2501940001
# Date   : 2025-11-11
# Title  : Attendance Tracker (MCA - Programming for Problem Solving Using Python)

import re
from datetime import datetime

TIME_PATTERN = re.compile(r'^(0?[1-9]|1[0-2]):[0-5][0-9]\s?(AM|PM)$', re.I)

def welcome():
    print("\n" + "="*60)
    print("Welcome to the Command-line Attendance Tracker")
    print("This tool records student names with check-in times and generates a summary.\n")
    print("Instructions:")
    print("- Enter student names (cannot be blank).")
    print("- Enter time like '09:15 AM' or '9:15 am'.\n")
    print("="*60 + "\n")

def validate_name(name: str) -> str:
    """Return cleaned name or raise ValueError if blank."""
    cleaned = name.strip()
    if not cleaned:
        raise ValueError("Name cannot be empty.")
    # Normalize spacing and capitalization
    return " ".join(part.capitalize() for part in cleaned.split())

def validate_time(ts: str) -> str:
    """
    Validate and normalize check-in time.
    Accepts formats like '09:15 AM', '9:05pm', etc.
    Returns normalized string like '09:15 AM'.
    """
    if not ts or not ts.strip():
        raise ValueError("Timestamp cannot be empty.")
    s = ts.strip().upper().replace('.', '')
    # Ensure a space before AM/PM for consistent parsing
    s = re.sub(r'([AP]M)$', r' \1', s)
    if not TIME_PATTERN.match(s):
        raise ValueError("Time must be in format HH:MM AM/PM (e.g., 09:15 AM).")
    # Normalize hour and minutes: ensure two-digit hour
    parts = s.split()
    hhmm = parts[0]
    ampm = parts[1]
    hh, mm = hhmm.split(':')
    hh = hh.zfill(2)
    return f"{hh}:{mm} {ampm}"

def collect_attendance() -> dict:
    """Collect multiple attendance entries from user with validation."""
    attendance = {}
    while True:
        try:
            count_input = input("How many entries do you want to record? (enter a positive integer): ").strip()
            total_entries = int(count_input)
            if total_entries <= 0:
                print("Please enter a number greater than zero.")
                continue
            break
        except ValueError:
            print("That's not an integer. Try again.")
    print()

    entry_num = 1
    while entry_num <= total_entries:
        try:
            raw_name = input(f"Entry #{entry_num} - Student name: ")
            name = validate_name(raw_name)

            if name in attendance:
                print(f"Duplicate entry: '{name}' already recorded. Skipping duplicate.")
                # Do not increment entry_num; allow user to re-enter this slot or choose to continue
                continue

            raw_time = input(f"Entry #{entry_num} - Check-in time for {name} (HH:MM AM/PM): ")
            time_normalized = validate_time(raw_time)

            attendance[name] = time_normalized
            entry_num += 1
        except ValueError as ve:
            print("Input error:", ve)
            print("Please re-enter this entry.\n")
    return attendance

def show_summary(attendance: dict, total_strength: int | None = None):
    """Print a formatted attendance table and total present/absent if total_strength provided."""
    names_sorted = sorted(attendance.keys())
    total_present = len(names_sorted)

    # Determine column widths
    name_col = max([len("Student Name")] + [len(n) for n in names_sorted]) + 2
    time_col = max(len("Check-in Time"), 8) + 2

    header = f"{'Student Name'.ljust(name_col)}{'Check-in Time'.ljust(time_col)}"
    sep = "-" * (name_col + time_col)
    print("\n" + sep)
    print(header)
    print(sep)
    for n in names_sorted:
        print(f"{n.ljust(name_col)}{attendance[n].ljust(time_col)}")
    print(sep)
    print(f"Total Students Present: {total_present}")
    if total_strength is not None:
        if total_strength < 0:
            print("Warning: total class strength cannot be negative. Ignoring absentee calc.")
        else:
            absent = max(0, total_strength - total_present)
            print(f"Total Students Absent : {absent} (Class strength: {total_strength})")
    print()

def ask_total_strength() -> int | None:
    """Ask user optionally for total class strength and return int or None."""
    resp = input("Do you want to calculate absentees? (y/n): ").strip().lower()
    if resp not in ('y', 'yes'):
        return None
    while True:
        try:
            t = int(input("Enter total number of students in the class (integer): ").strip())
            if t < 0:
                print("Please enter a non-negative integer.")
                continue
            return t
        except ValueError:
            print("That's not an integer. Try again.")

def save_report_to_file(attendance: dict, total_strength: int | None):
    """Prompt user and save the report to attendance_log.txt with timestamp if requested."""
    resp = input("Would you like to save the attendance report to 'attendance_log.txt'? (y/n): ").strip().lower()
    if resp not in ('y', 'yes'):
        print("Report not saved.")
        return

    now = datetime.now()
    filename = "attendance_log.txt"
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write("="*60 + "\n")
            f.write("Attendance Report\n")
            f.write(f"Generated on: {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("-" * 60 + "\n")
            f.write(f"{'Student Name'.ljust(30)}{'Check-in Time'.ljust(15)}\n")
            f.write("-" * 60 + "\n")
            for name in sorted(attendance.keys()):
                f.write(f"{name.ljust(30)}{attendance[name].ljust(15)}\n")
            f.write("-" * 60 + "\n")
            f.write(f"Total Present: {len(attendance)}\n")
            if total_strength is not None:
                absent = max(0, total_strength - len(attendance))
                f.write(f"Total Absent : {absent}\n")
            f.write("\n")
        print(f"Report saved successfully to '{filename}'.")
    except Exception as e:
        print("Failed to save report:", e)

def main():
    welcome()
    attendance = collect_attendance()
    total_strength = ask_total_strength()
    show_summary(attendance, total_strength)
    save_report_to_file(attendance, total_strength)
    print("Thank you — attendance recorded. Goodbye!\n")

if __name__ == "__main__":
    main()
