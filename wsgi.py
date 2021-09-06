from app import app as application
import sys
import site

site.addsitedir('/var/www/AutoScale/venv/lib/python3.7/site-packages')


sys.path.insert(0, '/var/www/AutoScale')

if __name__ == "__main__":
	application.run()
