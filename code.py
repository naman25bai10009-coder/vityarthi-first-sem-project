import csv
import os
from datetime import datetime

class HealthTracker:
    def __init__(self, file_name):
        self.file_name = file_name
        self.entries = []
        self.create_file_if_not_exists()
        self.load_data()

    # make file with header if it does not exist
    def create_file_if_not_exists(self):
        if not os.path.exists(self.file_name):
            try:
                with open(self.file_name, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        "date",
                        "sleep_hours",
                        "water_glasses",
                        "exercise_minutes",
                        "screen_nonstudy_hours",
                        "health_score"
                    ])
            except OSError as e:
                print("Error creating file:", e)

    # load old data from csv into list
    def load_data(self):
        self.entries = []
        try:
            with open(self.file_name, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.entries.append(row)
        except FileNotFoundError:
            # no file yet, ok
            pass
        except OSError as e:
            print("Error reading file:", e)

    # health score logic (same style as earlier one)
    def calculate_health_score(self, sleep_hours, water_glasses, exercise_minutes, screen_nonstudy_hours):
        score = 0

        # sleep block
        if 7 <= sleep_hours <= 9:
            score += 25
        elif 6 <= sleep_hours < 7 or 9 < sleep_hours <= 10:
            score += 15
        else:
            score += 5

        # water block
        if water_glasses >= 8:
            score += 25
        elif 5 <= water_glasses < 8:
            score += 15
        else:
            score += 5

        # exercise block
        if exercise_minutes >= 30:
            score += 25
        elif 15 <= exercise_minutes < 30:
            score += 15
        else:
            score += 5

        # non-study screen time block
        if screen_nonstudy_hours <= 4:
            score += 25
        elif 4 < screen_nonstudy_hours <= 6:
            score += 15
        else:
            score += 5

        return score

    # add today entry and save to csv
    def add_entry(self, sleep_hours, water_glasses, exercise_minutes, screen_nonstudy_hours):
        today = datetime.now().strftime("%Y-%m-%d")

        score = self.calculate_health_score(
            sleep_hours,
            water_glasses,
            exercise_minutes,
            screen_nonstudy_hours
        )

        entry = {
            "date": today,
            "sleep_hours": str(sleep_hours),
            "water_glasses": str(water_glasses),
            "exercise_minutes": str(exercise_minutes),
            "screen_nonstudy_hours": str(screen_nonstudy_hours),
            "health_score": str(score)
        }

        # keep in list
        self.entries.append(entry)

        # append to csv file
        try:
            with open(self.file_name, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    entry["date"],
                    entry["sleep_hours"],
                    entry["water_glasses"],
                    entry["exercise_minutes"],
                    entry["screen_nonstudy_hours"],
                    entry["health_score"]
                ])
        except OSError as e:
            print("Error writing to file:", e)

        return score

    # delete all data of a given date
    def delete_entry_by_date(self, date_to_delete):
        new_list = []
        found = False

        for row in self.entries:
            if row.get("date") == date_to_delete:
                found = True
            else:
                new_list.append(row)

        if not found:
            print("No entry found on this date.")
            return

        # rewrite file with remaining rows
        try:
            with open(self.file_name, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "date",
                    "sleep_hours",
                    "water_glasses",
                    "exercise_minutes",
                    "screen_nonstudy_hours",
                    "health_score"
                ])
                for r in new_list:
                    writer.writerow([
                        r.get("date", ""),
                        r.get("sleep_hours", ""),
                        r.get("water_glasses", ""),
                        r.get("exercise_minutes", ""),
                        r.get("screen_nonstudy_hours", ""),
                        r.get("health_score", "")
                    ])
        except OSError as e:
            print("Error rewriting file:", e)
            return

        self.entries = new_list
        print("Data deleted for date:", date_to_delete)

    # show last N entries with average score
    def show_last_entries(self, number_of_days=7):
        if not self.entries:
            print("No data yet. Please add some entries first.")
            return

        last_rows = self.entries[-number_of_days:]
        total_score = 0.0
        count = 0

        print("\nLast {} record(s):".format(len(last_rows)))
        for r in last_rows:
            try:
                score_value = float(r.get("health_score", 0))
            except ValueError:
                score_value = 0.0

            total_score += score_value
            count += 1

            print(
                f"{r.get('date', '')}: score {r.get('health_score', '')}, "
                f"sleep {r.get('sleep_hours', '')}h, "
                f"water {r.get('water_glasses', '')} glasses, "
                f"exercise {r.get('exercise_minutes', '')} min, "
                f"non-study screen {r.get('screen_nonstudy_hours', '')}h"
            )

        if count > 0:
            avg = total_score / count
            print("\nAverage health score over last {} day(s): {:.1f}/100".format(count, avg))


# helper input functions
def ask_float(message):
    while True:
        try:
            value = float(input(message))
            return value
        except ValueError:
            print("Please enter a number.")

def ask_int(message):
    while True:
        try:
            value = int(input(message))
            return value
        except ValueError:
            print("Please enter a whole number.")


def give_basic_tips(score):
    print("\nSome basic tips from this score:")
    if score >= 80:
        print("Nice. Your day looks quite healthy.")
    elif score >= 60:
        print("Not bad, but you can improve some habits.")
    else:
        print("Try to fix small things. Sleep a bit more, drink more water, move more and reduce non-study screen time.")


def show_menu():
    print("\n===== Health Habit Tracker =====")
    print("1. Add today record")
    print("2. Show last 7 days summary")
    print("3. Delete data by date")
    print("4. Exit")


def main():
    tracker = HealthTracker("health_log.csv")

    while True:
        show_menu()
        choice = input("Enter choice (1/2/3/4): ").strip()

        if choice == "1":
            print("\nEnter today data:")
            sleep = ask_float("Hours of sleep: ")
            water = ask_int("Number of glasses of water: ")
            exercise = ask_int("Minutes of exercise: ")
            screen_nonstudy = ask_float(
                "Hours of NON-study screen time (YouTube, social media, etc.): "
            )

            score = tracker.add_entry(sleep, water, exercise, screen_nonstudy)
            print(f"\nYour health score for today is: {score}/100")
            give_basic_tips(score)

        elif choice == "2":
            tracker.show_last_entries(7)

        elif choice == "3":
            date_str = input("Enter date to delete (YYYY-MM-DD): ").strip()
            tracker.delete_entry_by_date(date_str)

        elif choice == "4":
            print("Exiting. Take care of your health.")
            break

        else:
            print("Wrong option. Please enter 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()
