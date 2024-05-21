# Constructor theory
Insipired by Constructor theory, Estuarine Mapping, Cynefin

Create constructors and visualize their output, see `main.py`

## Example
![](https://github.com/ThijmenVanBuuren/constructor_theory/raw/main/images/constructors_smoking.png)


```python
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
counterfactual_size = 2
easy_change_size = 2

plot_constructors(constructors=constructors, 
                    x_range=[0, 5], y_range=[0, 5], title=title,
                    counterfactual_diameter=counterfactual_size,
                    easy_change_diameter=easy_change_size)
```