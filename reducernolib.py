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
