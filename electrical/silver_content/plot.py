# Calculating the relative increase in conductivity compared to 1g silver content
# First, find the mean conductivity for 1g silver content as the baseline
baseline_conductivity = aggregated_data[aggregated_data["Ag Content (g)"] == 1]["mean"].values[0]

# Calculate the relative increase (times increase over the baseline)
aggregated_data["Relative Increase"] = aggregated_data["mean"] / baseline_conductivity

# Plotting the relative increase
plt.figure(figsize=(10, 6))
plt.bar(aggregated_data['Category'], aggregated_data['Relative Increase'], color='lightgreen')
plt.title("Relative Increase in Conductivity vs Silver Content")
plt.xlabel("Silver Content (g)")
plt.ylabel("Relative Increase in Conductivity")
plt.xticks(aggregated_data['Category'], aggregated_data["Ag Content (g)"])  # Label x-ticks with actual silver content
plt.grid(axis='y')
plt.show()

