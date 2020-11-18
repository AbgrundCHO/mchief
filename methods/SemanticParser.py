from methods.SemanticClass import SemanticElement, SemanticRelation


class SemanticParser:
    def __init__(self, seg, sdp):
        # 待处理数据
        self.seg = seg[0].insert(0, 'ROOT')
        self.sdp = sdp[0]

        # 基本语义
        self.subject_type = ['AGT', 'EXP']
        self.object_type = ['PAT', 'CONT', 'DATV', 'LINK']

        # 语义主成分分析
        # self.main_subject, self.main_object, self.main_relation = self.host_element_parser()
        self.relationships = list()

    def host_element_parser(self):
        '''
        该函数用于分析句子的主成分
        :return:
        '''
        # 分析句子的主关系
        for sdp in self.sdp:
            if sdp[1] == 0:
                main_relation = SemanticRelation()
                main_relation.relation = self.seg[sdp[0]]
                self.sdp = main_relation.complete_by_relation(self.seg, self.sdp)

        # 根据句子的主关系分析句子的主语和宾语
        # for sdp in self.sdp:
        #     if sdp[2] in self.subject_type:

    # def semanticparse(self, semantic_triple):
    #     first_word, second_word, relation_word = semantic_triple
    #     if relation_word in self.subject_type:
    #         pass
    #     else relation_word in


if __name__ == '__main__':
    a = [(2, 3, 'EXP'), (3, 3, 'EXP'), (4, 3, 'EXP')]
    a.remove((3, 3, 'EXP'))
    print(a)
