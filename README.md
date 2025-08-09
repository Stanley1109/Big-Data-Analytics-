# 📙 Amazon Book Reviews: Sentiment Analysis using Hadoop MapReduce and Apache Spark

This project focuses on efficiently processing and analysing a large dataset of Amazon book reviews to extract key sentiment insights. Using predefined positive and negative word sets tailored for book reviews, each review is classified as positive, neutral, or negative, enabling the calculation of total reviews, average sentiment scores, and counts for each sentiment category. Leveraging distributed computing, we implement the analysis using both Hadoop MapReduce and Apache Spark (PySpark) to handle the dataset’s massive scale, ensuring faster processing compared to traditional methods. The project also compares the two frameworks in terms of implementation complexity, execution efficiency, and output accuracy, providing guidance on the most effective approach for large-scale sentiment analysis in the e-commerce domain.

---

## 📁 Files in this Repo

- `README.md`: Project overview
- `mappernolib.py`: Script to clean and split the raw Kaggle dataset into chunks
- `reducernolib.py`: Script to merge cleaned chunks into a single CSV file
- `MapReduce Approach.md`: Full execution guide and explanation of the Hadoop MapReduce implementation
- `Non-MapReduce Approach.md`: Full execution guide and explanation of the Apache Spark (non-MapReduce) implementation

---

## 📦 Dataset

This project uses flight performance data sourced from Kaggle:

🔗 [Amazon Book Reviews(Kaggle)](https://www.kaggle.com/datasets/mohamedbakhet/amazon-books-reviews/data?select=Books_rating.csv)

- **File Name**: `Books_rating.csv`
- **File Size**: ~2.80 GB
- **Total Records**: ~3.0 million rows

---

## 👥 Group Members

| Name                    | Student ID  |
|-------------------------|-------------|
| Stanley Chung Shen Wei  | 22057251    |
| Lam Zi Xin              | 22049126    |
| Terrance Loong Jun Yen  | 21026976    |

