from pyscipopt import Model, quicksum

# Data
shipment_data = [{"awb": 1, "capacity": 500}, {"awb": 2, "capacity": 300}, {"awb": 3, "capacity": 200}]
vehicle_data = [{"id": 1, "capacity": 550}, {"id": 2, "capacity": 600}, {"id": 3, "capacity": 550}]

# Create a SCIP model
model = Model("Optimal Shipment Allocation")

# Variables
x = {}  # x[i, j] is 1 if shipment i is assigned to vehicle j
u = {}  # u[j] is the used capacity of vehicle j
for vehicle in vehicle_data:
    u[vehicle['id']] = model.addVar(vtype="C", name=f"u_{vehicle['id']}")
    for shipment in shipment_data:
        x[shipment['awb'], vehicle['id']] = model.addVar(vtype="B", name=f"x_{shipment['awb']}_{vehicle['id']}")

# Constraints
# Each shipment is assigned to exactly one vehicle
for shipment in shipment_data:
    model.addCons(quicksum(x[shipment['awb'], vehicle['id']] for vehicle in vehicle_data) == 1)

# The total capacity of shipments in each vehicle does not exceed its maximum capacity
for vehicle in vehicle_data:
    model.addCons(quicksum(shipment['capacity'] * x[shipment['awb'], vehicle['id']] for shipment in shipment_data) <= vehicle['capacity'])

# Link the used capacity variables to the assignment variables
for vehicle in vehicle_data:
    model.addCons(quicksum(shipment['capacity'] * x[shipment['awb'], vehicle['id']] for shipment in shipment_data) == u[vehicle['id']])

# Objective: Adjusted objective function to balance minimizing number of vehicles and unused capacity
alpha = 100  # Adjusted weight factor
model.setObjective(
    quicksum(x[shipment['awb'], vehicle['id']] for shipment in shipment_data for vehicle in vehicle_data) + 
    alpha * quicksum(vehicle['capacity'] - u[vehicle['id']] for vehicle in vehicle_data), "minimize")

# Solve the problem
model.optimize()

# Process and display the solution
if model.getStatus() == 'optimal':
    print('Optimal solution found:')
    for vehicle in vehicle_data:
        print(f"\nVehicle {vehicle['id']}:")
        for shipment in shipment_data:
            if model.getVal(x[shipment['awb'], vehicle['id']]) > 0.5:
                print(f"  Shipment {shipment['awb']} with capacity {shipment['capacity']}")
else:
    print("No optimal solution found.")
