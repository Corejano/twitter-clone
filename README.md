# Twitter Clone

Full-stack Twitter clone application with Django REST Framework backend and Vue.js frontend.

## Tech Stack

### Backend
- Django 5.2.8
- Django REST Framework
- PostgreSQL
- Redis
- Django Channels (WebSockets)
- JWT Authentication

### Frontend
- Vue.js 3
- TypeScript

## Project Structure

```
clone-twitter/
├── backend/
│   ├── apps/
│   │   └── users/
│   ├── config/
│   ├── media/
│   ├── staticfiles/
│   ├── manage.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
├── docker-compose.yml
└── README.md
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for frontend development)

### Installation with Docker

1. Clone the repository
```bash
git clone <repository-url>
cd clone-twitter
```

2. Create environment file
```bash
cp backend/.env.example backend/.env
```

3. Start services
```bash
docker-compose up -d
```

4. Create superuser
```bash
docker-compose exec backend python manage.py createsuperuser
```

The backend will be available at `http://localhost:8000`
Admin panel: `http://localhost:8000/admin/`

### Local Development (without Docker)

#### Backend

1. Create virtual environment
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create .env file
```bash
cp .env.example .env
```

4. Run PostgreSQL and Redis (with Docker)
```bash
docker run -d --name twitter_db -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=twitter_clone postgres:16-alpine
docker run -d --name twitter_redis -p 6379:6379 redis:7-alpine
```

5. Run migrations
```bash
python manage.py migrate
```

6. Create superuser
```bash
python manage.py createsuperuser
```

7. Run development server
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout
- `POST /api/auth/token/refresh/` - Refresh JWT token

### Users
- `GET /api/users/me/` - Get current user
- `PATCH /api/users/me/` - Update current user profile
- `GET /api/users/{username}/` - Get user profile
- `GET /api/users/{username}/followers/` - Get user followers
- `GET /api/users/{username}/following/` - Get user following
- `POST /api/users/{username}/follow/` - Follow user
- `DELETE /api/users/{username}/unfollow/` - Unfollow user
- `GET /api/users/search/?q=query` - Search users

## Environment Variables

See `backend/.env.example` for all available environment variables.

Key variables:
- `DEBUG` - Debug mode (True/False)
- `SECRET_KEY` - Django secret key
- `DB_NAME` - Database name
- `DB_USER` - Database user
- `DB_PASSWORD` - Database password
- `DB_HOST` - Database host
- `REDIS_HOST` - Redis host

## Contributing

1. Follow PEP 8 style guide
2. Write clean, maintainable code
3. Follow SOLID principles
4. No comments in code unless absolutely necessary

## License

MIT
