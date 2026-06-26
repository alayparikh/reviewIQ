import uuid
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import init_db, save_report, get_report
from fetcher import fetch_reviews
from analyzer import analyze_reviews, generate_insights
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Ensure DB is initialized
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    business_name = request.form.get('business_name')
    competitors = request.form.get('competitors', '').split(',')
    competitors = [c.strip() for c in competitors if c.strip()]
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    
    if not business_name:
        return "Business name is required", 400
        
    report_id = str(uuid.uuid4())
    
    # Fetch and analyze for main business
    own_reviews = fetch_reviews(business_name, source='self', api_key=api_key)
    own_analysis = analyze_reviews(own_reviews)
    
    all_reviews = []
    competitor_analyses = {}
    competitor_reviews_dict = {}
    
    # Fetch and analyze for competitors
    for comp in competitors:
        comp_reviews = fetch_reviews(comp, source='competitor', api_key=api_key)
        comp_analysis = analyze_reviews(comp_reviews)
        competitor_analyses[comp] = comp_analysis
        competitor_reviews_dict[comp] = comp_reviews
        
    insights = generate_insights(own_reviews, competitor_analyses)
    
    # After generating insights, own_reviews are updated with suggested replies
    all_reviews.extend(own_reviews)
    for comp_reviews in competitor_reviews_dict.values():
        all_reviews.extend(comp_reviews)
    
    summary = {
        "business_name": business_name,
        "own_analysis": own_analysis,
        "competitor_analyses": competitor_analyses,
        "insights": insights
    }
    
    save_report(report_id, business_name, summary, all_reviews)
    
    return redirect(url_for('view_report', report_id=report_id))

@app.route('/report/<report_id>')
def view_report(report_id):
    report_data = get_report(report_id)
    if not report_data:
        return "Report not found", 404
    return render_template('report.html', report=report_data)

@app.route('/api/report/<report_id>')
def api_report(report_id):
    report_data = get_report(report_id)
    if not report_data:
        return jsonify({"error": "Report not found"}), 404
    return jsonify(report_data)

if __name__ == '__main__':
    # Listen on all interfaces, port 3000
    app.run(host='0.0.0.0', port=3000, debug=True)
