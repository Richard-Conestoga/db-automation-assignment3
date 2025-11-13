import os
import pytest
import pymysql
from datetime import datetime


class TestSubscribers:
    """Test suite for subscribers CRUD operations"""
    
    @pytest.fixture(scope="class")
    def db_connection(self):
        """Create database connection fixture"""
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER', 'dbuser'),
            password=os.getenv('DB_PASSWORD', 'dbpassword123'),
            database=os.getenv('DB_NAME', 'subscribers_db'),
            cursorclass=pymysql.cursors.DictCursor
        )
        yield connection
        connection.close()
    
    @pytest.fixture(autouse=True)
    def cleanup(self, db_connection):
        """Clean up test data before each test"""
        with db_connection.cursor() as cursor:
            # Remove any test subscribers
            cursor.execute(
                "DELETE FROM subscribers WHERE email = %s",
                ('test.user@example.com',)
            )
        db_connection.commit()
        yield
        # Cleanup after test
        with db_connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM subscribers WHERE email = %s",
                ('test.user@example.com',)
            )
        db_connection.commit()
    
    def test_01_create_subscriber(self, db_connection):
        """
        Test CREATE operation
        Verify that a new subscriber can be inserted into the database
        """
        with db_connection.cursor() as cursor:
            # Insert a new subscriber
            sql = """
                INSERT INTO subscribers (first_name, last_name, phone, email)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, ('Test', 'User', '555-9999', 'test.user@example.com'))
            db_connection.commit()
            
            # Verify insertion
            cursor.execute(
                "SELECT * FROM subscribers WHERE email = %s",
                ('test.user@example.com',)
            )
            result = cursor.fetchone()
            
            assert result is not None, "Subscriber was not created"
            assert result['first_name'] == 'Test'
            assert result['last_name'] == 'User'
            assert result['phone'] == '555-9999'
            assert result['email'] == 'test.user@example.com'
            
            print(f"✅ CREATE Test Passed: Subscriber ID {result['id']} created")
    
    def test_02_read_subscriber(self, db_connection):
        """
        Test READ operation
        Verify that a subscriber can be retrieved from the database
        """
        # First, create a subscriber to read
        with db_connection.cursor() as cursor:
            sql = """
                INSERT INTO subscribers (first_name, last_name, phone, email)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, ('Test', 'User', '555-9999', 'test.user@example.com'))
            db_connection.commit()
            subscriber_id = cursor.lastrowid
        
        # Now test reading
        with db_connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM subscribers WHERE id = %s",
                (subscriber_id,)
            )
            result = cursor.fetchone()
            
            assert result is not None, "Subscriber not found"
            assert result['id'] == subscriber_id
            assert result['first_name'] == 'Test'
            assert result['email'] == 'test.user@example.com'
            assert 'created_at' in result
            assert 'updated_at' in result
            
            print(f"✅ READ Test Passed: Retrieved subscriber ID {subscriber_id}")
    
    def test_03_update_subscriber(self, db_connection):
        """
        Test UPDATE operation
        Verify that a subscriber's information can be modified
        """
        # Create a subscriber
        with db_connection.cursor() as cursor:
            sql = """
                INSERT INTO subscribers (first_name, last_name, phone, email)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, ('Test', 'User', '555-9999', 'test.user@example.com'))
            db_connection.commit()
            subscriber_id = cursor.lastrowid
        
        # Update the subscriber
        with db_connection.cursor() as cursor:
            update_sql = """
                UPDATE subscribers 
                SET first_name = %s, phone = %s
                WHERE id = %s
            """
            cursor.execute(update_sql, ('Updated', '555-0000', subscriber_id))
            db_connection.commit()
            
            # Verify update
            cursor.execute(
                "SELECT * FROM subscribers WHERE id = %s",
                (subscriber_id,)
            )
            result = cursor.fetchone()
            
            assert result is not None
            assert result['first_name'] == 'Updated', "First name was not updated"
            assert result['phone'] == '555-0000', "Phone was not updated"
            assert result['last_name'] == 'User', "Last name should remain unchanged"
            
            print(f"✅ UPDATE Test Passed: Subscriber ID {subscriber_id} updated")
    
    def test_04_delete_subscriber(self, db_connection):
        """
        Test DELETE operation
        Verify that a subscriber can be removed from the database
        """
        # Create a subscriber
        with db_connection.cursor() as cursor:
            sql = """
                INSERT INTO subscribers (first_name, last_name, phone, email)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, ('Test', 'User', '555-9999', 'test.user@example.com'))
            db_connection.commit()
            subscriber_id = cursor.lastrowid
        
        # Delete the subscriber
        with db_connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM subscribers WHERE id = %s",
                (subscriber_id,)
            )
            db_connection.commit()
            
            # Verify deletion
            cursor.execute(
                "SELECT * FROM subscribers WHERE id = %s",
                (subscriber_id,)
            )
            result = cursor.fetchone()
            
            assert result is None, "Subscriber was not deleted"
            
            print(f"✅ DELETE Test Passed: Subscriber ID {subscriber_id} deleted")
    
    def test_05_verify_indexes(self, db_connection):
        """
        Test that required indexes exist
        Verify database optimization
        """
        with db_connection.cursor() as cursor:
            cursor.execute("SHOW INDEX FROM subscribers")
            indexes = cursor.fetchall()
            
            index_names = [idx['Key_name'] for idx in indexes]
            
            # Check for required indexes
            assert 'PRIMARY' in index_names, "Primary key index missing"
            assert 'idx_last_name' in index_names, "last_name index missing"
            assert 'idx_email' in index_names, "email index missing"
            
            print(f"✅ INDEX Test Passed: All required indexes exist")
    
    def test_06_email_uniqueness(self, db_connection):
        """
        Test email uniqueness constraint
        Verify that duplicate emails are rejected
        """
        with db_connection.cursor() as cursor:
            # Insert first subscriber
            sql = """
                INSERT INTO subscribers (first_name, last_name, phone, email)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, ('Test', 'User', '555-9999', 'test.user@example.com'))
            db_connection.commit()
            
            # Try to insert duplicate email
            with pytest.raises(pymysql.IntegrityError) as exc_info:
                cursor.execute(sql, ('Another', 'User', '555-8888', 'test.user@example.com'))
                db_connection.commit()
            
            assert "Duplicate entry" in str(exc_info.value)
            print(f"✅ UNIQUENESS Test Passed: Duplicate email rejected")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])