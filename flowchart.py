from flowchart import Flowchart

# Create a new flowchart
flow = Flowchart()

# Define nodes
flow.start()
flow.add_operation("Initialize sum = 0")
flow.add_operation("Initialize i = 1")
flow.decision("i > 10")
flow.add_operation("Print i")
flow.add_operation("sum = sum + i")
flow.add_operation("i = i + 1")
flow.end()

# Define connections between nodes
flow.connect("start", "Initialize sum = 0")
flow.connect("Initialize sum = 0", "Initialize i = 1")
flow.connect("Initialize i = 1", "i > 10", "no")
flow.connect("i > 10", "end", "yes")
flow.connect("i > 10", "Print 'Sum of the first 10 natural numbers is:', sum", "no")
flow.connect("Print i", "sum = sum + i")
flow.connect("sum = sum + i", "i = i + 1")
flow.connect("i = i + 1", "i > 10")

# Draw the flowchart
flow.draw("flowchart.png")

