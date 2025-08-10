## Full Execution Guide (Hadoop MapReduce Approach)
This section outlines how we executed the MapReduce workflow on AWS using Hadoop Streaming.

### 1️⃣ Dataset Preparation
Upload the zip file for the dataset downloaded from the Kaggle link to the S3 Bucket.
Then on the master node run the code below (root-user admin):

```bash
sudo apt update
sudo apt install awscli
sudo su - hadoop
start-all.sh
```
Create a new directory ready to store the dataset:

```bash
mkdir SMProject
cd SMProject/
```
Copy the zip file from the S3 bucket into Hadoop Cluster:
```bash
aws s3 cp s3://sentimentanalysis3134/SentimentAnalysisDataset/ ./ --recursive
```

Unzip the Books_rating.zip file:
```bash
unzip Books_rating.zip
```

We then uploaded the file to HDFS:
```bash
hadoop fs -mkdir -p /user/hadoop/SMProject
hadoop fs -put SMProject /user/hadoop/SMProject/
```
### 2️⃣  Mapper and Reducer Scripts

Two Python scripts were written to perform the MapReduce job. The mapper (mappernolib.py) reads each book review from CSV input, tokenizes the review text, assigns a score by counting predefined positive and negative words, determines the sentiment (positive, negative, or neutral), and outputs the book ID with its score and sentiment. The reducer (reducernolib.py) aggregates these results for each book, calculating the total number of reviews, average score, and counts of positive, neutral, and negative reviews, then outputs these summary statistics per book.

#### mapper.py
```python
#!/usr/bin/env python3
import sys
import csv
import re

# Define basic positive and negative words
positive_words = {
    "good", "great", "excellent", "amazing", "wonderful", "love", "awesome", "fantastic",
    "superb", "engaging", "inspiring", "informative", "entertaining", "brilliant", "touching"
}

negative_words = {
    "bad", "terrible", "awful", "worst", "hate", "boring", "poor", "disappointing",
    "slow", "confusing", "uninteresting", "predictable", "frustrating", "overrated", "annoying"
}

# Read CSV from stdin
reader = csv.reader(sys.stdin)

for row in reader:
    if len(row) < 10:
        continue

    book_id = row[0].strip()
    review_text = row[9].strip().lower()

    # Tokenize: remove punctuation, split by whitespace
    words = re.findall(r'\b\w+\b', review_text)

    score = 0
    for word in words:
        if word in positive_words:
            score += 1
        elif word in negative_words:
            score -= 1

    # Determine sentiment label
    if score > 0:
        sentiment = "positive"
    elif score < 0:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    print(f"{book_id}\t{score},{sentiment}")
```
#### reducer.py
```python
#!/usr/bin/env python3
import sys

current_book = None
total_reviews = 0
total_score = 0
positive = 0
neutral = 0
negative = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    book_id, value = line.split("\t")
    score_str, sentiment = value.split(",")

    score = int(score_str)

    if current_book != book_id:
        if current_book is not None:
            avg_score = total_score / total_reviews if total_reviews else 0
            print(f"{current_book}\t{total_reviews}\t{avg_score:.2f}\t{positive}\t{neutral}\t{negative}")
        # Reset for new book
        current_book = book_id
        total_reviews = 0
        total_score = 0
        positive = 0
        neutral = 0
        negative = 0

    total_reviews += 1
    total_score += score
    if sentiment == "positive":
        positive += 1
    elif sentiment == "neutral":
        neutral += 1
    elif sentiment == "negative":
        negative += 1

# Output final book group
if current_book is not None:
    avg_score = total_score / total_reviews if total_reviews else 0
    print(f"{current_book}\t{total_reviews}\t{avg_score:.2f}\t{positive}\t{neutral}\t{negative}")
```

Both of the Python scripts are stored in the local directory (SMPython/Python)

Scripts were made executable using:
```bash
chmod +x mappernolib.py reducernolib.py
```
### 3️⃣ Hadoop Streaming Job Execution
The MapReduce job was executed using the Hadoop Streaming JAR:
```bash
hadoop jar /home/hadoop/hadoop-3.3.6/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar -input /user/hadoop/SMProject/Books_rating.csv -output sentimentpython -file SMPython/Python/mappernolib.py -file SMPython/Python/reducernolib.py -mapper SMPython/Python/mappernolib.py -reducer SMPython/Python/reducernolib.py
```

### 4️⃣ Output & Sorting
Final output from the Hadoop Streaming MapReduce job was retrieved in the HDFS
```bash
hadoop fs -cat /user/hadoop/sentimentpython/part-00000 | head -n 20
```
### 5️⃣ Sample Output
```bash
0001047604      4       0.25      3      0      1   
0001047655      74      0.65      38     28     8
0001047736      12      0.92      7      4      1
0001047825      14      1.07      9      5      0
0001047876      8       1.00      4      4      0
0001048228      33      0.61      13     19     1
0001049143      11      0.36      4      6      1
0001050079      26      0.81      14     8      4
0001050087      28      1.00      12     14     2
0001050184      138     0.83      82     48     8
0001052888      13      0.77      6      6      1
0001052934      10      0.60      5      5      0
0001052950      49      0.96      26     21     2 
0001053744      1       2.00      1      0      0
0001054090      22      0.68      14     7      1
0001055003      338     1.06      203    119    16
0001384155      2       1.00      1      1      0
0001472879      1       0.00      0      1      0
0001474103      9       1.11      5      4      0
0001515195      2       0.00      0      2      0
