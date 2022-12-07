# from matplotlib.widgets import RectangleSelector
# import matplotlib.pyplot as plt
#
#
# # Function to be executed after selection
# def onselect_function(eclick, erelease):
#     # Obtain (xmin, xmax, ymin, ymax) values
#     # for rectangle selector box using extent attribute.
#     extent = rect_selector.extents
#     print("Extents: ", extent)
#
#     # Zoom the selected part
#     # Set xlim range for plot as xmin to xmax
#     # of rectangle selector box.
#     plt.xlim(extent[0], extent[1])
#
#     # Set ylim range for plot as ymin to ymax
#     # of rectangle selector box.
#     plt.ylim(extent[2], extent[3])
#
#
# # plot a line graph for data n
# fig, ax = plt.subplots()
# n = [4, 5, 6, 10, 12, 15, 20, 23, 24, 19]
# ax.plot(n)
#
# # Define a RectangleSelector at given axes ax.
# # It calls a function named 'onselect_function'
# # when the selection is completed.
# # Rectangular box is drawn to show the selected region.
# # Only left mouse button is allowed for doing selection.
# rect_selector = RectangleSelector(
#     ax, onselect_function, drawtype='box', button=[1])
#
# # Display graph
# plt.show()
