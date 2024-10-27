# FastAPI Organizations

This is a FastAPI application for managing organizations and their members. It includes features such as user authentication, organization creation, and member management.

## Features

- User authentication with JWT tokens
- Organization creation and management
- Member invitation and management
- Token blacklisting using Redis
- MongoDB for data storage

## Requirements

- Docker
- Docker Compose

## Quick Start with Docker

1. **Clone the repository:**

   ```bash
   git clone https://github.com/oel21sakka/fastapi-organizations.git
   cd fastapi-organizations
   ```

2. **Set up environment variables:**

   Create a `.env` file in the root directory with the following content:

   ```env
   SECRET_KEY=your_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REFRESH_TOKEN_EXPIRE_DAYS=7
   MONGODB_URL=mongodb://mongo:27017
   DATABASE_NAME=fastapi-organizations
   REDIS_URL=redis://redis:6379
   ```

3. **Build and run the Docker containers:**

   ```bash
   docker-compose up --build
   ```

4. **Access the application:**

   The application will be available at `http://localhost:8000`.

## Usage

- **API Documentation:** Access the interactive API documentation at `http://localhost:8000/docs`.
- **Redoc Documentation:** Access the ReDoc documentation at `http://localhost:8000/redoc`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [MongoDB](https://www.mongodb.com/)
- [Redis](https://redis.io/)
- [Docker](https://www.docker.com/)

