python_home = "/var/www/AutoScale/venv"

import sys, site

python_version = ".".join(map(str, sys.version_info[:2]))


site_packages = python_home + '/lib/python%s/site-packages'% python_version
site.addsitedir("/home/centos/.local/lib/python3.7/site-packages")
sys.path.insert(0, "/var/www/AutoScale")

from app import app as application

if __name__ == "__main__":
	application.run()
