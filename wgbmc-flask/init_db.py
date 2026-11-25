"""Create the MySQL database/tables and reset the initial admin login."""
import os, pymysql
from werkzeug.security import generate_password_hash
host=os.getenv('DB_HOST','localhost'); user=os.getenv('DB_USER','root'); password=os.getenv('DB_PASS',''); name=os.getenv('DB_NAME','galii_baha_oromiyaa')
conn=pymysql.connect(host=host,user=user,password=password,charset='utf8mb4',autocommit=True)
try:
    with conn.cursor() as c:
        c.execute(f"CREATE DATABASE IF NOT EXISTS `{name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        c.execute(f"USE `{name}`")
        c.execute("""CREATE TABLE IF NOT EXISTS admins (
          id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
          username VARCHAR(80) NOT NULL UNIQUE,
          password_hash VARCHAR(255) NOT NULL,
          created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci""")
        c.execute("""CREATE TABLE IF NOT EXISTS revenue_records (
          id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
          category VARCHAR(40) NOT NULL, serial_no INT DEFAULT NULL,
          entity_name VARCHAR(160) NOT NULL,
          annual_plan DECIMAL(18,2) NOT NULL DEFAULT 0,
          annual_actual DECIMAL(18,2) NOT NULL DEFAULT 0,
          annual_percent DECIMAL(8,2) NOT NULL DEFAULT 0,
          daily_plan DECIMAL(18,2) NOT NULL DEFAULT 0,
          daily_actual DECIMAL(18,2) NOT NULL DEFAULT 0,
          daily_percent DECIMAL(8,2) NOT NULL DEFAULT 0,
          is_summary TINYINT(1) NOT NULL DEFAULT 0,
          created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
          updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          KEY idx_category(category), KEY idx_entity(entity_name), KEY idx_summary(is_summary)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci""")
        c.execute("SELECT id FROM admins WHERE username='admin'")
        row=c.fetchone(); hashed=generate_password_hash('ChangeMe123!')
        if row: c.execute("UPDATE admins SET password_hash=%s WHERE username='admin'",(hashed,))
        else: c.execute("INSERT INTO admins(username,password_hash) VALUES('admin',%s)",(hashed,))
finally: conn.close()
print('Database fi tables qophaa’aniiru. Admin login: admin / ChangeMe123!')
