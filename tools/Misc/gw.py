# Budget and costs
budget = 224
ice_cream_cost = 4.50
chicken_cost = 8
total_days = 18

# Calculate maximum ice cream-only days
# Let x = ice cream only days
# y = ice cream + chicken days
# 4.5*x + 12.5*y = budget and x + y = 30

# Using equations:
# 4.5*x + 12.5*(30-x) = 290
# Solve for x
x = (12.5 * total_days - budget) / (12.5 - 4.5)
y = total_days - x

print(f"Approximate solution:")
print(f"Ice cream only days: {x:.2f}")
print(f"Ice cream + chicken days: {y:.2f}")

# Practical integer solution
x_int = int(x)  # round down to nearest day
y_int = total_days - x_int
total_cost = ice_cream_cost*x_int + (ice_cream_cost + chicken_cost)*y_int

print(f"\nPractical integer solution:")
print(f"Ice cream only days: {x_int}")
print(f"Ice cream + chicken days: {y_int}")
print(f"Total cost: ${total_cost:.2f}")