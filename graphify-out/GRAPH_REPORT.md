# Graph Report - .  (2026-06-26)

## Corpus Check
- Corpus is ~3,850 words - fits in a single context window. You may not need a graph.

## Summary
- 92 nodes · 119 edges · 10 communities (9 shown, 1 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 16 edges (avg confidence: 0.86)
- Token cost: 38,285 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Review Analysis Engine|Review Analysis Engine]]
- [[_COMMUNITY_Frontend App Logic|Frontend App Logic]]
- [[_COMMUNITY_Static Frontend Page|Static Frontend Page]]
- [[_COMMUNITY_Setup & Deployment Docs|Setup & Deployment Docs]]
- [[_COMMUNITY_Review Sense Form UI|Review Sense Form UI]]
- [[_COMMUNITY_Report Insights UI|Report Insights UI]]
- [[_COMMUNITY_Review Fetching Layer|Review Fetching Layer]]
- [[_COMMUNITY_Vercel Config|Vercel Config]]
- [[_COMMUNITY_Scraping Dependencies|Scraping Dependencies]]

## God Nodes (most connected - your core abstractions)
1. `fetch_reviews()` - 8 edges
2. `generate_insights()` - 7 edges
3. `report Template Object` - 7 edges
4. `analyze_reviews()` - 6 edges
5. `analyze()` - 5 edges
6. `api_analyze()` - 5 edges
7. `save_report()` - 5 edges
8. `get_report()` - 5 edges
9. `app.py` - 5 edges
10. `/analyze POST Form` - 5 edges

## Surprising Connections (you probably didn't know these)
- `/analyze POST Form` --semantically_similar_to--> `businessName Input`  [INFERRED] [semantically similar]
  templates/index.html → frontend/index.html
- `competitorBusiness Input` --semantically_similar_to--> `competitors Input`  [INFERRED] [semantically similar]
  frontend/index.html → templates/index.html
- `What to Fix Insight` --semantically_similar_to--> `Results Section (sentiment/rating/fix topics)`  [INFERRED] [semantically similar]
  templates/report.html → frontend/index.html
- `api_key Input (optional)` --references--> `GOOGLE_PLACES_API_KEY`  [INFERRED]
  templates/index.html → README.md
- `app.py` --calls--> `flask`  [INFERRED]
  README.md → requirements.txt

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Two Parallel Frontends Pattern (Vercel static vs Flask templates)** — index_reviewiq_page, index_reviewsense_page, report_reviewsense_insights_page [INFERRED 0.85]
- **Review Analysis Insight Generation Flow** — index_analyze_form, report_object, report_what_to_fix, report_comparison_table [INFERRED 0.85]
- **Sentiment Analysis Dependency Chain** — requirements_textblob, requirements_vadersentiment, report_sentiment_score_card [INFERRED 0.75]

## Communities (10 total, 1 thin omitted)

### Community 0 - "Review Analysis Engine"
Cohesion: 0.20
Nodes (15): analyze_reviews(), extract_topics(), generate_insights(), generate_suggested_reply(), Generates a professional response template for a negative review., Analyzes a list of reviews for sentiment and common topics., Generates actionable insights from analyzed reviews., analyze() (+7 more)

### Community 1 - "Frontend App Logic"
Cohesion: 0.13
Nodes (11): analyzeForm, competitorStatsEl, fixTopicsEl, formMessage, ownStatsEl, placeRatingEl, resultsSection, reviewListEl (+3 more)

### Community 2 - "Static Frontend Page"
Cohesion: 0.18
Nodes (13): app.js script include, Bootstrap 5 CSS CDN, Results Section (sentiment/rating/fix topics), ReviewIQ Homepage (frontend/index.html), /api/analyze Endpoint, API_BASE_URL Variable, CORS Requirement, Deploying Instructions (+5 more)

### Community 3 - "Setup & Deployment Docs"
Cohesion: 0.18
Nodes (12): app.py, .env File, frontend/index.html (referenced), GOOGLE_PLACES_API_KEY, python-dotenv, reviewIQ Project, Setup Instructions, Vercel Frontend (+4 more)

### Community 4 - "Review Sense Form UI"
Cohesion: 0.25
Nodes (9): /analyze POST Form, analyzeForm, api_key Input (optional), static/js/app.js script include, businessName Input, competitorBusiness Input, competitors Input, ReviewSense Homepage (templates/index.html) (+1 more)

### Community 5 - "Report Insights UI"
Cohesion: 0.22
Nodes (9): Copy to Clipboard Button, report Template Object, Recent Reviews List, Overall Sentiment Score Card, Suggested Reply Feature, Trending Insight Card, What to Shout About Insight, textblob (+1 more)

### Community 6 - "Review Fetching Layer"
Cohesion: 0.43
Nodes (6): fetch_from_places_api(), fetch_from_scraper(), fetch_reviews(), get_mock_reviews(), A very simple scraper that extracts review snippets from Google search results., Fetches reviews for a business.     Tries Google Places API first, then falls ba

### Community 7 - "Vercel Config"
Cohesion: 0.50
Nodes (3): builds, routes, version

## Knowledge Gaps
- **27 isolated node(s):** `analyzeForm`, `formMessage`, `resultsSection`, `sentimentScoreEl`, `sentimentLabelEl` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `report Template Object` connect `Report Insights UI` to `Static Frontend Page`, `Setup & Deployment Docs`, `Review Sense Form UI`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **What connects `Analyzes a list of reviews for sentiment and common topics.`, `Generates actionable insights from analyzed reviews.`, `Generates a professional response template for a negative review.` to the rest of the system?**
  _32 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Frontend App Logic` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._