import math
import random


class UNO_OPTIMO:
    def __init__(self, num_ants, num_iterations, decay, alpha=1, beta=1, shipment_data=None, vehicle_data=None):
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        self.shipment_data = shipment_data
        self.vehicle_data = vehicle_data
        self.best_solution = None
        self.best_vehicles_used = float('inf')
        self.skipped_shipments = []

    def initialize_pheromones(self, num_vehicles):
        return [[1.0 for _ in range(num_vehicles)] for _ in range(num_vehicles)]

    def place_shipment(self, shipment, vehicle_loads, pheromones):
        probabilities = [0] * len(vehicle_loads)
        total = 0

        for i, vehicle in enumerate(vehicle_loads):
            used_capacity = sum(s['capacity'] for s in vehicle['shipments'])
            remaining_capacity = vehicle['capacity'] - used_capacity
            if shipment['capacity'] <= remaining_capacity:
                # Enhanced Heuristic: Strong preference for vehicles with less remaining capacity
                heuristic_val = (used_capacity + shipment['capacity']) / vehicle['capacity']
                pheromone_val = pheromones[i][i]
                prob = (pheromone_val ** self.alpha) * (heuristic_val ** self.beta)
                probabilities[i] = prob
                total += prob

        if total == 0:
            return False

        probabilities = [p / total for p in probabilities]
        chosen_vehicle_index = random.choices(range(len(vehicle_loads)), weights=probabilities, k=1)[0]
        vehicle_loads[chosen_vehicle_index]['shipments'].append(shipment)
        return True

    def solve(self):
        num_vehicles = len(self.vehicle_data)
        pheromones = self.initialize_pheromones(num_vehicles)
        self.best_solution = None
        self.skipped_shipments = []

        for iteration in range(self.num_iterations):
            iteration_best_solution = None
            iteration_best_vehicles_used = float('inf')
            iteration_skipped_shipments = []

            for ant in range(self.num_ants):
                vehicle_loads = [{'id': v['id'], 'capacity': v['capacity'], 'shipments': []} for v in self.vehicle_data]
                skipped_shipments = []

                for shipment in self.shipment_data:
                    if not self.place_shipment(shipment, vehicle_loads, pheromones):
                        skipped_shipments.append(shipment)

                vehicles_used = sum(1 for vehicle in vehicle_loads if vehicle['shipments'])
                if vehicles_used < iteration_best_vehicles_used:
                    iteration_best_vehicles_used = vehicles_used
                    iteration_best_solution = vehicle_loads
                    iteration_skipped_shipments = skipped_shipments

            if iteration_best_vehicles_used < self.best_vehicles_used:
                self.best_vehicles_used = iteration_best_vehicles_used
                self.best_solution = iteration_best_solution
                self.skipped_shipments = iteration_skipped_shipments

            # Pheromone Update
            for i in range(num_vehicles):
                for j in range(num_vehicles):
                    pheromones[i][j] *= (1 - self.decay)
                    if iteration_best_solution and i < len(iteration_best_solution) and iteration_best_solution[i][
                        'shipments']:
                        pheromones[i][j] += 1.0 / iteration_best_vehicles_used

    def print_solution(self):
        if not self.best_solution:
            print("No solution found.")
            return

        print("Truck Loading Configuration:")
        for vehicle in self.best_solution:
            print(f"Vehicle ID {vehicle['id']} (Capacity: {vehicle['capacity']}):")
            for shipment in vehicle['shipments']:
                print(f"  - Shipment AWB {shipment['awb']} (Capacity: {shipment['capacity']})")
            used_capacity = sum(shipment['capacity'] for shipment in vehicle['shipments'])
            print(f"  Total Used Capacity: {used_capacity}")
            print(f"  Remaining Capacity: {vehicle['capacity'] - used_capacity}")
            print("----")

        if self.skipped_shipments:
            print("Skipped Shipments:")
            for shipment in self.skipped_shipments:
                print(f"  Shipment AWB {shipment['awb']} (Capacity: {shipment['capacity']})")


# Example usage
shipment_data =  [{"awb": i, "capacity": math.floor(random.random()*100)} for i in range(1, 21)]  # 20 shipments of increasing sizes
# vehicle_data = [{"id": i, "capacity": 500} for i in range(1, 5)]  # 4 vehicles, each with capacity 500
vehicle_data = [{"id": 1, "capacity": 500}, {"id": 2, "capacity": 510}, {"id": 3, "capacity": 600}]  # 4 vehicles, each with capacity 500


# shipment_data = [{"awb": 1, "capacity": 500}, {"awb": 2, "capacity": 300}, {"awb": 3, "capacity": 200}]
# vehicle_data = [{"id": 1, "capacity": 1000}, {"id": 2, "capacity": 800}]


uno_optimo = UNO_OPTIMO(num_ants=10, num_iterations=100, decay=0.1, alpha=1, beta=1, shipment_data=shipment_data,
                        vehicle_data=vehicle_data)
uno_optimo.solve()
uno_optimo.print_solution()



# give one approache with multiple steps that should be taken to imporve our UNO-optima