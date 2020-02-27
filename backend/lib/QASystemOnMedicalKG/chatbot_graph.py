#!/usr/bin/env python3
# coding: utf-8
# File: chatbot_graph.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

from . import *
# from question_classifier import *
# from question_parser import *
# from answer_search import *
# from decision_tree import *

# 设置默认文件编码utf8
import _locale
_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])

dialog_state_table = ["Answering", "Questioning"]

'''问答类'''


class ChatBotGraph:
    def __init__(self):
        self.dialog_state = dialog_state_table[0]
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        if self.dialog_state == "Answering":
            init_answer = '没答上来'
            res_classify = self.classifier.classify(sent)
            if not res_classify:
                return init_answer
            res_sql = self.parser.parser_main(res_classify)
            print(res_sql)
            self.dialog_state, final_answers, desc = self.searcher.search_main(
                res_sql)
            if self.dialog_state == "Questioning":
                self.decision_tree = DecisionTree(desc)
                self.decision_tree.build()
                question = self.decision_tree.ask()
                return question

            elif self.dialog_state == "Answering":
                if not final_answers:
                    return init_answer
                else:
                    return '\n'.join(final_answers)
        elif self.dialog_state == "Questioning":
            ###  sent  --> int or list
            self.dialog_state,answer = self.decision_tree.reply(int(sent))
            return answer







if __name__ == '__main__':
    handler = ChatBotGraph()
    while 1:
        question = input('用户:')
        answer = handler.chat_main(question)
        print('小勇:', answer)
