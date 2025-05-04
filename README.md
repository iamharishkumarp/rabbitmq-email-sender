# Email Notification Service

A microservice-based email notification system built with Flask, RabbitMQ, and PostgreSQL. This service allows users to register, login, and send emails through a message queue system.

## Features

- User registration and authentication
- Email sending through RabbitMQ message queue
- PostgreSQL database for user management
- Dockerized deployment
- SMTP email integration

## Tech Stack

- **Backend**: Python/Flask
- **Database**: PostgreSQL
- **Message Queue**: RabbitMQ
- **Containerization**: Docker
- **Email Service**: SMTP (Gmail)

## Prerequisites

- Docker and Docker Compose
- Gmail account (for SMTP)
- Python 3.9+ (for local development)

## Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd email-notify
```

2. Create a `.env` file in the root directory with your SMTP credentials:
```
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_specific_password
```

3. Build and start the services:
```bash
docker-compose up --build
```

## API Endpoints

### User Management

- **Signup**
  ```
  POST /email/signup
  Content-Type: application/json
  
  {
      "email": "user@example.com",
      "password": "password123"
  }
  ```

- **Login**
  ```
  POST /email/login
  Content-Type: application/json
  
  {
      "email": "user@example.com",
      "password": "password123"
  }
  ```

- **Change Password**
  ```
  POST /email/change-password
  Content-Type: application/json
  
  {
      "email": "user@example.com",
      "new_password": "newpassword123"
  }
  ```

- **Logout**
  ```
  POST /email/logout
  Content-Type: application/json
  
  {
      "email": "user@example.com"
  }
  ```

### Email Service

- **Send Email**
  ```
  POST /email/send-email
  Content-Type: application/json
  
  {
      "to": "recipient@example.com",
      "subject": "Test Email",
      "message": "This is a test email"
  }
  ```

## Service Architecture

The application consists of three main services:

1. **Web Service** (`web`): Flask application handling HTTP requests
2. **Worker Service** (`worker`): Processes email queue and sends emails
3. **Database** (`db`): PostgreSQL database for user management
4. **Message Queue** (`rabbitmq`): RabbitMQ for message queuing

## Accessing Services

- **Flask Application**: http://localhost:5000
- **RabbitMQ Management**: http://localhost:15672
  - Username: guest
  - Password: guest

## Development

### Docker Development

1. Build and start all services:
```bash
docker-compose up --build
```

2. To view logs for a specific service:
```bash
docker-compose logs -f web    # For Flask application logs
docker-compose logs -f worker # For worker logs
docker-compose logs -f db     # For database logs
docker-compose logs -f rabbitmq # For RabbitMQ logs
```

3. To stop the services:
```bash
docker-compose down
```

4. To stop and remove all containers and volumes (fresh start):
```bash
docker-compose down -v
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Flask
- RabbitMQ
- PostgreSQL
- Docker 