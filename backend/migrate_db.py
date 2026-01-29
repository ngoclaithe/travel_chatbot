import sys
import os
# Add the current directory to sys.path so we can import app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.core.config import settings
except ImportError as e:
    print(f"Error importing settings: {e}")
    # Fallback/Hardcoded if strictly necessary or ask user to check env
    sys.exit(1)

import psycopg2
from urllib.parse import urlparse

def migrate():
    print(f"Starting migration...")
    
    url = settings.DATABASE_URL
    print(f"Database URL found (masked): {url.split('@')[1] if '@' in url else '...'}")

    # Remove driver specific prefix if present for psycopg2
    if "postgresql+asyncpg://" in url:
        url = url.replace("postgresql+asyncpg://", "postgresql://")
    
    try:
        conn = psycopg2.connect(url)
        conn.autocommit = True
        cur = conn.cursor()
        
        tables = ['destinations', 'hotels', 'restaurants', 'tours']
        column = 'image_url'
        dtype = 'VARCHAR(500)'
        
        for table in tables:
            print(f"Checking table '{table}'...")
            try:
                # Check if column exists
                cur.execute(f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='{table}' AND column_name='{column}';
                """)
                if not cur.fetchone():
                    print(f"  Column '{column}' missing. Adding...")
                    cur.execute(f"ALTER TABLE {table} ADD COLUMN {column} {dtype};")
                    print(f"  Successfully added '{column}' to '{table}'.")
                else:
                    print(f"  Column '{column}' already exists.")
            except Exception as e:
                print(f"  Error processing table '{table}': {e}")
                
        cur.close()
        conn.close()
        print("Migration completed successfully.")
        
    except Exception as e:
        print(f"Migration failed: {e}")
        print("Ensure the database is running and configuration is correct.")

if __name__ == "__main__":
    migrate()
