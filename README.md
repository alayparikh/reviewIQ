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

4. Open the app at `http://localhost:3000`, then paste your API key into the "Google Places API Key" field on the form.

## Notes

- The `.env` file is ignored by Git so your API key stays private.
- The app currently accepts the API key from the form on the web page.
- If you want to store the key in `.env` and use it automatically, you can extend the app to load it with a package like `python-dotenv`.
