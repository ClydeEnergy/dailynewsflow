#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daily_news_flow.settings')
django.setup()

from django.db import connection

def check_database_structure():
    cursor = connection.cursor()
    
    # Check NewsProvider table structure
    print("=== NewsProvider Table Structure ===")
    cursor.execute('DESCRIBE news_newsprovider')
    rows = cursor.fetchall()
    for row in rows:
        print(f"{row[0]:<20} {row[1]:<15} {str(row[2]):<5} {str(row[3]):<5} {str(row[4]):<10} {str(row[5])}")
    
    print("\n=== All Tables with 'market' in name ===")
    cursor.execute("SHOW TABLES LIKE '%market%'")
    rows = cursor.fetchall()
    for row in rows:
        print(row[0])
    
    print("\n=== All news_ Tables ===")
    cursor.execute("SHOW TABLES LIKE 'news_%'")
    rows = cursor.fetchall()
    for row in rows:
        print(row[0])

if __name__ == "__main__":
    check_database_structure()
