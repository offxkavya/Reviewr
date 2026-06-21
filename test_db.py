import psycopg2
try:
    conn = psycopg2.connect(host="localhost", port=5432, user="postgres", password="password")
    print("Connected with password 'password'")
except Exception as e:
    print(f"Failed with 'password': {e}")

try:
    conn = psycopg2.connect(host="localhost", port=5432, user="postgres", password="secret")
    print("Connected with password 'secret'")
except Exception as e:
    print(f"Failed with 'secret': {e}")
    
try:
    conn = psycopg2.connect(host="localhost", port=5432, user="postgres", password="postgres")
    print("Connected with password 'postgres'")
except Exception as e:
    print(f"Failed with 'postgres': {e}")
