class SemanticElement:
    def __init__(self, num, label, form):
        self.num = num
        self.label = label
        self.form = form


class SemanticRelation:
    def __init__(self):
        self.subject = None
        self.object = None
        self.relation = None

    def complete_by_relation(self, seg, sdp):
        subject_type = ['AGT', 'EXP']
        object_type = ['PAT', 'CONT', 'DATV', 'LINK']
        for triple in sdp:
            if triple[1] == self.relation:
                if triple[2] in subject_type:
                    self.subject = seg[triple[0]]
                elif triple[2] in object_type:
                    self.object = seg[triple[0]]
                sdp.remove(triple)

        return sdp
