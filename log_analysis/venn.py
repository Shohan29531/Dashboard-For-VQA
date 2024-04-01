from matplotlib import pyplot as plt
from matplotlib_venn import venn2, venn2_circles
import matplotlib.patches as patches

# Define the sizes of the sets
set1_size = 1.5
set2_size = 1.5
overlap_size = 1

# Set the figure size
plt.figure(figsize=(10, 10))

# Create a Venn diagram
venn = venn2(subsets=(set1_size, set2_size, overlap_size),
             set_labels=('Set 1', 'Set 2'))

# Customize the colors of the circles and the overlap
venn.get_patch_by_id('10').set_color('skyblue')  # set1
venn.get_patch_by_id('01').set_color('lightgreen')  # set2
venn.get_patch_by_id('11').set_color('salmon')  # overlap

# Customize the linewidth of the circle edges
venn2_circles(subsets=(set1_size, set2_size, overlap_size), linestyle='solid')

# Get the positions and sizes of the circles
circle1_pos = venn.get_circle_center(0)
circle2_pos = venn.get_circle_center(1)
circle_radius = min(venn.get_circle_radius(0), venn.get_circle_radius(1))

# Calculate the dimensions of the rectangle
x_min = min(circle1_pos[0] - circle_radius, circle2_pos[0] - circle_radius)
x_max = max(circle1_pos[0] + circle_radius, circle2_pos[0] + circle_radius)
y_min = min(circle1_pos[1] - circle_radius, circle2_pos[1] - circle_radius)
y_max = max(circle1_pos[1] + circle_radius, circle2_pos[1] + circle_radius)

# Draw a rectangle around the Venn diagram
rect_width = x_max - x_min + 3
rect_height = y_max - y_min + 3
rect = patches.Rectangle((x_min, y_min), rect_width, rect_height, linewidth=2, edgecolor='black', facecolor='none')
plt.gca().add_patch(rect)

# Add a title
plt.title("Venn Diagram")

# Show the plot
plt.show()
