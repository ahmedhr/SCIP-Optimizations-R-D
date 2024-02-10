
# SCIP Optimizations Research & Development

## Introduction
This repository contains research and development work on SCIP (Solving Constraint Integer Programs) optimizations. It focuses on exploring advanced techniques to enhance SCIP's performance in various scenarios.


## UNO OPTIMO: Vehicle Routing Optimization

UNO OPTIMO is a sophisticated vehicle routing optimization tool designed to efficiently solve the complex problem of assigning shipments to a fleet of vehicles. Utilizing an Ant Colony Optimization (ACO) approach, UNO OPTIMO aims to minimize the number of vehicles used while maximizing the overall load capacity utilization. This tool is ideal for logistics and distribution companies looking to optimize their routing strategies, reduce operational costs, and improve service delivery.

## Features

- **Ant Colony Optimization: Leverages the ACO algorithm to find the most efficient routing solutions.
- **Customizable Parameters: Allows adjustment of key parameters such as the number of ants, iterations, pheromone decay rate, and heuristic influence to fine-tune the optimization process.
- **Heuristic Evaluation: Incorporates heuristic information to guide the search process towards more promising solutions.
- **Dynamic Shipment Placement: Employs a probabilistic approach for shipment placement, considering both pheromone trails and heuristic information.
- **Solution Evaluation: Evaluates solutions based on the number of vehicles used and the total remaining capacity, aiming for optimal resource utilization.
- **Scalability: Designed to handle varying sizes of shipment and vehicle data, making it suitable for both small and large-scale operations.

## Installation

To get started with UNO OPTIMO, clone this repository to your local machine:

``` git clone https://github.com/your-username/uno-optimo.git
cd uno-optimo ```

Ensure you have Python 3.6 or later installed on your system. No additional dependencies are required to run the tool.

## Usage

To use UNO OPTIMO, you need to prepare your shipment and vehicle data in the form of lists of dictionaries. Each shipment and vehicle dictionary should contain the necessary attributes as described in the class documentation.

Example:


```from uno_optimo import UNO_OPTIMO

# Sample shipment data
shipment_data = [
    {"id": "S1", "capacity": 10},
    {"id": "S2", "capacity": 20},
    # Add more shipments as needed
]

# Sample vehicle data
vehicle_data = [
    {"id": "V1", "capacity": 100},
    {"id": "V2", "capacity": 150},
    # Add more vehicles as needed
]

# Initialize the optimizer
optimizer = UNO_OPTIMO(
    num_ants=10,
    num_iterations=100,
    decay=0.1,
    alpha=1,
    beta=1,
    shipment_data=shipment_data,
    vehicle_data=vehicle_data
)

# Run the optimization
optimizer.solve()

# Print the best solution found
optimizer.print_solution()```

## Contributing

Contributions to UNO OPTIMO are welcome! Whether it's bug reports, feature requests, or code contributions, please feel free to reach out or submit a pull request.
