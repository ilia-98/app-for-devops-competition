import argparse
import ipaddress
from app import app, Settings


def is_ip(ip_addr):
    try:
        ipaddress.ip_address(ip_addr)
    except ValueError:
        print('something went wrong')
        raise


parser = argparse.ArgumentParser()
parser.add_argument('--ad_ip_addr', dest='ad_ip_addr', action='store', help='Windows Server IP address with AD DS')
parser.add_argument('--db_conn_string', dest='db_conn_string', action='store', help='Database connection string')
parser.add_argument('--external_link', dest='external_link', action='store', help='External link')
parser.add_argument('--storage_path', dest='storage_path', action='store', help='Path to the directory for storing files in the OS')

args = parser.parse_args()

is_ip(args.ad_ip_addr)
Settings.AD_IP_ADDR = args.ad_ip_addr
Settings.DB_CONN_STRING = args.db_conn_string
Settings.EXTERNAL_LINK = args.external_link
Settings.STORAGE_PATH = args.storage_path

from app import auth_views
from app import api_views
from app import web_views
from app.database import db_session, init_db

init_db()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


app.run(host='0.0.0.0')

