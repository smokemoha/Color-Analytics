import re
import random
import psycopg2
from collections import Counter
import statistics
import numpy as np
import os
from dotenv import load_dotenv
# Extract colors from the HTML file
def extract_colors_from_html(file_path):
    with open(file_path, 'r') as file:
        html_content = file.read()
        
    # Extract color data using regex
    day_pattern = r'<td>([A-Z]+)</td>'
    color_pattern = r'<td>((?:[A-Z]+(?:, )?)+)</td>'
    
    days = re.findall(day_pattern, html_content)
    color_data = re.findall(color_pattern, html_content)
    
    # Remove days from the color_data if they were captured
    color_data = [item for item in color_data if item not in days]
    
    # Process the color data
    all_colors = []
    for day_colors in color_data:
        colors = [color.strip() for color in day_colors.split(',')]
        all_colors.extend(colors)
    
    return all_colors

# 1. Mean color (most frequent)
def get_mean_color(colors):
    color_counts = Counter(colors)
    return color_counts.most_common(1)[0][0]

# 2. Most worn color throughout the week
def get_most_worn_color(colors):
    color_counts = Counter(colors)
    return color_counts.most_common(1)[0][0]

# 3. Median color
def get_median_color(colors):
    # Sort colors alphabetically
    sorted_colors = sorted(colors)
    # Get the middle color
    median_index = len(sorted_colors) // 2
    return sorted_colors[median_index]

# 4. Variance of colors
def get_color_variance(colors):
    color_counts = Counter(colors)
    frequencies = list(color_counts.values())
    return np.var(frequencies)

# 5. Probability of choosing red
def get_red_probability(colors):
    red_count = colors.count('RED')
    total_count = len(colors)
    return red_count / total_count

# 6. Save colors and frequencies to PostgreSQL
def save_to_postgresql(colors):
    try:
        # Load environment variables
        load_dotenv()
        
        # Get database connection details from environment variables
        db_name = os.getenv('DB_NAME', 'color_analysis')
        db_user = os.getenv('DB_USER', 'postgres')
        db_password = os.getenv('DB_PASSWORD')
        db_host = os.getenv('DB_HOST', 'localhost')
        
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host
        )
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS color_frequencies (
                color VARCHAR(50) PRIMARY KEY,
                frequency INTEGER
            )
        """)
        
        # Insert color frequencies
        color_counts = Counter(colors)
        for color, frequency in color_counts.items():
            cursor.execute(
                "INSERT INTO color_frequencies (color, frequency) VALUES (%s, %s) ON CONFLICT (color) DO UPDATE SET frequency = %s",
                (color, frequency, frequency)
            )
        
        conn.commit()
        print("Data saved to PostgreSQL successfully")
        
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

# ... rest of the code remains unchanged ...

# 7. Recursive searching algorithm
def recursive_search(numbers, target, start=0, end=None):
    if end is None:
        end = len(numbers) - 1
    
    if start > end:
        return -1
    
    mid = (start + end) // 2
    
    if numbers[mid] == target:
        return mid
    elif numbers[mid] > target:
        return recursive_search(numbers, target, start, mid - 1)
    else:
        return recursive_search(numbers, target, mid + 1, end)

# 8. Generate random 4 digits of 0s and 1s and convert to base 10
def generate_binary_and_convert():
    binary = ''.join(random.choice(['0', '1']) for _ in range(4))
    decimal = int(binary, 2)
    return binary, decimal

# 9. Sum of first 50 Fibonacci numbers
def fibonacci_sum(n):
    if n <= 0:
        return 0
    
    fib = [0, 1]
    for i in range(2, n+1):
        fib.append(fib[i-1] + fib[i-2])
    
    return sum(fib[:n+1])

def main():

    # Extract colors from HTML
    # Use relative path for the HTML file in the same directory
    html_file_path = os.path.join(os.path.dirname(__file__), 'python_test.html')
    colors = extract_colors_from_html(html_file_path)
    
    # Fix any potential typos in the color data
    colors = [color.upper() for color in colors]
    colors = [color.replace('BLEW', 'BLUE').replace('ARSH', 'ASH') for color in colors]
    print(f"Total colors extracted: {len(colors)}")
    print(f"Unique colors: {set(colors)}")
    
    # 1. Mean color
    mean_color = get_mean_color(colors)
    print(f"\n1. Mean color: {mean_color}")
    
    # 2. Most worn color
    most_worn = get_most_worn_color(colors)
    print(f"2. Most worn color: {most_worn}")
    
    # 3. Median color
    median_color = get_median_color(colors)
    print(f"3. Median color: {median_color}")
    
    # 4. Variance of colors
    variance = get_color_variance(colors)
    print(f"4. Variance of colors: {variance:.2f}")
    
    # 5. Probability of choosing red
    red_prob = get_red_probability(colors)
    print(f"5. Probability of choosing red: {red_prob:.4f} ({red_prob*100:.2f}%)")
    
    # 6. Save to PostgreSQL
    print("\n6. Saving to PostgreSQL...")
    save_to_postgresql(colors)
    
    # 7. Recursive search demo
    print("\n7. Recursive search demonstration:")
    numbers = sorted([random.randint(1, 100) for _ in range(20)])
    target = random.choice(numbers)
    print(f"   Numbers: {numbers}")
    print(f"   Searching for: {target}")
    result = recursive_search(numbers, target)
    print(f"   Found at index: {result}")
    
    # Interactive search
    user_target = int(input("\nEnter a number to search for: "))
    result = recursive_search(numbers, user_target)
    if result != -1:
        print(f"Found {user_target} at index {result}")
    else:
        print(f"{user_target} not found in the list")
    
    # 8. Generate binary and convert to decimal
    binary, decimal = generate_binary_and_convert()
    print(f"\n8. Random 4-digit binary: {binary}")
    print(f"   Converted to decimal: {decimal}")
    
    # 9. Sum of first 50 Fibonacci numbers
    fib_sum = fibonacci_sum(50)
    print(f"\n9. Sum of first 50 Fibonacci numbers: {fib_sum}")

if __name__ == "__main__":
    main()