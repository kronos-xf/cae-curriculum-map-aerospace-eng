import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# ------------------ SAMPLE DATA ------------------ #
courses = {
    "MATH 12002": {"name": "Calculus I", "prereqs": []},
    "MATH 12003": {"name": "Calculus II", "prereqs": ["MATH 12002"]},
    "PHY 23101": {"name": "Physics I", "prereqs": ["MATH 12002"]},
    "PHY 23102": {"name": "Physics II", "prereqs": ["PHY 23101"]},
    "ENGR 25200": {"name": "Statics", "prereqs": ["PHY 23101"]},
    "ENGR 25400": {"name": "Dynamics", "prereqs": ["ENGR 25200"]},
    "ENGR 25500": {"name": "Aero I", "prereqs": ["ENGR 25400"]},
    "ENGR 35600": {"name": "Aero II", "prereqs": ["ENGR 25500"]},
    "ENGR 45600": {"name": "Stability II", "prereqs": ["ENGR 35600"]},
    "ENGR 48099": {"name": "Capstone I", "prereqs": []},
    "ENGR 48199": {"name": "Capstone II", "prereqs": ["ENGR 48099"]},
}

# ------------------ BUILD GRAPH ------------------ #
G = nx.DiGraph()

for course, details in courses.items():
    G.add_node(course, label=details["name"])
    for prereq in details["prereqs"]:
        G.add_edge(prereq, course)

# ------------------ STREAMLIT UI ------------------ #
st.title("CAE Curriculum Map Viewer")

selected = st.selectbox("Select a course to trace its impact:", list(courses.keys()))

# DFS to find downstream nodes
def get_all_downstream(graph, start_node):
    visited = set()
    stack = [start_node]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            stack.extend(graph.successors(node))
    visited.remove(start_node)
    return visited

downstream = get_all_downstream(G, selected)

# ------------------ DRAWING ------------------ #
fig, ax = plt.subplots(figsize=(10, 6))
pos = nx.spring_layout(G, seed=42)

node_colors = []
for node in G.nodes():
    if node == selected:
        node_colors.append("orange")
    elif node in downstream:
        node_colors.append("lightgreen")
    else:
        node_colors.append("lightblue")

nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=2000, font_size=8, ax=ax)
plt.title(f"Dependencies from {selected}")
st.pyplot(fig)

st.caption("Orange = selected course | Green = courses that depend on it")
