
# Recipe Hub Backend (Flask)

This is a realistic Flask REST API for a recipe application. You can deploy it on AWS EC2 behind a Load Balancer and with an Auto Scaling Group.

## Main Features

- User registration and login (JWT auth)
- CRUD for recipes
- Rating system (1–5 stars)
- Basic search and filtering
- Health check endpoint for load balancers

## Endpoints (Summary)

- `GET /health`
- `POST /auth/register`
- `POST /auth/login`
- `GET /recipes`
- `GET /recipes/<id>`
- `POST /recipes` (auth required)
- `PUT /recipes/<id>` (auth required, owner only)
- `DELETE /recipes/<id>` (auth required, owner only)
- `POST /recipes/<id>/rate` (auth required)

## Local Run

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export SECRET_KEY="change-me"  # Windows: set SECRET_KEY=change-me
python app.py
```

Then visit: `http://localhost:5000/health`
