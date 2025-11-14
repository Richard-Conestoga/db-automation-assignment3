# Database Automation Project

## 🎯 Project Overview

This project demonstrates **Database DevOps Automation** using:
- **Ansible** for infrastructure provisioning
- **Flyway** for database migrations
- **GitHub Actions** for CI/CD
- **pytest** for automated testing

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.8+ (with venv)
- Git

## 🚀 Quick Start

### 1. Setup Local Environment 

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Ansible collections
ansible-galaxy collection install community.docker
ansible-galaxy collection install community.mysql
```

### 2. Provision MySQL Environment

```bash
# Make sure virtual environment is activated!
source venv/bin/activate

cd ansible
ansible-playbook -i inventory.yml up.yml
```

This will:
- Start a MySQL 8.0 container
- Create the `subscribers_db` database
- Create a database user
- Run initial and incremental Flyway migrations


### 3. Run Tests Locally

```bash
# Make sure virtual environment is activated
source venv/bin/activate

cd tests
pip install -r requirements.txt

pytest test_subscribers.py -v
```

### 5. Tear Down Environment

```bash
# Virtual environment should still be activated
cd ansible
ansible-playbook -i inventory.yml down.yml
```

### 6. Deactivate Virtual Environment (when done)

```bash
deactivate
```

## 🔄 CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) automatically:

1. ✅ Spins up MySQL service
2. ✅ Runs initial migrations
3. ✅ Runs incremental migrations
4. ✅ Executes CRUD tests
5. ✅ Reports deployment status

**Triggers:**
- Push to `main` branch
- Pull requests to `main`

## 📊 Database Schema

### Initial Schema (V1)
```sql
CREATE TABLE subscribers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### After Incremental Migration (V2)
- ✅ Email column added with UNIQUE constraint
- ✅ Index on last_name created
- ✅ Index on email created

## 🧪 Test Coverage

The test suite covers:
- ✅ **CREATE**: Insert new subscribers
- ✅ **READ**: Retrieve subscriber data
- ✅ **UPDATE**: Modify subscriber information
- ✅ **DELETE**: Remove subscribers
- ✅ **INDEXES**: Verify database optimization
- ✅ **CONSTRAINTS**: Test email uniqueness


