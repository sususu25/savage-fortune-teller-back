# Savage Fortune Teller API

FastAPI backend for a savage, shareable astrology roast result.

## What It Does

- Calculates a birth chart from birth date, time, city, latitude, longitude, and timezone.
- Scores the chart into one of six astrology-based archetypes.
- Returns English roast-style result copy for viral sharing.
- Exposes reusable section titles and result text for frontend cards.

## Local Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Health check:

```bash
curl http://localhost:8000/api/v1/health
```

Reading example:

```bash
curl -X POST http://localhost:8000/api/v1/readings ^
  -H "Content-Type: application/json" ^
  -d "{\"birth_date\":\"1995-12-18\",\"birth_time\":\"14:30\",\"birth_city\":\"Seoul\",\"birth_country\":\"South Korea\",\"latitude\":37.5665,\"longitude\":126.978,\"timezone\":\"Asia/Seoul\"}"
```

## Environment

Create `.env` from `.env.example`.

```env
PROJECT_NAME="Savage Fortune Teller API"
API_V1_PREFIX="/api/v1"
BACKEND_CORS_ORIGINS="*"
GEONAMES_USERNAME="YOUR_GEONAMES_USERNAME"
```

`GEONAMES_USERNAME` is optional when the client sends `latitude`, `longitude`, and `timezone`.

## Docker

```bash
docker compose up --build -d
```

The API runs on:

```text
http://localhost:8000
```

## Oracle Free Tier Notes

On an Oracle VM, install Docker and Docker Compose, clone the repo, create `.env`, then run:

```bash
docker compose up --build -d
```

Open TCP port `8000` in both:

- Oracle Cloud security list / network security group
- VM firewall, if enabled

For production, put Nginx or Caddy in front of the app and set `BACKEND_CORS_ORIGINS` to the real frontend domain.
