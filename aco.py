import math
import random
import time


class UNO_OPTIMO:
    """
    A class to model and solve the vehicle routing problem with an Ant Colony Optimization (ACO) approach.

    Attributes:
        num_ants (int): The number of ants (solutions) to generate per iteration.
        num_iterations (int): The number of iterations to perform the optimization.
        decay (float): The rate at which pheromone trails decay.
        alpha (float): The exponent on the pheromone trail influence (default=1).
        beta (float): The exponent on the heuristic information (default=1).
        shipment_data (list): A list of dictionaries, each representing a shipment with its properties.
        vehicle_data (list): A list of dictionaries, each representing a vehicle with its properties.
        best_solution (list): The best solution found during the optimization process.
        best_vehicles_used (int): The number of vehicles used in the best solution.
        skipped_shipments (list): Shipments that could not be placed in any vehicle in the best solution.
        best_evaluation (tuple): A tuple containing the evaluation metrics of the best solution.

    Methods:
        initialize_pheromones(num_vehicles): Initializes the pheromone matrix for the given number of vehicles.
        place_shipment(shipment, vehicle_loads, pheromones): Attempts to place a shipment in the best vehicle based on pheromones and heuristic.
        evaluate_solution(vehicle_loads): Evaluates a solution based on the number of vehicles used and total remaining capacity.
        construct_solution(pheromones): Constructs a solution (vehicle loads) based on current pheromones.
        solve(): Runs the ACO algorithm to find the best solution for the vehicle routing problem.
        print_solution(): Prints the details of the best solution found.
    """

    def __init__(self, num_ants, num_iterations, decay, alpha=1, beta=1, shipment_data=None, vehicle_data=None):
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        self.shipment_data = shipment_data
        self.vehicle_data = vehicle_data
        self.best_solution = None
        self.best_vehicles_used = float("inf")
        self.skipped_shipments = []
        self.best_evaluation = (float("inf"), float("inf"))

    @staticmethod
    def initialize_pheromones(num_vehicles):
        return [[1.0 for _ in range(num_vehicles)] for _ in range(num_vehicles)]

    def place_shipment(self, shipment, vehicle_loads, pheromones):
        # If no exact match, use the probabilistic approach
        probabilities = [0] * len(vehicle_loads)
        total = 0

        for i, vehicle in enumerate(vehicle_loads):
            used_capacity = sum(s["capacity"] for s in vehicle["shipments"])
            remaining_capacity = vehicle["capacity"] - used_capacity
            if shipment["capacity"] <= remaining_capacity:
                # Heuristic favors vehicles which will have the least remaining capacity after adding the shipment
                heuristic_val = (used_capacity + shipment['capacity']) / vehicle['capacity']
                pheromone_val = pheromones[i][i]
                prob = (pheromone_val ** self.alpha) * (heuristic_val ** self.beta)
                probabilities[i] = prob
                total += prob

        if total == 0:
            return False

        probabilities = [p / total for p in probabilities]
        chosen_vehicle_index = random.choices(
            range(len(vehicle_loads)), weights=probabilities, k=1)[0]
        vehicle_loads[chosen_vehicle_index]['shipments'].append(shipment)
        return True

    @staticmethod
    def evaluate_solution(vehicle_loads):
        num_vehicles_used = sum(
            1 for vehicle in vehicle_loads if vehicle['shipments'])
        total_remaining_capacity = sum(
            vehicle['capacity'] - sum(shipment['capacity'] for shipment in vehicle['shipments'])
            for vehicle in vehicle_loads if vehicle['shipments'])
        return num_vehicles_used, total_remaining_capacity

    def construct_solution(self, pheromones):
        vehicle_loads = [{'id': v['id'], 'capacity': v['capacity'], 'shipments': []} for v in self.vehicle_data]
        skipped_shipments = []

        for shipment in self.shipment_data:
            placed = self.place_shipment(shipment, vehicle_loads, pheromones)
            if not placed:
                skipped_shipments.append(shipment)

        return vehicle_loads, skipped_shipments

    def solve(self):
        num_vehicles = len(self.vehicle_data)
        pheromones = self.initialize_pheromones(num_vehicles)

        for iteration in range(self.num_iterations):
            iteration_best_solution = None
            iteration_best_vehicles_used = float("inf")
            iteration_skipped_shipments = []
            vehicle_loads = []
            for ant in range(self.num_ants):
                vehicle_loads, skipped_shipments = self.construct_solution(pheromones)

                vehicles_used = sum(1 for vehicle in vehicle_loads if vehicle['shipments'])
                if vehicles_used < iteration_best_vehicles_used:
                    iteration_best_vehicles_used = vehicles_used
                    iteration_best_solution = vehicle_loads
                    iteration_skipped_shipments = skipped_shipments

            current_evaluation = self.evaluate_solution(vehicle_loads)
            if current_evaluation < self.best_evaluation:
                self.best_evaluation = current_evaluation
                self.best_solution = vehicle_loads.copy()
                self.skipped_shipments = iteration_skipped_shipments

            # Pheromone Update
            for i in range(num_vehicles):
                for j in range(num_vehicles):
                    pheromones[i][j] *= (1 - self.decay)
                    if (iteration_best_solution and
                            i < len(iteration_best_solution) and iteration_best_solution[i]['shipments']):
                        pheromones[i][j] += 1.0 / iteration_best_vehicles_used

    def print_solution(self):
        if not self.best_solution:
            print("No solution found.")
            return

        num_vehicles_used = sum(
            1 for vehicle in self.best_solution if vehicle['shipments'])
        total_remaining_capacity = sum(
            vehicle['capacity'] - sum(shipment['capacity'] for shipment in vehicle['shipments'])
            for vehicle in self.best_solution if vehicle['shipments'])
        score = (num_vehicles_used, total_remaining_capacity)

        print(f"Number of Vehicles Used: {num_vehicles_used}")
        print(f"Total Remaining Capacity: {total_remaining_capacity}")
        print(f"Score: {score}")

        print("\nTruck Loading Configuration:")
        for vehicle in self.best_solution:
            print(
                f"Vehicle ID {vehicle['id']} (Capacity: {vehicle['capacity']}):")
            for shipment in vehicle['shipments']:
                print(
                    f"  - Shipment AWB {shipment['awb']} (Capacity: {shipment['capacity']})")
            used_capacity = sum(shipment['capacity']
                                for shipment in vehicle['shipments'])
            print(f"  Total Used Capacity: {used_capacity}")
            print(
                f"  Remaining Capacity: {vehicle['capacity'] - used_capacity}")
            print("----")


