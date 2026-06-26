import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify
from fetcher import fetch_reviews
from analyzer import analyze_reviews, generate_insights

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


@app.route('/api/analyze', methods=['POST', 'OPTIONS'])
def api_analyze():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    data = request.get_json(silent=True) or request.form
    business_name = data.get('business_name') or ''
    competitor_business = data.get('competitor_business', '') or ''
    if isinstance(competitor_business, str):
        competitors = [c.strip() for c in competitor_business.split(',') if c.strip()]
    else:
        competitors = [c.strip() for c in competitor_business if c and isinstance(c, str)]

    api_key = os.getenv('GOOGLE_PLACES_API_KEY')

    if not business_name:
        return jsonify({"error": "Business name is required"}), 400

    own_reviews = fetch_reviews(business_name, source='self', api_key=api_key)
    own_analysis = analyze_reviews(own_reviews)

    all_reviews = []
    competitor_analyses = {}
    competitor_reviews_dict = {}

    for comp in competitors:
        comp_reviews = fetch_reviews(comp, source='competitor', api_key=api_key)
        comp_analysis = analyze_reviews(comp_reviews)
        competitor_analyses[comp] = comp_analysis
        competitor_reviews_dict[comp] = comp_reviews

    insights = generate_insights(own_reviews, competitor_analyses)

    all_reviews.extend(own_reviews)
    for comp_reviews in competitor_reviews_dict.values():
        all_reviews.extend(comp_reviews)

    summary = {
        "business_name": business_name,
        "own_analysis": own_analysis,
        "competitor_analyses": competitor_analyses,
        "insights": insights
    }

    return jsonify({
        "business_name": business_name,
        "summary": summary,
        "reviews": all_reviews
    })
