import pyodbc
print("Drivers instalados:")
for driver in pyodbc.drivers():
    print(f"- {driver}")
