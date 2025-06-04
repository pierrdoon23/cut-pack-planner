[English version](#Graduation-qualification-project)

# Дипломная работа
Данная дипломная работа создана для оптимизации автоматизации процессов по нарезке упаковки
и использовались инструменты такие как: 
Python3, FastApi, SQLAlchemy, PostgreSQL, typescript, react, tailwindcss, redux, vite

---

## Требования

- Python 3.8 или выше
- PostgreSQL
- npm 10.9.2 или выше

---

## Для запуска приложения потребуется

### 1. Создайте виртуальное окружение:
```bash
python -m venv venv
```

### 2. Активируйте виртуальное окружение:
- Windows:
```bash
.\venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

### 3. Установите зависимости:
```bash
pip install -r requirements.txt
```

### 4. Создайте файл `.env` в директории backend со следующим содержимым:
```
DATABASE_URL=postgresql://user:password@localhost:5432/your_db

HOST=127.0.0.1
PORT=8080

```

### 5. Запустить бэкенд(парсер)
   ```bash
      cd backend

      python -m app.run
   ```
   или
   ```bash
      cd backend

      python3 -m app.run
   ```
   
### 6. Запустить фронтенд
   ```bash
      cd frontend

      npm i 

      npm run dev
   ```

---

## Миграции базы данных

Для применения миграций базы данных:

```bash
alembic upgrade head
```

Для создания новой миграции:

```bash
alembic revision --autogenerate -m "описание изменений"
```

---

# Graduation qualification project
This final qualification work was created to optimise the automation of packaging slicing processes and used tools such as: Python3, FastApi, SQLAlchemy, PostgreSQL, typescript, react, tailwindcss, redux, vite

---

## Requirements

- Python 3.8 or higher
- PostgreSQL
- npm 10.9.2 or higher

---

## To run the application

### 1. Create a virtual environment:
```bash
python -m venv venv
```

### 2. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file in the backend directory with the following content:
```
DATABASE_URL=postgresql://user:password@localhost:5432/your_db

HOST=127.0.0.1
PORT=8080

```

### 5. Start the backend (parser)
   ```bash
      cd backend

      python -m app.run
   ```
   or
   ```bash
      cd backend

      python3 -m app.run
   ```
   
### 6. Start the frontend
   ```bash
      cd frontend

      npm i 

      npm run dev
   ```

---

## Database Migrations

To apply database migrations:

```bash
alembic upgrade head
```

To create a new migration:

```bash
alembic revision --autogenerate -m "description of changes"
``` 
