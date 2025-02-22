# FastAPI-Project
FastAPI Social Media API is a FastAPI-based Social Media API that provides:

User authentication
Post creation
Like system
It uses PostgreSQL as the database and follows best practices in API security and authentication.

Features
User Authentication

OAuth2 and password hashing
JWT-based access token generation
Post Management

Create and retrieve posts
Associate posts with users
Like System

Users can like/unlike posts
Prevent duplicate likes
Database

Uses SQLAlchemy ORM
PostgreSQL database connection
Dependency Injection

Depends() for database session and authentication
Error Handling

Returns meaningful HTTP exceptions for invalid actions
