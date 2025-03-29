# Color Analytics Engine 

A comprehensive solution for processing color data from HTML sources, performing statistical analysis, and managing color frequency data in PostgreSQL. Developed as a technical assessment solution for Bincom ICT.

## Features

- HTML Color Extraction: Automated parsing of color data from HTML tables
- *dvanced Analytics*:
  - Frequency analysis (mean/mode)
  - Median color determination
  - Variance calculation
  - Probability modeling
- **Database Integration**: PostgreSQL storage with conflict-aware upserts
- **Algorithm Suite**:
  - Recursive binary search
  - Fibonacci sequence summation
  - Binary number generation/conversion

## Installation
```bash
git clone https://github.com/smokemohaE/Color-Analytics.git
cd ColorAnalytics
pip install -r requirements.txt
```
## Requirements
- Python 3.8+
- PostgreSQL 12+
- Required packages:
  ```bash
  psycopg2-binary
  numpy
  python-dotenv
   ```
## Configuration
1. Create .env file:
```ini
DB_NAME=color_analysis
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=localhost
 ```

## Database setup
```bash
createdb color_analysis
 ```

## Usage
```python
python color_analysis.py
 ```


## Sample output
```bash
Total colors extracted: 142
Unique colors: {'RED', 'BLUE', 'GREEN', 'YELLOW'}
1. Mean color: BLUE
2. Most worn color: BLUE
3. Median color: GREEN
4. Variance: 0.000000
5. Probability of RED: 0.000000
6. Fibonacci sum: 144
7. Binary representation of 10: 1010
 ```