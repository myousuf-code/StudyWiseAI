# Deployment

## Architecture

- React frontend: Cloudflare Pages
- FastAPI API: Render Web Service
- Production database: hosted PostgreSQL, such as Neon or Supabase
- Hosted AI: NVIDIA API (the key stays on Render)

## Render API

Create a Render Web Service from this repository. `render.yaml` contains the
build, start, and health-check settings. Configure these environment variables
in Render:

```text
SECRET_KEY=<new-random-secret>
DATABASE_URL=<postgresql-connection-string>
CORS_EXTRA_ORIGINS=https://<your-pages-project>.pages.dev
FRONTEND_URL=https://<your-pages-project>.pages.dev
NVIDIA_API_KEY=<nvidia-key>
NVIDIA_MODEL=<model-id>
```

The service URL should respond at `/health` with a healthy status.

## Cloudflare Pages

Create a Pages project from the same repository with:

- Root directory: `frontend-react`
- Build command: `npm run build`
- Build output directory: `dist`
- Environment variable: `VITE_API_URL=https://<your-render-service>.onrender.com/api`

The frontend environment variable is embedded during the build, so redeploy
the Pages project after changing it.

## Before deploying

- Rotate any API keys that were ever committed to `.env`.
- Use a persistent PostgreSQL database instead of the default SQLite URL.
- Do not add `NVIDIA_API_KEY` or other secrets to frontend variables.