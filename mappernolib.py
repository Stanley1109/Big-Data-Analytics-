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
