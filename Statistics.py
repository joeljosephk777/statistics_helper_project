import matplotlib.pyplot as plt

def bubble_sort(arr):
    """Sort array using bubble sort algorithm"""
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def calculate_mean(arr):
    """Calculate the mean (average)"""
    return sum(arr) / len(arr)

def calculate_median(arr):
    """Calculate the median (middle value)"""
    n = len(arr)
    if n % 2 == 0:
        return (arr[n // 2 - 1] + arr[n // 2]) / 2
    else:
        return arr[n // 2]

def calculate_mode(arr):
    """Calculate the mode (most frequent value)"""
    frequency = {}
    for num in arr:
        frequency[num] = frequency.get(num, 0) + 1
    
    max_freq = max(frequency.values())
    modes = [num for num, freq in frequency.items() if freq == max_freq]
    
    if len(modes) == len(frequency):
        return "No mode (all values appear equally)"
    return modes if len(modes) > 1 else modes[0]

def calculate_variance(arr, mean):
    """Calculate the variance OF A SAMPLE"""
    return sum((x - mean) ** 2 for x in arr) / (len(arr)-1)

def calculate_standard_deviation(variance):
    """Calculate the standard deviation OF A SAMPLE"""
    return variance ** 0.5

def calculate_range(arr):
    """Calculate the range (max - min)"""
    return max(arr) - min(arr)

def calculate_intervals(mean, std_dev):
    """Calculate x̄ ± s, x̄ ± 2s, x̄ ± 3s intervals"""
    intervals = {}
    
    # x̄ ± s
    intervals['1s'] = (mean - std_dev, mean + std_dev)
    
    # x̄ ± 2s
    intervals['2s'] = (mean - 2*std_dev, mean + 2*std_dev)
    
    # x̄ ± 3s
    intervals['3s'] = (mean - 3*std_dev, mean + 3*std_dev)
    
    return intervals

def count_values_in_intervals(arr, intervals):
    """Count how many values fall within each interval and calculate percentages"""
    total = len(arr)
    counts = {}
    percentages = {}
    
    for key, (lower, upper) in intervals.items():
        count = sum(1 for x in arr if lower <= x <= upper)
        counts[key] = count
        percentages[key] = (count / total) * 100
    
    return counts, percentages

def calculate_quartiles(arr):
    """Calculate Q1, Q2 (median), Q3"""
    n = len(arr)
    q2 = calculate_median(arr)
    
    # Q1 is median of lower half
    lower_half = arr[:n//2]
    q1 = calculate_median(lower_half)
    
    # Q3 is median of upper half
    if n % 2 == 0:
        upper_half = arr[n//2:]
    else:
        upper_half = arr[n//2 + 1:]
    q3 = calculate_median(upper_half)
    
    return q1, q2, q3

def create_visualizations(arr, mean, std_dev, q1, median, q3):
    """Create box plot and histogram using matplotlib"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Box Plot
    bp = ax1.boxplot(arr, vert=False, patch_artist=True,
                     boxprops=dict(facecolor='lightblue', color='blue'),
                     whiskerprops=dict(color='blue'),
                     capprops=dict(color='blue'),
                     medianprops=dict(color='red', linewidth=2))
    ax1.set_xlabel('Values', fontsize=11)
    ax1.set_title('Box Plot', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Add statistics text to box plot
    stats_text = f'Min: {min(arr)}\nQ1: {q1}\nMedian: {median}\nQ3: {q3}\nMax: {max(arr)}'
    ax1.text(0.02, 0.98, stats_text, transform=ax1.transAxes,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
             fontsize=9)
    
    # 2. Histogram
    n, bins, patches = ax2.hist(arr, bins=6, edgecolor='black', color='skyblue', alpha=0.7)
    ax2.axvline(mean, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean:.2f}')
    ax2.axvline(median, color='green', linestyle='--', linewidth=2, label=f'Median: {median:.2f}')
    ax2.set_xlabel('Values', fontsize=11)
    ax2.set_ylabel('Frequency', fontsize=11)
    ax2.set_title('Histogram', fontsize=13, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    
    # 3. Normal Distribution Overlay
    ax3.hist(arr, bins=6, edgecolor='black', color='lightcoral', alpha=0.6, density=True, label='Data')
    
    # Plot normal curve
    import math
    x_min, x_max = min(arr), max(arr)
    x = [x_min + i * (x_max - x_min) / 100 for i in range(101)]
    y = [1/(std_dev * math.sqrt(2 * math.pi)) * math.exp(-0.5 * ((val - mean) / std_dev) ** 2) for val in x]
    ax3.plot(x, y, 'b-', linewidth=2, label='Normal Distribution')
    ax3.axvline(mean, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean:.2f}')
    ax3.set_xlabel('Values', fontsize=11)
    ax3.set_ylabel('Density', fontsize=11)
    ax3.set_title('Distribution with Normal Curve', fontsize=13, fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Interval Visualization
    intervals = calculate_intervals(mean, std_dev)
    interval_names = ['x̄ ± 1s', 'x̄ ± 2s', 'x̄ ± 3s']
    colors = ['#90EE90', '#87CEEB', '#FFB6C1']
    
    y_pos = 0.5
    for i, (name, key) in enumerate(zip(interval_names, ['1s', '2s', '3s'])):
        lower, upper = intervals[key]
        width = upper - lower
        ax4.barh(i, width, left=lower, height=0.6, color=colors[i], 
                edgecolor='black', alpha=0.7, label=name)
        
        # Add interval text
        ax4.text(mean, i, f'{name}', ha='center', va='center', 
                fontweight='bold', fontsize=9)
    
    # Plot data points
    ax4.scatter(arr, [3.5] * len(arr), color='red', s=100, zorder=5, 
               marker='o', edgecolors='black', linewidth=1.5, label='Data Points')
    
    # Mark mean
    ax4.axvline(mean, color='red', linestyle='--', linewidth=2, alpha=0.7)
    
    ax4.set_xlabel('Values', fontsize=11)
    ax4.set_yticks([0, 1, 2, 3.5])
    ax4.set_yticklabels(['x̄ ± 1s', 'x̄ ± 2s', 'x̄ ± 3s', 'Data'])
    ax4.set_title('Standard Deviation Intervals', fontsize=13, fontweight='bold')
    ax4.grid(True, alpha=0.3, axis='x')
    ax4.legend(loc='upper right')
    
    plt.tight_layout()
    plt.savefig('statistics_visualization.png', dpi=300, bbox_inches='tight')
    print("\n✓ Visualizations saved as 'statistics_visualization.png'")
    plt.show()

# Example usage - sample data set
numbers = [0.2, 2, 6, 10, 11, 13, 13, 17, 17, 23, 27, 28, 35, 64 ]


print(f"Original numbers: {numbers}")

# Sort using bubble sort
sorted_numbers = bubble_sort(numbers.copy())
print(f"Sorted numbers: {sorted_numbers}")

# Calculate statistics
mean = calculate_mean(sorted_numbers)
median = calculate_median(sorted_numbers)
mode = calculate_mode(sorted_numbers)
variance = calculate_variance(sorted_numbers, mean)
std_deviation = calculate_standard_deviation(variance)
range_value = calculate_range(sorted_numbers)

print(f"\nStatistics:")
print(f"number of elements:{len(numbers)}")
print(f"Mean: {mean:.4f}")
print(f"Median: {median}")
print(f"Mode: {mode}")
print(f"Range: {range_value}")
print(f"Variance: {variance:.4f}")
print(f"Standard Deviation: {std_deviation:.4f}")

intervals = calculate_intervals(mean, std_deviation)
print(f"\nIntervals:")
print(f"x̄ ± s  = ({intervals['1s'][0]:.3f}, {intervals['1s'][1]:.3f})")
print(f"x̄ ± 2s = ({intervals['2s'][0]:.3f}, {intervals['2s'][1]:.3f})")
print(f"x̄ ± 3s = ({intervals['3s'][0]:.3f}, {intervals['3s'][1]:.3f})")

counts, percentages = count_values_in_intervals(sorted_numbers, intervals)
print(f"\nValues within intervals:")
print(f"x̄ ± s:  {counts['1s']} values ({percentages['1s']:.2f}%)")
print(f"x̄ ± 2s: {counts['2s']} values ({percentages['2s']:.2f}%)")
print(f"x̄ ± 3s: {counts['3s']} values ({percentages['3s']:.2f}%)")

# Create beautiful visualizations
q1, q2, q3 = calculate_quartiles(sorted_numbers)
create_visualizations(sorted_numbers, mean, std_deviation, q1, median, q3)