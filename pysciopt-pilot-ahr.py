from pyscipopt import Model

# Data
shipment_data = [{"awb": 1, "capacity": 500}, {"awb": 2, "capacity": 300}, {"awb": 3, "capacity": 200}]
vehicle_data = [{"id": 1, "capacity": 1000}, {"id": 2, "capacity": 1001}]

# Create a SCIP model
model = Model("Optimal Shipment Allocation")

# Variables: x[i, j] is True if shipment i is assigned to vehicle j.
x = {}
for shipment in shipment_data:
    for vehicle in vehicle_data:
        x[shipment['awb'], vehicle['id']] = model.addVar(vtype="B", name=f"x_{shipment['awb']}_{vehicle['id']}")

# Constraints
# Each shipment is assigned to exactly one vehicle
for shipment in shipment_data:
    model.addCons(sum(x[shipment['awb'], vehicle['id']] for vehicle in vehicle_data) == 1)

# The total capacity of shipments in each vehicle does not exceed its maximum capacity
for vehicle in vehicle_data:
    model.addCons(sum(shipment['capacity'] * x[shipment['awb'], vehicle['id']] for shipment in shipment_data) <= vehicle['capacity'])

# Objective: Minimize the number of vehicles used
model.setObjective(sum(x[shipment['awb'], vehicle['id']] for shipment in shipment_data for vehicle in vehicle_data), "minimize")

# Solve the problem
model.optimize()

# Check if a feasible solution has been found
if model.getStatus() == 'optimal':
    print('Solution:')
    for vehicle in vehicle_data:
        vehicle_load = 0
        print(f"\nVehicle {vehicle['id']}:")
        for shipment in shipment_data:
            if model.getVal(x[shipment['awb'], vehicle['id']]) > 0.5:
                print(f"  Shipment {shipment['awb']} with capacity {shipment['capacity']}")
                vehicle_load += shipment['capacity']
        print(f"  Total load: {vehicle_load}")
else:
    print("No optimal solution found.")
# Close the model
del model
