import re  # Regular expression library for pattern matching in strings (e.g., extracting data from HTML)
import random  # Library for generating random numbers or choices (e.g., binary digits or demo numbers)
import psycopg2  # Library to connect and interact with PostgreSQL databases
from collections import Counter  # A tool to count occurrences of items in a list (e.g., color frequencies)
import statistics  # Library for statistical calculations (not used here, but imported)
import numpy as np  # Library for numerical operations, like calculating variance
import os  # Library for operating system tasks, like handling file paths
from dotenv import load_dotenv  # Loads environment variables from a .env file for secure configuration

# Function to extract colors from an HTML file
def extract_colors_from_html(file_path):
    # Open the HTML file in read mode ('r') to access its content
    with open(file_path, 'r') as file:
        html_content = file.read()  # Read the entire file into a single string
        
    # Define patterns to find specific data in HTML using regex
    day_pattern = r'<td>([A-Z]+)</td>'  # Matches uppercase words (e.g., days) between <td> tags
    color_pattern = r'<td>((?:[A-Z]+(?:, )?)+)</td>'  # Matches one or more uppercase words (colors) separated by commas
    
    # Extract all matches for days and colors from the HTML content
    days = re.findall(day_pattern, html_content)  # List of days found (e.g., ["MONDAY", "TUESDAY"])
    color_data = re.findall(color_pattern, html_content)  # List of color strings (e.g., ["RED, BLUE", "GREEN"])
    
    # Filter out any day names that might have been accidentally captured in color_data
    color_data = [item for item in color_data if item not in days]
    
    # Process the color data into a single list of individual colors
    all_colors = []  # Empty list to store all colors
    for day_colors in color_data:  # Loop through each day's color string (e.g., "RED, BLUE")
        colors = [color.strip() for color in day_colors.split(',')]  # Split by comma and remove extra spaces
        all_colors.extend(colors)  # Add each color to the all_colors list
    
    return all_colors  # Return the complete list of colors (e.g., ["RED", "BLUE", "GREEN"])

# Function to find the "mean" color (most frequent color in this context)
def get_mean_color(colors):
    color_counts = Counter(colors)  # Count how many times each color appears (e.g., {"RED": 3, "BLUE": 2})
    return color_counts.most_common(1)[0][0]  # Get the most frequent color (e.g., "RED")

# Function to find the most worn color (same as mean color here)
def get_most_worn_color(colors):
    color_counts = Counter(colors)  # Count occurrences of each color
    return color_counts.most_common(1)[0][0]  # Return the color with the highest count

# Function to find the median color (middle color when sorted)
def get_median_color(colors):
    sorted_colors = sorted(colors)  # Sort the colors alphabetically (e.g., ["BLUE", "GREEN", "RED"])
    median_index = len(sorted_colors) // 2  # Find the middle index using integer division
    return sorted_colors[median_index]  # Return the color at the middle position

# Function to calculate the variance of color frequencies
def get_color_variance(colors):
    color_counts = Counter(colors)  # Get frequency of each color
    frequencies = list(color_counts.values())  # List of counts (e.g., [3, 2, 1] for 3 RED, 2 BLUE, 1 GREEN)
    return np.var(frequencies)  # Calculate variance using NumPy (measures how spread out the frequencies are)

# Function to calculate the probability of choosing "RED"
def get_red_probability(colors):
    red_count = colors.count('RED')  # Count how many times "RED" appears in the list
    total_count = len(colors)  # Total number of colors in the list
    return red_count / total_count  # Probability = number of REDs divided by total colors

