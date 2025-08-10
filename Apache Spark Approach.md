## 📜 Full Execution Guide (Apache Spark Approach)
As an alternative to the MapReduce pipeline, we implemented the same logic using Apache Spark’s DataFrame API in a PySpark script. This approach provided in-memory processing advantages, and leveraged the power of distributed computing for enhanced performance.
### 1️⃣ Prepare PySpark Script
```bash
nano sentiment_python.py
```
#### sentiment_python.py
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, split, size, udf
from pyspark.sql.functions import avg, count, sum as _sum
from pyspark.sql.types import IntegerType, StringType, FloatType


# ✅ Create Spark session
spark = SparkSession.builder.appName("BookReviewSentiment").getOrCreate()

# ✅ Load CSV from HDFS
df = spark.read.option("header", "true") \
               .option("multiLine", "true") \
               .option("quote", '"') \
               .option("escape", '"') \
               .option("delimiter", ",") \
               .option("mode", "PERMISSIVE") \
               .csv("hdfs:///user/hadoop/SMProject/Books_rating.csv")

# ✅ Keep relevant columns only
df = df.select(
    col("Id").alias("book_id"),
    col("review/text").alias("review_text")
).filter(col("review_text").isNotNull())

# ✅ Define expanded sentiment word sets (15 each)
positive_words = {
    "good", "great", "excellent", "amazing", "wonderful", "love", "awesome", "fantastic",
    "superb", "engaging", "inspiring", "informative", "entertaining", "brilliant", "touching"
}

negative_words = {
    "bad", "terrible", "awful", "worst", "hate", "boring", "poor", "disappointing",
    "slow", "confusing", "uninteresting", "predictable", "frustrating", "overrated", "annoying"
}

# ✅ Define UDF to calculate sentiment score (+1 for positive, -1 for negative)
def get_sentiment_score(text):
    words = text.lower().split()
    score = 0
    for word in words:
        if word in positive_words:
            score += 1
        elif word in negative_words:
            score -= 1
    return score

sentiment_score_udf = udf(get_sentiment_score, IntegerType())

# ✅ Apply UDF
df = df.withColumn("sentiment_score", sentiment_score_udf(col("review_text")))

# ✅ Classify as positive/neutral/negative
def classify_sentiment(score):
    if score > 0:
        return "positive"
    elif score < 0:
        return "negative"
    else:
        return "neutral"

sentiment_type_udf = udf(classify_sentiment, StringType())
df = df.withColumn("sentiment_type", sentiment_type_udf(col("sentiment_score")))

# ✅ Aggregate results per book_id

result_df = df.groupBy("book_id").agg(
    count("*").alias("total_reviews"),
    _sum("sentiment_score").alias("total_score"),
    _sum((col("sentiment_type") == "positive").cast("int")).alias("positive_count"),
    _sum((col("sentiment_type") == "neutral").cast("int")).alias("neutral_count"),
    _sum((col("sentiment_type") == "negative").cast("int")).alias("negative_count")
).withColumn(
    "avg_sentiment_score", (col("total_score") / col("total_reviews"))
).select(
    "book_id", "total_reviews", "avg_sentiment_score", "positive_count", "neutral_count", "negative_count"
).orderBy(col("book_id").asc())  # ✅ sort by book_id ascending


# ✅ Save to HDFS in requested order
result_df.rdd.map(lambda row: '\t'.join(map(str, [
    row['book_id'],
    row['total_reviews'],
    f"{row['avg_sentiment_score']:.2f}",
    row['positive_count'],
    row['neutral_count'],
    row['negative_count']
]))).saveAsTextFile("hdfs:///user/hadoop/SMPythonResultNew")

# ✅ Stop Spark session
spark.stop()
```
### 2️⃣ Execute PySpark Script in Local Mode
```bash
spark-submit sentiment_python.py
```
### 3️⃣ View Output in HDFS
Retrieve the output in HDFS after successfully execute the PySpark
```bash
hdfs dfs -cat /user/hadoop/SMPythonResultNew/part-* | head -n 20
```
### 4️⃣ Sample Output
```bash
0001047604      4       0.25      2      1      1   
0001047655      74      0.70      35     38     1
0001047736      12      0.50      4      8      0
0001047825      14      0.93      7      7      0
0001047876      8       0.50      3      5      0
0001048228      33      0.76      16     17     0
0001049143      11      0.27      2      9      0
0001050079      26      0.96      15     9      2
0001050087      28      1.21      17     10     1
0001050184      138     0.87      75     62     1
0001052888      13      0.69      5      8      0
0001052934      10      1.00      5      5      0
0001052950      49      0.86      25     23     1 
0001053744      1       2.00      1      0      0
0001054090      22      0.64      12     9      1
0001055003      338     0.99      189    138    11
0001384155      2       0.00      0      2      0
0001472879      1       0.00      0      1      0
0001474103      9       1.00      5      4      0
0001515195      2       0.00      1      0      1
```
