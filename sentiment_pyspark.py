from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, split, size, udf
from pyspark.sql.functions import avg, count, sum as _sum
from pyspark.sql.types import IntegerType, StringType, FloatType


# ✅ Create Spark session
spark = SparkSession.builder.appName("BookReviewSentiment").getOrCreate()

# ✅ Load CSV
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
