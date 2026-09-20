import csv
import random
from datetime import datetime, timedelta

cuisines = [
    "Indian",
    "Chinese",
    "Italian",
    "Fast Food",
    "South Indian",
    "North Indian",
    "Biryani",
    "Desserts"
]

locations = [
    "Delhi",
    "Mumbai",
    "Bangalore",
    "Kolkata",
    "Hyderabad",
    "Pune"
]

start_date = datetime(2026, 1, 1)

with open("data/food_orders.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)

    writer.writerow([
        "order_id",
        "order_time",
        "location",
        "cuisine",
        "total_items",
        "order_value"
    ])

    for i in range(1, 50001):

        random_days = random.randint(0, 200)

        hour = random.choices(
            range(24),
            weights=[
                1, 1, 1, 1, 1, 1,
                2, 3, 4, 4, 5, 6,
                8, 7, 5, 4, 5, 7,
                10, 12, 13, 11, 7, 4
            ]
        )[0]

        minute = random.randint(0, 59)

        order_time = (
            start_date + timedelta(days=random_days)
        ).replace(
            hour=hour,
            minute=minute
        )

        location = random.choice(locations)

        cuisine = random.choices(
            cuisines,
            weights=[18, 14, 8, 15, 10, 12, 17, 6]
        )[0]

        total_items = random.randint(1, 6)
        order_value = random.randint(150, 1500)

        writer.writerow([
            i,
            order_time.strftime("%Y-%m-%d %H:%M:%S"),
            location,
            cuisine,
            total_items,
            order_value
        ])

print("Dataset created successfully!")
print("Total records: 50000")