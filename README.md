# Django Library management


Features

    Book Management: Create, read, update, and delete books.

    Filtering: Filter books by author, published date, and language.

    Pagination: Paginate the list of books.
    
    Swagger API documentation

    Authentication: JWT token-based authentication.

    Permissions: Read-only access for unauthenticated users; full access for authenticated users.





## Setup

### Prerequisites

- Python 3.8+
- Docker

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Daniil-Pankieiev/library-management.git
    cd library-management
    ```

2. **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    ```
   Activate On macOS and Linux:
   ```bash
   source venv/bin/activate
   ```
   On Windows:
   ```bash
   venv\Scripts\activate
   ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply the migrations:

   ```bash
   python manage.py makemigrations
   ```

5. **Run migrations**:
    ```bash
    python manage.py migrate
    ```

6 **Run the development server**:
    ```bash
    python manage.py runserver
    ```
### Using Docker
```bash
docker compose up --build
```

### Create super user
```bash
docker  exec -it library_backend-api-1  python manage.py createsuperuser
```

### Populate Database with Example Data

To populate the database with example data, run the following management command:

```bash
docker  exec library_backend-api-1  python manage.py generate_books

```
### Tests
Run tests:
```bash
docker  exec library_backend-api-1  python manage.py test

```
###  Usage

Navigate to http://127.0.0.1:8000/api/swagger/ to see SWAGGER documentation
Register and use access token in headers with Bearer key

