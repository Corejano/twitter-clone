# Postman API Testing Guide

## Setup

Base URL: `http://localhost:8000/api`

## 1. Register User

**POST** `/auth/register/`

Body (JSON):
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "full_name": "Test User",
  "password": "password123",
  "password_confirm": "password123"
}
```

Response: Returns user data + JWT tokens (access, refresh)

---

## 2. Login

**POST** `/auth/login/`

Body (JSON):
```json
{
  "username": "testuser",
  "password": "password123"
}
```

Response: Returns user data + JWT tokens

**Important:** Copy the `access` token from response for next requests

---

## 3. Get Current User

**GET** `/users/me/`

Headers:
```
Authorization: Bearer <your_access_token>
```

---

## 4. Update Profile

**PATCH** `/users/me/`

Headers:
```
Authorization: Bearer <your_access_token>
```

Body (JSON):
```json
{
  "full_name": "Updated Name",
  "bio": "This is my bio"
}
```

---

## 5. Get User Profile

**GET** `/users/{username}/`

Example: `GET /users/testuser/`

No auth required

---

## 6. Follow User

**POST** `/users/{username}/follow/`

Headers:
```
Authorization: Bearer <your_access_token>
```

Example: `POST /users/anotheruser/follow/`

---

## 7. Unfollow User

**DELETE** `/users/{username}/unfollow/`

Headers:
```
Authorization: Bearer <your_access_token>
```

---

## 8. Get Followers

**GET** `/users/{username}/followers/`

---

## 9. Get Following

**GET** `/users/{username}/following/`

---

## 10. Search Users

**GET** `/users/search/?q=test`

---

## 11. Refresh Token

**POST** `/auth/token/refresh/`

Body (JSON):
```json
{
  "refresh": "<your_refresh_token>"
}
```

---

## 12. Logout

**POST** `/auth/logout/`

Headers:
```
Authorization: Bearer <your_access_token>
```

Body (JSON):
```json
{
  "refresh": "<your_refresh_token>"
}
```

---

## Quick Test Flow

1. Register new user → Get tokens
2. Create another user (change username/email)
3. Login with first user → Copy access token
4. Add token to Authorization header (Bearer token)
5. Update profile (PATCH /users/me/)
6. Follow second user (POST /users/{username}/follow/)
7. Check followers (GET /users/{username}/followers/)
8. Search users (GET /users/search/?q=test)

---

## Tips

- Always add `Content-Type: application/json` header for POST/PATCH requests
- Save access token after login/register
- Token format: `Bearer eyJ0eXAiOiJKV1QiLCJhbGc...`
- Tokens expire after 60 minutes
