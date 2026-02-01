import pulp
import pandas as pd
import random


# DEFINE BUILDING ROOMS
# Number of rooms in the building
rooms = {
    'Labs': 3,
    'Classrooms': 3,
    'Office': 10
}


# DEFINE TIME PERIODS
time_periods = ['Morning', 'Afternoon', 'Evening']


# ELECTRICITY COST (₦/kWh)
electricity_cost = {
    'Morning': 40,
    'Afternoon': 60,
    'Evening': 90
}


# TOTAL AVAILABLE POWER (kWh)
total_available_power = {
    'Morning': 80,
    'Afternoon': 80,
    'Evening': 60
}

# AI KNOWLEDGE BASE (DEMAND RANGES)
demand_rules = {
    'Labs': {
        'Morning': (12, 15),
        'Afternoon': (10, 13),
        'Evening': (8, 10)
    },
    'Classrooms': {
        'Morning': (6, 8),
        'Afternoon': (5, 7),
        'Evening': (4, 6)
    },
    'Office': {
        'Morning': (3, 4),
        'Afternoon': (3, 4),
        'Evening': (3, 4)
    }
}


# AI DEMAND PREDICTION
predicted_demand = {}

for room_type, periods in demand_rules.items():
    predicted_demand[room_type] = {}
    for period, (low, high) in periods.items():
        predicted_demand[room_type][period] = round(
            random.uniform(low, high), 2
        )

print("AI Predicted Demand (kWh):")
for room in predicted_demand:
    print(room, predicted_demand[room])


# CREATE LP MODEL
model = pulp.LpProblem("Smart_nerg", pulp.LpMinimize)


# DECISION VARIABLES
power_vars = {}

for room_type, count in rooms.items():
    for i in range(1, count + 1):
        for period in time_periods:
            var_name = f"{room_type}_{i}_{period}"
            power_vars[var_name] = pulp.LpVariable(
                var_name,
                lowBound=0,
                upBound=predicted_demand[room_type][period]
            )


# OBJECTIVE FUNCTION
# Minimize total electricity cost
model += pulp.lpSum(
    electricity_cost[var.split("_")[-1]] * power_vars[var]
    for var in power_vars
)


# MINIMUM POWER CONSTRAINTS
# Minimum power each room must receive
min_power = {
    'Labs': 6.0,
    'Classrooms': 4.0,
    'Office': 2.0
}

for room_type, min_pwr in min_power.items():
    for i in range(1, rooms[room_type] + 1):
        for period in time_periods:
            model += power_vars[f"{room_type}_{i}_{period}"] >= min_pwr


#TOTAL POWER AVAILABILITY CONSTRAINT
for period in time_periods:
    model += pulp.lpSum(
        power_vars[var]
        for var in power_vars
        if var.endswith(period)
    ) <= total_available_power[period]


#SOLVE MODEL
model.solve()

print("\nOptimization Status:", pulp.LpStatus[model.status])


#DISPLAY RESULTS
results = []

for var in power_vars:
    results.append([var, round(power_vars[var].varValue, 2)])

df_results = pd.DataFrame(results, columns=["Room", "Allocated Power (kWh)"])
print("\n Energy Allocation per Room:")
display(df_results)


# COST CALCULATION
total_cost = sum(
    power_vars[var].varValue * electricity_cost[var.split("_")[-1]]
    for var in power_vars
)

print(f"\n Total Electricity Cost: ₦{round(total_cost, 2)}\n")


# POWER USAGE SUMMARY
for period in time_periods:
    total_used = sum(
        power_vars[var].varValue
        for var in power_vars
        if var.endswith(period)
    )
    print(
        f" {period}: {round(total_used, 2)} kWh used / "
        f"{total_available_power[period]} kWh available"
    )