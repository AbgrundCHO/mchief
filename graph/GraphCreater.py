from graph.utils import link2neo4j, create_relation, create_node
import os
from py2neo import Node
import pandas as pd


class GraphCreater:
    # 该类用于将数据绘制成知识图谱
    def __init__(self):
        self.graph = link2neo4j()
        self.datapath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'datasets'))
        self.stations_dir = os.path.join(self.datapath, 'stations')

    def initialize_graph(self):
        self._create_orgs()

    def _create_orgs(self):
        # 该函数负责绘制部队编制组织图
        orgs = self.graph.run("match (p:部队) return p.name")
        orgs_name_list = list()
        for org in orgs:
            orgs_name_list.append(org[0])

        orgs_data = pd.read_csv(os.path.join(self.datapath, 'universal', '部队编制.csv'), encoding='gbk')
        for i in range(len(orgs_data)):
            if orgs_data['部队名称'][i] not in orgs_name_list:
                orgs_name_list.append(orgs_data['部队名称'][i])
                node = Node('部队', name=orgs_data['部队名称'][i],
                            部队内码=orgs_data['部队内码'][i],
                            直属上级=orgs_data['直属上级'][i])
                self.graph.create(node)
            else:
                search_node = self.graph.run("match (p:部队) where p.name='%s' return p.部队内码, p.直属上级"
                                             % orgs_data['部队名称'][i]).data()[0]
                node = {'部队内码': search_node['p.部队内码'],
                        '直属上级': search_node['p.直属上级'], }

            # 绘制部队之间的隶属关系
            create_relation(self.graph, '部队', '部队', node['直属上级'], node['部队内码'])

        return None

    def initialize_stations(self):
        '''
        该函数用于台站批量初始化
        :return: None
        '''
        self.clear_graph()
        stations_list = os.listdir(self.stations_dir)
        for station in stations_list:
            self.__initialize_station(os.path.join(self.stations_dir, station))

        return None

    def __initialize_station(self, station_dir):
        try:
            station_info = pd.read_csv(os.path.join(station_dir, 'station_info.csv'), encoding='gbk')
        except FileNotFoundError:
            return None

        # 生成台站节点
        create_node(self.graph, '台站',
                    {'name': station_info['台站名称'][0],
                     '代号': station_info['台站代号'][0],
                     '机房面积': station_info['机房面积'][0]})

        # 生成路由信息
        self.__initialize_routes(station_dir, station_info['台站名称'][0])
        self.__initialize_equips(station_dir, station_info['台站名称'][0])

        return None

    def __initialize_routes(self, station_dir, station_name):
        '''
        该函数用于生成路由连接部分的图谱
        :param station_dir: 台站文件夹
        :param station_name: 台站名称
        :return:
        '''
        try:
            stations_data = pd.read_csv(os.path.join(station_dir, 'routes.csv'), encoding='gbk')
        except FileNotFoundError:
            return None

        # 生成路由节点
        for i in range(len(stations_data)):
            # 建立线路节点
            create_node(self.graph, '线路',
                        {'name': stations_data['线路名称'][i],
                         '纤芯数量': stations_data['纤芯数量'][i],
                         '在用纤芯': stations_data['承载系统'][i],
                         '不可用纤芯': str(stations_data['不可用纤芯'][i]).replace('、', '/')})

            # 创建至台站连接
            # 本端台站至线路的连接
            create_relation(self.graph, '台站', '线路', station_name, stations_data['线路名称'][i])
            # 对端台站到线路的连接
            create_relation(self.graph, '台站', '线路', stations_data['通达方向'][i], stations_data['线路名称'][i])
            # 台站到台站之间的连接
            create_relation(self.graph, '台站', '台站', station_name, stations_data['通达方向'][i])

            # 建立系统节点
            systems = str(stations_data['承载系统'][i]).split('、')
            for j in range(len(systems)):
                system = systems[j].split('[')[0]
                if str(system) == 'nan':
                    break

                create_node(self.graph, '系统', {'name': system})
                create_relation(self.graph, '台站', '系统', station_name, system)
                create_relation(self.graph, '线路', '系统', stations_data['线路名称'][i], system)

            # 建立中继节点
            relays = str(stations_data['中继站'][i]).split('、')
            for relay in relays:
                if relay == 'nan':
                    break
                create_node(self.graph, '中继', {'name': relay})
                create_relation(self.graph, '线路', '中继', stations_data['线路名称'][i], relay)

        return None

    def __initialize_equips(self, station_dir, station_name):
        try:
            equips_data = pd.read_csv(os.path.join(station_dir, 'equips.csv'), encoding='gbk')
        except FileNotFoundError:
            return None

        # 生成设备节点
        for i in range(len(equips_data)):
            create_node(self.graph, '设备',
                        {'name': equips_data['设备类型'][i],
                         '名称': equips_data['设备名称'][i],
                         '编码': equips_data['设备编码'][i]},
                        overwrite=False)

            # 建立台站到设备的连接
            create_relation(self.graph, '台站', '设备', station_name, equips_data['设备编码'][i], sub_key='编码')
            # 建立设备到设备的连接
            for equ in str(equips_data['连接设备'][i]).split('、'):
                if equ == '' or equ == 'nan':
                    continue
                create_relation(self.graph, '设备', '设备', equips_data['设备编码'][i],
                                int(equ), main_key='编码', sub_key='编码', newnode=False)
            # 建立设备到线路的连接
            for route in equips_data['连接路由'][i].split('、'):
                create_relation(self.graph, '设备', '线路', equips_data['设备编码'][i], route, main_key='编码')

    def clear_graph(self):
        '''
        该函数用于清空知识图谱，慎用！
        :return: None
        '''
        self.graph.run('match(n) detach delete n')

        return None


if __name__ == '__main__':
    g = GraphCreater()
    g.initialize_stations()
