const API_BASE_URL = ''; // Set this to your backend URL if the API is hosted elsewhere, e.g. 'https://my-backend.example.com'

const analyzeForm = document.getElementById('analyzeForm');
const formMessage = document.getElementById('formMessage');
const resultsSection = document.getElementById('results');
const sentimentScoreEl = document.getElementById('sentimentScore');
const sentimentLabelEl = document.getElementById('sentimentLabel');
const placeRatingEl = document.getElementById('placeRating');
const reviewRatingEl = document.getElementById('reviewRating');
const fixTopicsEl = document.getElementById('fixTopics');
const ownStatsEl = document.getElementById('ownStats');
const competitorStatsEl = document.getElementById('competitorStats');
const reviewListEl = document.getElementById('reviewList');
const replyRecommendationsEl = document.getElementById('replyRecommendations');
const businessSuggestionsEl = document.getElementById('businessSuggestions');

analyzeForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  formMessage.classList.add('d-none');
  resultsSection.classList.add('d-none');

  const businessName = document.getElementById('businessName').value.trim();
  const competitorBusiness = document.getElementById('competitorBusiness').value.trim();

  if (!businessName) {
    showError('Your business name is required.');
    return;
  }

  const payload = {
    business_name: businessName,
    competitor_business: competitorBusiness
  };

  try {
    const response = await fetch(`${API_BASE_URL}/api/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    if (!response.ok) {
      showError(data.error || 'Unable to analyze your business.');
      return;
    }

    renderResults(data);
  } catch (error) {
    showError('Unable to reach the backend API. Please check your backend URL and try again.');
    console.error(error);
  }
});

function showError(message) {
  formMessage.innerText = message;
  formMessage.classList.remove('d-none');
}

function renderResults(data) {
  const summary = data.summary;
  const ownStats = summary.insights.own_stats;
  const competitorData = summary.insights.comparison || [];

  sentimentScoreEl.innerText = summary.own_analysis.average_sentiment.toFixed(2);
  sentimentLabelEl.innerText = summary.own_analysis.sentiment_label;
  sentimentLabelEl.className = `badge ${summary.own_analysis.average_sentiment > 0.1 ? 'bg-success' : summary.own_analysis.average_sentiment < -0.1 ? 'bg-danger' : 'bg-warning text-dark'}`;

  if (ownStats.place_rating !== null && ownStats.place_rating !== undefined) {
    placeRatingEl.innerText = `${ownStats.place_rating.toFixed(1)}/5`;
    reviewRatingEl.innerText = ownStats.review_rating.toFixed(1) !== ownStats.place_rating.toFixed(1)
      ? `Sample average: ${ownStats.review_rating.toFixed(1)}/5`
      : 'Google overall rating';
  } else {
    placeRatingEl.innerText = `${ownStats.review_rating.toFixed(1)}/5`;
    reviewRatingEl.innerText = 'Review sample average';
  }

  const fixes = summary.insights.what_to_fix || [];
  fixTopicsEl.innerHTML = fixes.length
    ? fixes.map(item => `<div class="badge bg-danger text-white rounded-pill me-1 mb-1">${item.topic}</div>`).join('')
    : '<span class="text-muted">No major issues found.</span>';

  ownStatsEl.innerHTML = `
    <div><strong>Sentiment</strong>: ${ownStats.sentiment_score.toFixed(2)}</div>
    <div><strong>Rating</strong>: ${ownStats.rating.toFixed(1)}/5</div>
    <div class="text-muted">${ownStats.place_rating ? 'Google overall rating' : 'Sample review average'}</div>
  `;

  competitorStatsEl.innerHTML = competitorData.length
    ? competitorData.map(comp => `
        <div class="mb-3">
          <div><strong>${comp.name}</strong></div>
          <div>Sentiment: ${comp.sentiment_score.toFixed(2)}</div>
          <div>Rating: ${comp.rating.toFixed(1)}/5</div>
          ${comp.place_rating !== null && comp.place_rating !== undefined ? `<div class="text-muted">Google: ${comp.place_rating.toFixed(1)}/5</div>` : ''}
          ${comp.review_rating !== null && comp.review_rating !== undefined ? `<div class="text-muted">Sample: ${comp.review_rating.toFixed(1)}/5</div>` : ''}
        </div>
      `).join('')
    : '<div class="text-muted">No competitor provided.</div>';

  const replyRecs = summary.insights.reply_recommendations || [];
  replyRecommendationsEl.innerHTML = replyRecs.length
    ? replyRecs.map(r => `
        <div class="mb-3 p-3 bg-light rounded border-start border-4 ${r.priority === 'High' ? 'border-danger' : 'border-secondary'}">
          <div class="d-flex justify-content-between mb-1">
            <span class="badge ${r.priority === 'High' ? 'bg-danger' : 'bg-secondary'}">${r.priority} priority</span>
            <span class="text-warning small">${'★'.repeat(r.rating)}${'☆'.repeat(5 - r.rating)}</span>
          </div>
          <p class="small mb-2">"${escapeHtml(r.text)}"</p>
          <p class="small text-muted mb-1">"${escapeHtml(r.suggested_reply)}"</p>
          <button type="button" class="btn btn-sm btn-link p-0 text-decoration-none copy-reply-btn" data-text="${escapeHtml(r.suggested_reply)}">Copy to clipboard</button>
        </div>
      `).join('')
    : '<p class="text-muted small">No recent reviews to respond to.</p>';

  document.querySelectorAll('.copy-reply-btn').forEach(button => {
    button.addEventListener('click', () => {
      navigator.clipboard.writeText(button.getAttribute('data-text')).then(() => {
        const original = button.innerText;
        button.innerText = 'Copied!';
        setTimeout(() => { button.innerText = original; }, 2000);
      });
    });
  });

  const suggestions = summary.insights.business_suggestions || [];
  const priorityBadge = { High: 'bg-danger', Medium: 'bg-warning text-dark', Low: 'bg-success' };
  businessSuggestionsEl.innerHTML = suggestions.length
    ? suggestions.map(s => `
        <div class="mb-3">
          <div class="d-flex align-items-center mb-1">
            <span class="badge ${priorityBadge[s.priority] || 'bg-secondary'} me-2">${s.priority}</span>
            <span class="fw-bold small">${escapeHtml(s.title)}</span>
          </div>
          <p class="small text-muted mb-0">${escapeHtml(s.suggestion)}</p>
        </div>
      `).join('')
    : '<p class="text-muted small">No suggestions yet.</p>';

  reviewListEl.innerHTML = data.reviews.map(review => `
    <div class="col-md-6">
      <div class="p-3 review-card rounded bg-white">
        <div class="d-flex justify-content-between align-items-start mb-2">
          <div><strong>${review.business_name}</strong></div>
          <div class="review-badge badge bg-secondary">${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}</div>
        </div>
        <p class="mb-2">${escapeHtml(review.text)}</p>
        <div class="small text-muted">Source: ${review.source}</div>
      </div>
    </div>
  `).join('');

  resultsSection.classList.remove('d-none');
}

function escapeHtml(text) {
  if (!text) return '';
  return text.replace(/[&<>"]+/g, (match) => {
    const escapeMap = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;'
    };
    return escapeMap[match] || match;
  });
}
