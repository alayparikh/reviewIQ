# reviewIQ

Simple review analysis app that compares your Google Places reviews with competitors and generates sentiment insights.

## Setup

1. Install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Add your Google Places API key to a local file named `.env`:

```text
GOOGLE_PLACES_API_KEY=your_google_places_api_key_here
```

3. Start the app:

```bash
python app.py
```

4. Open the app at `http://localhost:3000`.

## Vercel Frontend

A static frontend is available under `frontend/` for hosting on Vercel.

- `frontend/index.html` is the homepage.
- `frontend/app.js` sends the request to the backend API at `/api/analyze`.
- If you host the frontend separately, set `API_BASE_URL` in `frontend/app.js` to your backend URL.

## Notes

- The `.env` file is ignored by Git so your API key stays private.
- The backend loads `GOOGLE_PLACES_API_KEY` automatically from `.env` using `python-dotenv`.
- The static frontend can be hosted on Vercel and will call the backend API for results.