# Function to save color frequencies to a PostgreSQL database
def save_to_postgresql(colors):
    try:
        # Load environment variables from a .env file (e.g., database credentials)
        load_dotenv()
        
        # Retrieve database connection details from environment variables, with defaults if not set
        db_name = os.getenv('DB_NAME', 'color_analysis')  # Database name
        db_user = os.getenv('DB_USER', 'postgres')  # Database user
        db_password = os.getenv('DB_PASSWORD')  # Database password
        db_host = os.getenv('DB_HOST', 'localhost')  # Database host
        
        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host
        )
        cursor = conn.cursor()  # Create a cursor to execute SQL commands
        
        # Create a table to store colors and their frequencies if it doesn’t already exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS color_frequencies (
                color VARCHAR(50) PRIMARY KEY,  -- Color name as the unique key
                frequency INTEGER  -- How many times the color appears
            )
        """)
        
        # Insert or update color frequencies in the table
        color_counts = Counter(colors)  # Count each color’s occurrences
        for color, frequency in color_counts.items():  # Loop through each color and its count
            cursor.execute(
                # SQL command to insert or update the frequency if the color already exists
                "INSERT INTO color_frequencies (color, frequency) VALUES (%s, %s) ON CONFLICT (color) DO UPDATE SET frequency = %s",
                (color, frequency, frequency)  # Parameters: color name, count, and count again for update
            )
        
        conn.commit()  # Save the changes to the database
        print("Data saved to PostgreSQL successfully")  # Confirmation message
        
    except Exception as e:
        print(f"Database error: {e}")  # Print any error that occurs (e.g., connection failure)
    finally:
        if conn:  # If a connection was established
            cursor.close()  # Close the cursor
            conn.close()  # Close the database connection

# Recursive function to search for a target number in a sorted list
def recursive_search(numbers, target, start=0, end=None):
    if end is None:  # If end isn’t provided, set it to the last index
        end = len(numbers) - 1
    
    if start > end:  # Base case: if start exceeds end, target isn’t in the list
        return -1
    
    mid = (start + end) // 2  # Calculate the middle index of the current range
    
    if numbers[mid] == target:  # If the middle element is the target, return its index
        return mid
    elif numbers[mid] > target:  # If middle element is too high, search the left half
        return recursive_search(numbers, target, start, mid - 1)
    else:  # If middle element is too low, search the right half
        return recursive_search(numbers, target, mid + 1, end)

# Function to generate a 4-digit binary number and convert it to decimal
def generate_binary_and_convert():
    binary = ''.join(random.choice(['0', '1']) for _ in range(4))  # Create a 4-digit binary string (e.g., "1011")
    decimal = int(binary, 2)  # Convert binary string to decimal (base 2 to base 10)
    return binary, decimal  # Return both the binary string and its decimal value

# Function to calculate the sum of the first n Fibonacci numbers
def fibonacci_sum(n):
    if n <= 0:  # If n is 0 or negative, return 0 (no numbers to sum)
        return 0
    
    fib = [0, 1]  # Start with the first two Fibonacci numbers
    for i in range(2, n+1):  # Generate subsequent Fibonacci numbers up to n
        fib.append(fib[i-1] + fib[i-2])  # Each number is the sum of the two before it
    
    return sum(fib[:n+1])  # Return the sum of the first n+1 Fibonacci numbers

# Main function to run the program
def main():
    # Define the path to the HTML file in the same directory as this script
    html_file_path = os.path.join(os.path.dirname(__file__), 'python_test.html')
    colors = extract_colors_from_html(html_file_path)  # Extract colors from the HTML file
    
    # Clean up the color data
    colors = [color.upper() for color in colors]  # Convert all colors to uppercase for consistency
    colors = [color.replace('BLEW', 'BLUE').replace('ARSH', 'ASH') for color in colors]  # Fix common typos
    print(f"Total colors extracted: {len(colors)}")  # Show how many colors were found
    print(f"Unique colors: {set(colors)}")  # Show the set of unique colors
    
    # 1. Calculate and display the mean (most frequent) color
    mean_color = get_mean_color(colors)
    print(f"\n1. Mean color: {mean_color}")
    
    # 2. Calculate and display the most worn color (same as mean here)
    most_worn = get_most_worn_color(colors)
    print(f"2. Most worn color: {most_worn}")
    
    # 3. Calculate and display the median color
    median_color = get_median_color(colors)
    print(f"3. Median color: {median_color}")
    
    # 4. Calculate and display the variance of color frequencies
    variance = get_color_variance(colors)
    print(f"4. Variance of colors: {variance:.2f}")  # Format to 2 decimal places
    
    # 5. Calculate and display the probability of choosing red
    red_prob = get_red_probability(colors)
    print(f"5. Probability of choosing red: {red_prob:.4f} ({red_prob*100:.2f}%)")  # Show as decimal and percentage
    
    # 6. Save the color data to PostgreSQL
    print("\n6. Saving to PostgreSQL...")
    save_to_postgresql(colors)
    
    # 7. Demonstrate recursive search with a random list
    print("\n7. Recursive search demonstration:")
    numbers = sorted([random.randint(1, 100) for _ in range(20)])  # Create a sorted list of 20 random numbers
    target = random.choice(numbers)  # Pick a random number from the list to search for
    print(f"   Numbers: {numbers}")
    print(f"   Searching for: {target}")
    result = recursive_search(numbers, target)
    print(f"   Found at index: {result}")
    
    # Allow the user to search for a number interactively
    user_target = int(input("\nEnter a number to search for: "))  # Get user input
    result = recursive_search(numbers, user_target)  # Search for the user’s number
    if result != -1:  # If the number was found
        print(f"Found {user_target} at index {result}")
    else:  # If the number wasn’t found
        print(f"{user_target} not found in the list")
    
    # 8. Generate and display a random binary number and its decimal equivalent
    binary, decimal = generate_binary_and_convert()
    print(f"\n8. Random 4-digit binary: {binary}")
    print(f"   Converted to decimal: {decimal}")
    
    # 9. Calculate and display the sum of the first 50 Fibonacci numbers
    fib_sum = fibonacci_sum(50)
    print(f"\n9. Sum of first 50 Fibonacci numbers: {fib_sum}")

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()