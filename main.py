"""
@author Thijmen van Buuren
thijmendeveloper@gmail.com
https://github.com/ThijmenVanBuuren

Given a set of variables, each constructor adds or subtracts a value from them. 
Each constructor has energy and time costs for changing them. 
In a simulation: in each timestep, an agent can weaken or strengthen a constructor. 
This changes their time/energy and strength change for the variables.
"""

import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class Constructor:
    def __init__(self, energy, time, variable_output, name=""):
        self.energy = energy
        self.time = time
        self.name = name
        # List, strength output
        self.variable_output = variable_output

    def __call__(self):
        return self.output()

    def __str__(self):
        string=f"Energy: {self.energy} \n Time: {self.time} \n Output: {self.variable_output}"
        return string

    def output(self):
        return self.variable_output

    def change_output(self, variables):
        self.variable_output = [
            current_output + change 
            for current_output, change in zip(self.variable_output, variables)
        ]


def make_random_constructors(num_constructors=10):
    # Make Constructors
    # num_constructors = 10

    def generate_lognormal_values(mean, sigma, size):
        """Generates a list of log-normal values."""
        return [random.lognormvariate(mean, sigma) for _ in range(size)]


    def generate_gaussian_values(mean, sigma, size):
        """Generates a list of log-normal values."""
        return [random.gauss(mean, sigma) for _ in range(size)]

    energy_mean = 1
    energy_sd = 0.5
    time_mean = 1
    time_sd = 0.5
    output_mean = 0
    output_sd = 2

    energies = generate_lognormal_values(energy_mean, energy_sd, num_constructors)
    times = generate_lognormal_values(time_mean, time_sd, num_constructors)
    outputs = [generate_gaussian_values(output_mean, output_sd, len(variables)) for _ in range(num_constructors)]

    constructors = []
    for i in range(num_constructors):
        c = Constructor(energies[i], times[i], outputs[i])
        constructors.append(c)
    return constructors


# TODO:scale factor
def plot_constructors(constructors,
                      x_range=None, y_range=None, 
                      counterfactual_diameter=2, 
                      easy_change_diameter=2, title=""):
    """
    Plots the constructors based on their energy cost and time cost.
    x = time cost to change
    y = energy cost to change


    Args:
        constructors (list): A list of constructors.
        scale_factor (int): arbitrary
        x_range (List[int]): axis [x_min, x_max]
        y_range (List[int]): axis [y_min, y_max]
        counterfactual_diameter (float): size of counterfactual area
            centered on max_points of 
        easy_change_diameter (float): size of 
    """
    # Plot constructors
    energies = [c.energy for c in constructors]
    times = [c.time for c in constructors]
    output_sizes = [c.variable_output[0] for c in constructors]
    names = [c.name for c in constructors]
    # names = ["Hello, world!" for c in constructors]

    colors = []
    sizes = []
    scale_factor = 100
    for size in output_sizes:
        if size > 0:
            colors.append('green')
            sizes.append(size * scale_factor) 
        elif size < 0:
            colors.append('red')
            sizes.append(abs(size) * scale_factor)
        else:
            colors.append('black')
            sizes.append(1)

    # Set axis limits if given, else use extreme values
    min_point = [min(times), min(energies)]
    max_point = [max(times), max(energies)]
    if x_range is not None:
        plt.xlim(x_range)
        min_point[0] = x_range[0]
        max_point[0] = x_range[1]
    if y_range is not None:
        plt.ylim(y_range)
        min_point[1] = y_range[0]
        max_point[1] = y_range[1]

    # Create Legend based on color
    green_patch = mpatches.Patch(color='green', label='Positive effect')
    red_patch = mpatches.Patch(color='red', label='Negative effect')
    black_patch = mpatches.Patch(color='yellow', label='No effect')

    # Create Counterfactual area (top right) and easy change area (left bottom)
    # We just take the maximum point for now
    counterfactual = mpatches.Circle(tuple(max_point), counterfactual_diameter, 
                                     color='black', alpha=0.5, label='Counterfactuals')
    easy_change = mpatches.Circle(tuple(min_point), easy_change_diameter, color='blue', 
                                  alpha=0.5, label='Easy change')

    # Get current axes and add patches to them
    ax = plt.gca()
    ax.add_patch(counterfactual)
    ax.add_patch(easy_change)

    # Add constructor points
    plt.scatter(times, energies, s=sizes, c=colors)
    # Add constructor names
    for i, constructor_name in enumerate(names):
        plt.text(times[i], energies[i], constructor_name)

    plt.legend(handles=[green_patch, red_patch, black_patch, counterfactual, easy_change], loc="lower right")
    plt.xlabel('Time cost to change')
    plt.ylabel('Energy cost to change')
    if title == "":
        plt.title('Constructors')
    else:
        plt.title(title)
    plt.show()


if __name__ == "__main__":
    var_names = ["health", "positivity"]
    variables = [10.0, 5.0]

    # Todo: timesteps
    timesteps = 20

    # Random constructors
    constructors = make_random_constructors(num_constructors=10)

    # for c in constructors:
    #     print(c)

    title = "Random constructors"
    plot_constructors(constructors=constructors, x_range=[0, 5], y_range=[0, 5], title=title)


    #######
    # Constructors for smoking
    #######
    # Init constructors with names
    #   - Negative output values for bad constructors
    #   - Positive output values for good constructors
    # Set axis sizes
    # Set counterfactual and easy change size
    # Plot constructors
    constructors = [
        Constructor(energy=2, time=4, variable_output=[-5], name="Peer Pressure"),
        Constructor(energy=1, time=4, variable_output=[-4], name="Stress"),
        Constructor(energy=4.5, time=4, variable_output=[-3], name="Addiction"),
        Constructor(energy=4, time=1, variable_output=[-2], name="Advertisements"),
        Constructor(energy=5, time=4.5, variable_output=[-1], name="Social Acceptance"),
        Constructor(energy=1, time=1, variable_output=[5], name="Health Awareness"),
        Constructor(energy=2, time=2, variable_output=[4], name="Support Groups"),
        Constructor(energy=3, time=3, variable_output=[3], name="Nicotine Patches"),
        Constructor(energy=4, time=4, variable_output=[2], name="Therapy"),
        Constructor(energy=2, time=3, variable_output=[1], name="Exercise"),
    ]
    title = "Constructors Smoking"
    plot_constructors(constructors=constructors, x_range=[0, 5], y_range=[0, 5], title=title)
