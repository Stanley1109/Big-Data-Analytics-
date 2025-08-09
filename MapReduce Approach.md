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




