import itertools
from pulp import *

teams = ["Team 1", "Team 2", "Team 3", "Team 4", "Team 5", "Team 6", "Team 7", "Team 8"]
venues = ["Venue A", "Venue B"]
days = ["Day 1", "Day 2"]
start_time = 9
end_time = 23
game_duration = 2
fields_per_venue = 3

# Calculate the number of time slots available each day
time_slots_per_day = (end_time - start_time) * 60 // game_duration

# Create a list of all possible time slots
time_slots = [(day, venue, field, time_slot)
              for day in days
              for venue in venues
              for field in range(fields_per_venue)
              for time_slot in range(time_slots_per_day)]

print(time_slots)

# Create the LP problem
problem = LpProblem("GameSchedule", LpMinimize)

# Define the decision variables
x = LpVariable.dicts("x", time_slots, cat='Binary')

# Define the objective function (minimize the total number of games played)
problem += lpSum([x[slot] for slot in time_slots]), "Objective"

# Constraint: Each team plays exactly 3 games
for team in teams:
    problem += lpSum([x[slot] for slot in time_slots if team in slot]) == 3, f"Team_{team}_Constraint"

# Constraint: Each time slot can have at most one game
for slot in time_slots:
    problem += lpSum([x[slot]]) <= 1, f"TimeSlot_{slot}_Constraint"

# Constraint: The venue is available during the time slot
for slot in time_slots:
    day, venue, field, time_slot = slot
    hour = start_time + (time_slot * game_duration) // 60
    minute = (time_slot * game_duration) % 60
    problem += lpSum([x[slot]]) <= int(hour < end_time or (hour == end_time and minute + game_duration <= 60)), \
               f"VenueAvailability_{slot}_Constraint"

# Solve the problem
problem.solve()

# Check if a feasible schedule is found
if problem.status != LpStatusOptimal:
    print("No feasible schedule found.")
    exit(1)

# Display the schedule
schedule = {}
for slot in time_slots:
    if x[slot].varValue == 1:
        day, venue, field, time_slot = slot
        hour = start_time + (time_slot * game_duration) // 60
        minute = (time_slot * game_duration) % 60
        if day not in schedule:
            schedule[day] = {}
        if venue not in schedule[day]:
            schedule[day][venue] = {}
        if field not in schedule[day][venue]:
            schedule[day][venue][field] = []
        schedule[day][venue][field].append((f"{str(hour).zfill(2)}:{str(minute).zfill(2)}", teams[slot[3] % len(teams)]))

# Display the schedule
for day in schedule:
    print(day)
    for venue in schedule[day]:
        print("  " + venue)
        for field in sorted(schedule[day][venue]):
            print("    Field", chr(ord('A')))
