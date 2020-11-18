print('''match (p:{0}), (q:{1})
        where p.{2}='{3}' and q.{4}='{5}'
        create (p)-[rel:{6}]->(q)
        '''.format('哈哈', 'hehe', 'main_key', 'main_value', '编码', 1144, 'relation_name'))