# # Example usage

# shipment_data = [
#     {"awb": 1, "capacity": 500},
#     {"awb": 2, "capacity": 300},
#     {"awb": 3, "capacity": 200},
#     {"awb": 4, "capacity": 100},
#     {"awb": 5, "capacity": 600}
# ]
# vehicle_data = [
#     {"id": 1, "capacity": 500},
#     {"id": 2, "capacity": 600},
#     {"id": 3, "capacity": 550},
#     {"id": 4, "capacity": 800}
# ]


# shipment_data = [
#     {"awb": i + 1, "capacity": math.floor(random.random() * 100)} for i in range(0, 100)
# ]
#
# vehicle_data = [
#     {"id": i + 1, "capacity": random.randint(100, 1000)} for i in range(0, 20)
# ]

shipment_data = [{'awb': 1, 'capacity': 62}, {'awb': 2, 'capacity': 25}, {'awb': 3, 'capacity': 89}, {'awb': 4, 'capacity': 5}, {'awb': 5, 'capacity': 33}, {'awb': 6, 'capacity': 60}, {'awb': 7, 'capacity': 50}, {'awb': 8, 'capacity': 6}, {'awb': 9, 'capacity': 3}, {'awb': 10, 'capacity': 9}, {'awb': 11, 'capacity': 71}, {'awb': 12, 'capacity': 71}, {'awb': 13, 'capacity': 68}, {'awb': 14, 'capacity': 5}, {'awb': 15, 'capacity': 54}, {'awb': 16, 'capacity': 97}, {'awb': 17, 'capacity': 60}, {'awb': 18, 'capacity': 43}, {'awb': 19, 'capacity': 87}, {'awb': 20, 'capacity': 39}, {'awb': 21, 'capacity': 24}, {'awb': 22, 'capacity': 88}, {'awb': 23, 'capacity': 60}, {'awb': 24, 'capacity': 33}, {'awb': 25, 'capacity': 96}, {'awb': 26, 'capacity': 71}, {'awb': 27, 'capacity': 4}, {'awb': 28, 'capacity': 71}, {'awb': 29, 'capacity': 72}, {'awb': 30, 'capacity': 8}, {'awb': 31, 'capacity': 99}, {'awb': 32, 'capacity': 78}, {'awb': 33, 'capacity': 99}, {'awb': 34, 'capacity': 87}, {'awb': 35, 'capacity': 83}, {'awb': 36, 'capacity': 29}, {'awb': 37, 'capacity': 44}, {'awb': 38, 'capacity': 51}, {'awb': 39, 'capacity': 96}, {'awb': 40, 'capacity': 7}, {'awb': 41, 'capacity': 56}, {'awb': 42, 'capacity': 30}, {'awb': 43, 'capacity': 75}, {'awb': 44, 'capacity': 89}, {'awb': 45, 'capacity': 13}, {'awb': 46, 'capacity': 10}, {'awb': 47, 'capacity': 61}, {'awb': 48, 'capacity': 74}, {'awb': 49, 'capacity': 51}, {'awb': 50, 'capacity': 45}, {'awb': 51, 'capacity': 91}, {'awb': 52, 'capacity': 34}, {'awb': 53, 'capacity': 49}, {'awb': 54, 'capacity': 75}, {'awb': 55, 'capacity': 61}, {'awb': 56, 'capacity': 83}, {'awb': 57, 'capacity': 24}, {'awb': 58, 'capacity': 42}, {'awb': 59, 'capacity': 82}, {'awb': 60, 'capacity': 76}, {'awb': 61, 'capacity': 42}, {'awb': 62, 'capacity': 89}, {'awb': 63, 'capacity': 12}, {'awb': 64, 'capacity': 33}, {'awb': 65, 'capacity': 13}, {'awb': 66, 'capacity': 63}, {'awb': 67, 'capacity': 72}, {'awb': 68, 'capacity': 76}, {'awb': 69, 'capacity': 95}, {'awb': 70, 'capacity': 11}, {'awb': 71, 'capacity': 34}, {'awb': 72, 'capacity': 41}, {'awb': 73, 'capacity': 42}, {'awb': 74, 'capacity': 5}, {'awb': 75, 'capacity': 62}, {'awb': 76, 'capacity': 66}, {'awb': 77, 'capacity': 5}, {'awb': 78, 'capacity': 75}, {'awb': 79, 'capacity': 7}, {'awb': 80, 'capacity': 45}, {'awb': 81, 'capacity': 4}, {'awb': 82, 'capacity': 30}, {'awb': 83, 'capacity': 75}, {'awb': 84, 'capacity': 27}, {'awb': 85, 'capacity': 98}, {'awb': 86, 'capacity': 33}, {'awb': 87, 'capacity': 37}, {'awb': 88, 'capacity': 92}, {'awb': 89, 'capacity': 58}, {'awb': 90, 'capacity': 6}, {'awb': 91, 'capacity': 36}, {'awb': 92, 'capacity': 90}, {'awb': 93, 'capacity': 55}, {'awb': 94, 'capacity': 30}, {'awb': 95, 'capacity': 36}, {'awb': 96, 'capacity': 19}, {'awb': 97, 'capacity': 16}, {'awb': 98, 'capacity': 55}, {'awb': 99, 'capacity': 71}, {'awb': 100, 'capacity': 85}]

