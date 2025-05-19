# Cut Pack Planner Backend

This is the backend service for the Cut Pack Planner application.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the backend directory with the following content:
```
DATABASE_URL=sqlite:///./app.db
```

## Running the Application

To run the application in development mode:

```bash
python -m app.run
```

The server will start at http://127.0.0.1:8000

## API Documentation

Once the server is running, you can access:
- Swagger UI documentation at http://127.0.0.1:8000/docs
- ReDoc documentation at http://127.0.0.1:8000/redoc
