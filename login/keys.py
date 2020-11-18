import codecs
from login.utils import decode_message, create_keys, encode_message
import os

USERNAME = 'neo4j'
PASSWORD = 'password'
key_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'neo4juser', 'password.pem'))


def read_ras_password():
    with open(key_path, 'r') as f:
        username = f.readline().strip()
        password = f.readline().strip()

    return username, password


def decode2str(str_info):
    str_info = bytes(str_info[2:-1], encoding='utf8')
    str_info = codecs.escape_decode(str_info, 'hex-escape')[0]
    str_info = decode_message(str_info)

    return str_info


def update_neo4j_user_info(username=USERNAME, password=PASSWORD):
    """
    该文件用于加密 Neo4j 数据库的用户名和密码，
    新用户执行后即可连接至数据库。
    """
    create_keys()
    with open(key_path, 'w') as f:
        f.write('')
    with open(key_path, 'w+') as f:
        f.write(str(encode_message(username)))
        f.write('\n')
        f.write(str(encode_message(password)))

    return None
