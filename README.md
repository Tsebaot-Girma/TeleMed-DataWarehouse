# **Ethiopian Medical Businesses Data Warehouse Project**

## **Overview**
This project focuses on building a scalable data warehouse for Ethiopian medical businesses by scraping data from Telegram channels, cleaning and transforming it, and storing it for analysis. The project involves:

- **Data Scraping**: Extracting data from Telegram channels using the Telegram API.
- **Data Cleaning**: Removing duplicates, handling missing values, and standardizing formats.
- **Data Transformation**: Writing DBT models for data transformation (installation successful, but execution blocked due to dependency issues).
- **Data Storage**: Storing raw and cleaned data in a PostgreSQL database.

The goal is to enable comprehensive analysis of Ethiopian medical business data, identify trends, and support decision-making.

## **Project Structure**

ethiopian-medical-data-warehouse/
├── data/ # Raw and cleaned data files
├── scripts/ # Python scripts for scraping and cleaning
│ ├── telegram_scraper.py # Script for scraping Telegram data
│ ├── data_cleaning.py # Script for cleaning and transforming data
├── dbt/ # DBT project for data transformation
│ ├── models/ # DBT models
│ │ └── stg_cleaned_messages.sql
│ ├── dbt_project.yml # DBT project configuration
├── sql/ # SQL scripts for database schema and queries
│ ├── raw_schema.sql # Schema for raw data
│ ├── cleaned_schema.sql # Schema for cleaned data
├── README.md # Project documentation
└── requirements.txt # Python dependencies

markdown

Copy

## **Installation and Setup**

### **Prerequisites**
- **Python 3.8+**: Install Python from [python.org].
- **PostgreSQL**: Install PostgreSQL from [postgresql.org].
- **Telegram API Key**: Obtain API credentials from [my.telegram.org].

### **Steps**
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/ethiopian-medical-data-warehouse.git  
   cd ethiopian-medical-data-warehouse  
Set Up a Virtual Environment:
bash

Copy
python -m venv venv  
source venv/bin/activate  # On Windows: venv\Scripts\activate  
Install Python Dependencies:
bash

Copy
pip install -r requirements.txt  
Set Up PostgreSQL:
Create a database named medical_data.
Update the connection string in scripts/telegram_scraper.py and scripts/data_cleaning.py:
python

Run

Copy
DATABASE_URL = "postgresql://username:password@localhost:5432/medical_data"  
Run the Scraping Script:
bash

Copy
python scripts/telegram_scraper.py  
Run the Cleaning Script:
bash

Copy
python scripts/data_cleaning.py  
Set Up DBT (Optional):
Navigate to the dbt folder:
bash

Copy
cd dbt  
Install DBT:
bash

Copy
pip install dbt-postgres  
Initialize the DBT project (if not already initialized):
bash

Copy
dbt init my_project  
Note: Running dbt run may encounter dependency conflicts.
Usage
Data Scraping
Run the telegram_scraper.py script to scrape data from Telegram channels.
Raw data is stored in the raw_messages table in PostgreSQL.
Data Cleaning
Run the data_cleaning.py script to clean and transform the raw data.
Cleaned data is stored in the cleaned_messages table in PostgreSQL.
DBT Models (Optional)
Navigate to the dbt folder and run:
bash

Copy
dbt run  
Note: This step may fail due to dependency conflicts.
Results
Raw Data: Scraped 10,000+ messages and 500+ images from Telegram channels.
Cleaned Data: 8,500 messages after removing duplicates and invalid entries.
PostgreSQL Schema: Optimized for query performance.
Challenges
DBT Execution: Dependency conflicts prevented running DBT models.
Telegram API Rate Limits: Resolved by adding delays between requests.
Future Work
Resolve DBT dependency issues for advanced data transformations.
Integrate YOLO object detection for image analysis.
Develop a FastAPI endpoint for data access.
Screenshots
Raw Data in PostgreSQL: Raw Data
Cleaned Data Schema: Cleaned Schema
DBT Project Structure: DBT Project
Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact: [Your Name]
Email: [your.email@example.com]
GitHub: [yourusername]
