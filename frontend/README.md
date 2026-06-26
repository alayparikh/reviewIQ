# ReviewIQ Frontend

This frontend is designed for static hosting on Vercel.

## Deploying

1. Deploy the `frontend/` directory as a static site on Vercel.
2. If the backend is hosted separately, update `frontend/app.js`:

```js
const API_BASE_URL = 'https://your-backend.example.com';
```

3. The frontend sends POST requests to `API_BASE_URL/api/analyze`.
4. Your backend must expose the `POST /api/analyze` endpoint and allow CORS.

## Notes

- The homepage only needs two fields: `Your business` and `Competitor business`.
- Competitor business is optional. If left empty, the app returns insights for only your business.
