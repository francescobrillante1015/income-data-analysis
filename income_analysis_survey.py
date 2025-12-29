import matplotlib.pyplot as plt
import math

income_values = []

income_values += [15000] * 2
income_values += [50000] * 3
income_values += [70000] * 15
income_values += [90000] * 23
income_values += [125000] * 20
income_values += [175000] * 7
income_values += [210000] * 13

values = income_values[:]

n = len(values)
mean_income = sum(values) / n
std_income = math.sqrt(sum((x - mean_income) ** 2 for x in values) / n)

BLS_WEEKLY = 1754
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
plt.hist(values, bins=30, alpha=0.6, color="skyblue", edgecolor="black", label="Student Expected Income")
plt.plot(x_vals, pdf_student_scaled, color="blue", linewidth=2, label="Bell Curve (Student Data)")
plt.plot(x_vals, pdf_bls_scaled, color="orange", linewidth=2, linestyle="--", label="Realistic Income Curve (BLS)")
plt.axvline(BLS_ANNUAL, color="red", linestyle=":", linewidth=2, label="BLS Median (~$91k)")
plt.xlabel("Annual Income (USD)")
plt.ylabel("Frequency / Density")
plt.title("Expected Income vs Realistic BLS Earnings")
plt.legend()
plt.tight_layout()
plt.show()

labels = ["Student Mean (Expected)", "BLS Median (Real)"]
values_bar = [mean_income, BLS_ANNUAL]

plt.figure(figsize=(8, 6))
bars = plt.bar(labels, values_bar, color=["skyblue", "orange"])
for i, v in enumerate(values_bar):
    plt.text(i, v + 0.02 * max(values_bar), "${:,.0f}".format(v), ha="center", va="bottom", fontsize=10)

plt.ylabel("Annual Income (USD)")
plt.title("Average Expected Income vs BLS Median Income")
plt.tight_layout()
plt.show()
