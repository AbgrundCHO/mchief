from login import read_ras_password, decode2str
from py2neo import Graph
import numpy as np


def link2neo4j():
    __username, __password = read_ras_password()
    link = Graph('http://localhost:7474',
                 username=decode2str(__username),
                 password=decode2str(__password))
    return link


def create_relation(graph, main_node, sub_node, main_name, sub_name,
                    relation_name=None, main_key='name', sub_key='name'):
    '''
    该函数用于建立简单的实体间关系
    :param graph: 图数据库连接
    :param main_node: 起始节点类型，Str
    :param sub_node: 指向节点类型，Str
    :param main_name: 起始节点名称，Str
    :param sub_name: 指向节点名称，Str
    :param relation_name: 关系名称，default = p_q
    :return: None
    '''
    if relation_name is None:
        relation_name = main_node + '_' + sub_node

    temp_bool = graph.run("match (p:{0}) where p.{1}='{2}' return p".format(sub_node, sub_key, sub_name)).data()
    if not temp_bool:
        graph.run("create (n:{0}{1})".format(sub_node, '{name:\'' + str(sub_name) + '\'}'))

    temp_bool = graph.run('''match (p:{0})-[r:{1}]-(q:{2})
    where p.{3}='{4}' and q.{5}='{6}'
    return r'''.format(main_node, relation_name, sub_node, main_key, main_name, sub_key, sub_name)).data()

    if not temp_bool:
        graph.run('''match (p:{0}), (q:{1})
        where p.{2}='{3}' and q.{4}='{5}'
        create (p)-[rel:{6}]->(q)
        '''.format(main_node, sub_node, main_key, main_name, sub_key, sub_name, relation_name))

    return None


def create_node(graph, node_type, node_dict):
    '''
    该函数用于创建知识图谱节点，有查重功能
    :param graph: 图数据库连接
    :param node_type: 节点类型，Str
    :param node_dict: 节点属性，Dict
    :return: None
    '''
    temp_bool = graph.run("match (p:{0}) where p.name='{1}' return p".format(node_type, node_dict['name'])).data()
    if not temp_bool:
        graph.run('create (n:{0}{1})'.format(node_type, rebuild_node_dict(node_dict)))
    else:
        graph.run("match (p:{0}) where p.name='{1}' set {2}"
                  .format(node_type, node_dict['name'], rewrite_node_dict(node_dict)))

    return None


def rebuild_node_dict(node_dict):
    '''
    该函数用于生成新节点过程中整理节点属性
    :param node_dict: 节点属性字典
    :return: 整理后的节点属性字符串
    '''
    query = '{'
    for k, v in node_dict.items():
        if isinstance(v, str):
            query += k + ':\'' + v + '\','
        else:
            query += k + ':' + str(v) + ','

    query = query[:-1] + '}'

    return query


def rewrite_node_dict(node_dict):
    '''
    该函数用于增加节点属性过程中整理节点属性
    :param node_dict: 节点属性字典
    :return: 整理后的节点属性字符串
    '''
    query = ''
    for k, v in node_dict.items():
        if isinstance(v, str):
            query += 'p.' + k + '=\'' + v + '\','
        elif str(v) == 'nan':
            query += 'p.' + k + '=\'' + str(v) + '\','
        else:
            query += 'p.' + k + '=' + str(v) + ','

    query = query[:-1]

    return query
