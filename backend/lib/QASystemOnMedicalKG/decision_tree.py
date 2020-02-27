from py2neo import Graph
from . import *
#from question_parser import QuestionPaser


class DecisionTree:
    def __init__(self, desc):
        self.g = Graph("http://localhost:7474", auth=("neo4j", "ohahaha"))
        self.parser = QuestionPaser()
        self.num_limits = 5
        self.tree_dict = {}
        self.desc = desc
        self.last_question = {'question_type': 0, 'candidates': 0}

    def build(self):

        if not self.tree_dict:
            tree_dims = ['disease_not_food', 'disease_check', 'disease_drug']
            for question_type in tree_dims:
                self.tree_dict[question_type] = {i: [] for i in self.desc}
                queries = self.parser.sql_transfer(question_type, self.desc)
                for query in queries[:self.num_limits]:
                    result = self.g.run(query).data()
                    for answer in result:
                        self.tree_dict[question_type][answer['m.name']].append(
                            answer['n.name'])
            print(self.tree_dict)

    def ask(self):
        if self.tree_dict:
            question_type = list(self.tree_dict.keys())[0]
            ask_dict = self.tree_dict[question_type]
            candidates = []
            for d in self.desc:
                candidates += ask_dict[d]
            candidates = list(set(candidates))
            self.last_question['question_type'] = question_type
            self.last_question['candidates'] = candidates
            return question_type+'or'.join(candidates)

        else:
            return "no decision tree"

    def update(self, result):
        candi = self.last_question['candidates'][result-1]
        question_type = self.last_question['question_type']
        q_dict = self.tree_dict[question_type]
        del_list = []
        # 对于当前question_type 未命中且属性不为空的删除
        for disease in self.desc:
            if (q_dict[disease]) and (candi not in q_dict[disease]):
                del_list.append(disease)
        for del_disease in del_list:
            self.desc.remove(del_disease)
        del self.tree_dict[question_type]
        print(candi,del_list,self.desc, self.tree_dict)
    
    def reply(self,result):
        self.update(result)
        next_state = "Questioning"
        if len(self.desc) <=1 :
            next_state = "Answering"
            answer = self.reply_wrapper(self.desc)
            
            return next_state,answer
        answer = self.ask()

        return next_state,answer

    ### ? 一次update之后 len(desc)=0 怎么处理
    def reply_wrapper(self,desc:list):
        return "可能为疾病："+'、'.join(desc) 