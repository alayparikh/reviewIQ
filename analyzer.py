from textblob import TextBlob
from collections import Counter
import re

def analyze_reviews(reviews):
    """
    Analyzes a list of reviews for sentiment and common topics.
    """
    if not reviews:
        return {
            "average_sentiment": 0,
            "sentiment_label": "Neutral",
            "top_topics": [],
            "rating_breakdown": {}
        }
        
    total_sentiment = 0
    ratings = []
    
    for review in reviews:
        blob = TextBlob(review['text'])
        sentiment = blob.sentiment.polarity
        review['sentiment_score'] = sentiment
        total_sentiment += sentiment
        ratings.append(review['rating'])
        
        # Topic extraction via regex (avoids NLTK corpora, unavailable in serverless envs)
        review['topics'] = extract_topics(review['text'], limit=3)

    avg_sentiment = total_sentiment / len(reviews)
    
    # Topic extraction (general)
    all_text = " ".join([r['text'] for r in reviews])
    top_topics = extract_topics(all_text)
    
    rating_breakdown = Counter(ratings)
    
    sentiment_label = "Positive" if avg_sentiment > 0.1 else "Negative" if avg_sentiment < -0.1 else "Neutral"
    
    place_ratings = [r['place_rating'] for r in reviews if r.get('place_rating') is not None]
    place_rating = place_ratings[0] if place_ratings else None
    avg_review_rating = sum(ratings) / len(ratings) if ratings else 0
    
    return {
        "average_sentiment": avg_sentiment,
        "sentiment_label": sentiment_label,
        "top_topics": top_topics,
        "rating_breakdown": dict(rating_breakdown),
        "place_rating": place_rating,
        "review_rating": avg_review_rating
    }

def extract_topics(text, limit=5):
    words = re.findall(r'\w+', text.lower())
    stop_words = {'the', 'and', 'a', 'to', 'of', 'in', 'is', 'i', 'was', 'it', 'for', 'at', 'with', 'on', 'this', 'but', 'here', 'staff', 'service', 'very', 'had', 'place', 'were', 'they', 'you', 'my'}
    filtered_words = [w for w in words if w not in stop_words and len(w) > 3]
    return [topic for topic, count in Counter(filtered_words).most_common(limit)]

def generate_insights(own_reviews, competitor_analyses):
    """
    Generates actionable insights from analyzed reviews.
    """
    positive_reviews = [r for r in own_reviews if r['sentiment_score'] > 0.2]
    negative_reviews = [r for r in own_reviews if r['sentiment_score'] < 0]
    
    # What to Shout About (formerly What People Love)
    pos_text = " ".join([r['text'] for r in positive_reviews])
    what_to_shout_about = extract_topics(pos_text, limit=3)
    
    # What to Fix
    neg_text = " ".join([r['text'] for r in negative_reviews])
    what_to_fix_topics = extract_topics(neg_text, limit=3)
    
    # Suggested actions based on negative topics
    action_map = {
        "wait": "Improve staffing during peak hours to reduce wait times.",
        "price": "Review pricing strategy or highlight premium value in marketing.",
        "clean": "Schedule more frequent cleaning rotations.",
        "staff": "Conduct customer service training for front-line employees.",
        "quality": "Investigate quality control in the production process.",
        "food": "Audit menu items for consistency and taste.",
        "service": "Look into specific bottlenecks in the service workflow."
    }
    
    what_to_fix = []
    for topic in what_to_fix_topics:
        action = action_map.get(topic, "Monitor customer feedback closely on this topic.")
        what_to_fix.append({"topic": topic, "action": action})
        
    # How You Stack Up
    own_sentiment = sum(r['sentiment_score'] for r in own_reviews) / len(own_reviews) if own_reviews else 0
    own_review_rating = sum(r['rating'] for r in own_reviews) / len(own_reviews) if own_reviews else 0
    own_place_rating = own_reviews[0].get('place_rating') if own_reviews and own_reviews[0].get('place_rating') is not None else None
    own_rating = own_place_rating if own_place_rating is not None else own_review_rating

    comparison = []
    for name, analysis in competitor_analyses.items():
        diff = own_sentiment - analysis['average_sentiment']
        comp_review_rating = sum(r * count for r, count in analysis['rating_breakdown'].items()) / sum(analysis['rating_breakdown'].values()) if analysis['rating_breakdown'] else 0
        comp_place_rating = analysis.get('place_rating')
        comp_rating = comp_place_rating if comp_place_rating is not None else comp_review_rating
        
        comparison.append({
            "name": name,
            "sentiment_score": analysis['average_sentiment'],
            "rating": comp_rating,
            "place_rating": comp_place_rating,
            "review_rating": comp_review_rating,
            "status": "Ahead" if diff > 0.05 else "Behind" if diff < -0.05 else "On par"
        })
    
    # Add own to comparison for convenience in template
    own_stats = {
        "name": "You",
        "sentiment_score": own_sentiment,
        "rating": own_rating,
        "place_rating": own_place_rating,
        "review_rating": own_review_rating,
        "status": "YOU"
    }
        
    # Trending
    trending = {"status": "Stable", "message": "Sentiment has been consistent across recent reviews."}
    if len(own_reviews) >= 3:
        # Sort reviews by timestamp if available, else assume they are already sorted recent-first
        sorted_reviews = sorted(own_reviews, key=lambda x: x.get('timestamp') or 0, reverse=True)
        
        # Split into two halves
        mid = len(sorted_reviews) // 2
        recent_half = sorted_reviews[:mid]
        older_half = sorted_reviews[mid:]
        
        recent_avg = sum(r['sentiment_score'] for r in recent_half) / len(recent_half)
        older_avg = sum(r['sentiment_score'] for r in older_half) / len(older_half)
        
        diff = recent_avg - older_avg
        if diff > 0.05:
            trending = {"status": "Improving", "message": f"Sentiment has trended upward by {diff*100:.0f}% in the most recent reviews."}
        elif diff < -0.05:
            trending = {"status": "Declining", "message": f"Sentiment has trended downward by {abs(diff)*100:.0f}% recently. Investigation recommended."}

    # Add suggested replies for every own review, sorted most-recent first so the
    # business can see what to respond to next
    recent_own_reviews = sorted(own_reviews, key=lambda r: r.get('timestamp') or 0, reverse=True)
    for review in recent_own_reviews:
        review['suggested_reply'] = generate_suggested_reply(review)
    reply_recommendations = [
        {
            "text": r['text'],
            "rating": r['rating'],
            "sentiment_score": r['sentiment_score'],
            "suggested_reply": r['suggested_reply'],
            "priority": "High" if r['sentiment_score'] < 0 else "Low"
        }
        for r in recent_own_reviews[:5]
    ]

    business_suggestions = generate_business_suggestions(
        own_stats, what_to_fix, what_to_shout_about, trending, comparison
    )

    return {
        "what_to_shout_about": what_to_shout_about,
        "what_to_fix": what_to_fix,
        "comparison": comparison,
        "own_stats": own_stats,
        "trending": trending,
        "reply_recommendations": reply_recommendations,
        "business_suggestions": business_suggestions
    }

