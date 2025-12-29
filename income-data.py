import matplotlib.pyplot as plt
import math

income_values = []

print("Enter expected annual incomes one by one.")
print("Type STOP when finished.\n")

while True:
    val = input("Income: ")
    if val.lower() == "stop":
        break
    income_values.append(float(val))

values = income_values[:]

n = len(values)
mean_income = sum(values) / n
std_income = math.sqrt(sum((x - mean_income) ** 2 for x in values) / n)

bls_input = input("Enter BLS weekly earnings (press Enter for default 1754): ")
if bls_input == "":
    BLS_WEEKLY = 1754
else:
    BLS_WEEKLY = float(bls_input)

BLS_ANNUAL = BLS_WEEKLY * 52
realistic_std = BLS_ANNUAL * 0.30

x_min = min(min(values), BLS_ANNUAL - 3 * realistic_std)
x_max = max(max(values), BLS_ANNUAL + 3 * realistic_std)

x_vals = []
step = (x_max - x_min) / 500.0
x = x_min
while x <= x_max:
    x_vals.append(x)
    x += step

pdf_student = []
pdf_bls = []

for x in x_vals:
    student_y = (1.0 / (std_income * math.sqrt(2 * math.pi))) * math.exp(-0.5 * ((x - mean_income) / std_income) ** 2)
    bls_y = (1.0 / (realistic_std * math.sqrt(2 * math.pi))) * math.exp(-0.5 * ((x - BLS_ANNUAL) / realistic_std) ** 2)
    pdf_student.append(student_y)
    pdf_bls.append(bls_y)

scale_factor = n * (x_max - x_min) / 30
pdf_student_scaled = [y * scale_factor for y in pdf_student]
pdf_bls_scaled = [y * scale_factor for y in pdf_bls]

plt.figure(figsize=(10, 6))
plt.hist(values, bins=30, alpha=0.6, edgecolor="black", label="Student Expected Income")
plt.plot(x_vals, pdf_student_scaled, linewidth=2, label="Bell Curve (Student Data)")
plt.plot(x_vals, pdf_bls_scaled, linewidth=2, linestyle="--", label="Realistic Income Curve (BLS)")
plt.axvline(BLS_ANNUAL, linestyle=":", linewidth=2, label="BLS Median")
plt.xlabel("Annual Income (USD)")
plt.ylabel("Frequency / Density")
plt.title("Expected Income vs Realistic BLS Earnings")
plt.legend()
plt.tight_layout()
plt.show()

labels = ["Student Mean (Expected)", "BLS Median (Real)"]
values_bar = [mean_income, BLS_ANNUAL]

plt.figure(figsize=(8, 6))
bars = plt.bar(labels, values_bar)
for i, v in enumerate(values_bar):
    plt.text(i, v + 0.02 * max(values_bar), "${:,.0f}".format(v), ha="center", va="bottom", fontsize=10)

plt.ylabel("Annual Income (USD)")
plt.title("Average Expected Income vs BLS Median Income")
plt.tight_layout()
plt.show()