vehicle_data = [{'id': 1, 'capacity': 549}, {'id': 2, 'capacity': 573}, {'id': 3, 'capacity': 433}, {'id': 4, 'capacity': 394}, {'id': 5, 'capacity': 640}, {'id': 6, 'capacity': 604}, {'id': 7, 'capacity': 769}, {'id': 8, 'capacity': 240}, {'id': 9, 'capacity': 237}, {'id': 10, 'capacity': 524}, {'id': 11, 'capacity': 332}, {'id': 12, 'capacity': 585}, {'id': 13, 'capacity': 486}, {'id': 14, 'capacity': 883}, {'id': 15, 'capacity': 170}, {'id': 16, 'capacity': 234}, {'id': 17, 'capacity': 194}, {'id': 18, 'capacity': 658}, {'id': 19, 'capacity': 364}, {'id': 20, 'capacity': 414}]


# print(shipment_data)
# print(vehicle_data)

uno_optimo = UNO_OPTIMO(num_ants=10, num_iterations=500, decay=0.1, alpha=1, beta=1, shipment_data=shipment_data,
                        vehicle_data=vehicle_data)
start_time = time.time()
uno_optimo.solve()
uno_optimo.print_solution()
execution_time = time.time() - start_time
print(f"Time Taken: {execution_time:.2f} seconds")
