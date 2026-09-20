from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, sum, avg, hour, date_format, desc

# Start Spark
spark = SparkSession.builder \
    .appName("Food Delivery Demand Analytics") \
    .master("local[*]") \
    .getOrCreate()

print("\n===================================")
print(" FOOD DELIVERY DEMAND ANALYTICS")
print("===================================\n")

# Load dataset
df = spark.read.csv(
    "data/food_orders.csv",
    header=True,
    inferSchema=True
)

# Show total records
print("TOTAL ORDERS:", df.count())

print("\nDATASET:")
df.show(5)

print("\nSCHEMA:")
df.printSchema()

# Remove duplicates and missing values
df = df.dropDuplicates()

df = df.dropna(
    subset=["order_time", "location", "cuisine"]
)

# Create hour column
df = df.withColumn(
    "order_hour",
    hour(col("order_time"))
)

# Create day column
df = df.withColumn(
    "day_of_week",
    date_format(col("order_time"), "EEEE")
)

# ===================================
# 1. POPULAR CUISINES
# ===================================

popular_cuisines = df.groupBy(
    "cuisine"
).agg(
    count("*").alias("total_orders")
).orderBy(
    desc("total_orders")
)

print("\n===================================")
print("1. POPULAR CUISINES")
print("===================================")

popular_cuisines.show()

# ===================================
# 2. PEAK ORDERING HOURS
# ===================================

peak_hours = df.groupBy(
    "order_hour"
).agg(
    count("*").alias("total_orders")
).orderBy(
    desc("total_orders")
)

print("\n===================================")
print("2. PEAK ORDERING HOURS")
print("===================================")

peak_hours.show(24)

# ===================================
# 3. LOCATION-WISE DEMAND
# ===================================

location_demand = df.groupBy(
    "location"
).agg(
    count("*").alias("total_orders")
).orderBy(
    desc("total_orders")
)

print("\n===================================")
print("3. LOCATION-WISE DEMAND")
print("===================================")

location_demand.show()

# ===================================
# 4. DAY-WISE DEMAND
# ===================================

day_demand = df.groupBy(
    "day_of_week"
).agg(
    count("*").alias("total_orders")
).orderBy(
    desc("total_orders")
)

print("\n===================================")
print("4. DAY-WISE DEMAND")
print("===================================")

day_demand.show()

# ===================================
# 5. REVENUE BY CUISINE
# ===================================

revenue_by_cuisine = df.groupBy(
    "cuisine"
).agg(
    count("*").alias("total_orders"),
    sum("order_value").alias("total_revenue"),
    avg("order_value").alias("average_order_value")
).orderBy(
    desc("total_revenue")
)

print("\n===================================")
print("5. REVENUE BY CUISINE")
print("===================================")

revenue_by_cuisine.show()

# ===================================
# 6. CUISINE BY LOCATION
# ===================================

location_cuisine = df.groupBy(
    "location",
    "cuisine"
).agg(
    count("*").alias("total_orders")
).orderBy(
    desc("total_orders")
)

print("\n===================================")
print("6. CUISINE BY LOCATION")
print("===================================")

location_cuisine.show(30)

# ============================================
# EXPORT RESULTS
# ============================================

import os

os.makedirs("output", exist_ok=True)

popular_cuisines.toPandas().to_csv(
    "output/popular_cuisines.csv", index=False
)

peak_hours.toPandas().to_csv(
    "output/peak_hours.csv", index=False
)

location_demand.toPandas().to_csv(
    "output/location_demand.csv", index=False
)

day_demand.toPandas().to_csv(
    "output/day_demand.csv", index=False
)

revenue_by_cuisine.toPandas().to_csv(
    "output/revenue_by_cuisine.csv", index=False
)

location_cuisine.toPandas().to_csv(
    "output/location_cuisine.csv", index=False
)

print("\n===================================")
print(" RESULTS EXPORTED SUCCESSFULLY")
print("===================================")

print("Files saved in the output folder:")
print("- popular_cuisines.csv")
print("- peak_hours.csv")
print("- location_demand.csv")
print("- day_demand.csv")
print("- revenue_by_cuisine.csv")
print("- location_cuisine.csv")

spark.stop()