def generate_suggested_reply(review):
    """
    Generates a professional response template tailored to a review's sentiment.
    """
    text = review['text'].lower()
    sentiment = review.get('sentiment_score', 0)

    if sentiment >= 0.2:
        if "staff" in text or "service" in text:
            return "Thank you so much for the kind words about our team! We'll be sure to pass along your compliments. We hope to see you again soon!"
        return "Thank you for the wonderful review! We're thrilled you had a great experience, and we look forward to welcoming you back soon."

    if sentiment > -0.05:
        return "Thanks for taking the time to share your feedback. We're always looking to improve, so if there's anything specific we could do better, we'd love to hear it."

    if "wait" in text or "long" in text:
        return "Hi, thank you for your feedback. We're sorry about the long wait during your visit. We're working on improving our staffing to ensure a faster experience. We hope to see you again soon!"
    elif "price" in text or "expensive" in text:
        return "Thank you for sharing your thoughts. We strive to provide premium quality and service, but we understand your concern about pricing. We regularly review our menu to ensure we offer great value."
    elif "clean" in text or "dirty" in text:
        return "We're very sorry to hear about the cleanliness issue. We maintain high standards and will address this with our team immediately. Thank you for bringing it to our attention."
    elif "rude" in text or "staff" in text:
        return "We apologize for the experience you had with our team. Providing excellent service is our top priority, and we'll use your feedback for further training. We'd love the chance to make it right."
    else:
        return "Thank you for your feedback. We're sorry we didn't meet your expectations. We'd like to learn more about your experience to improve our service. Please feel free to reach out to us directly."

def generate_business_suggestions(own_stats, what_to_fix, what_to_shout_about, trending, comparison):
    """
    Curates prioritized, actionable suggestions for improving the business and
    earning more positive reviews, synthesized from the rest of the analysis.
    """
    suggestions = []

    for item in what_to_fix:
        suggestions.append({
            "priority": "High",
            "title": f"Address recurring '{item['topic']}' complaints",
            "suggestion": item['action']
        })

    if trending.get('status') == 'Declining':
        suggestions.append({
            "priority": "High",
            "title": "Reverse declining sentiment",
            "suggestion": trending['message'] + " Consider following up directly with recent unhappy customers."
        })

    behind_competitors = [c for c in comparison if c.get('status') == 'Behind']
    if behind_competitors:
        names = ", ".join(c['name'] for c in behind_competitors)
        suggestions.append({
            "priority": "Medium",
            "title": f"Close the gap with {names}",
            "suggestion": "You're trailing on sentiment versus this competitor. Review their top-rated reviews for ideas on what customers value most."
        })

    if what_to_shout_about:
        topics = ", ".join(what_to_shout_about)
        suggestions.append({
            "priority": "Medium",
            "title": "Promote what customers already love",
            "suggestion": f"Customers consistently praise {topics}. Highlight these in your marketing, social posts, and review-request follow-ups to attract more positive reviews."
        })

    if own_stats.get('sentiment_score', 0) > 0.1 and not behind_competitors:
        suggestions.append({
            "priority": "Low",
            "title": "Turn happy customers into reviewers",
            "suggestion": "Sentiment is strong. Ask satisfied customers for a review right after a positive interaction (e.g. a QR code at checkout) to build review volume while sentiment is high."
        })

    if not suggestions:
        suggestions.append({
            "priority": "Low",
            "title": "Keep monitoring",
            "suggestion": "No major issues detected. Keep collecting reviews to track trends over time."
        })

    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    suggestions.sort(key=lambda s: priority_order.get(s['priority'], 3))
    return suggestions
