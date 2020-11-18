'''
此文件用于调用 LTP 方法
'''
from ltp import LTP
import os

# 超参数：文件路径
# LTP 模型参数文件路径, 将权重文件放在本目录下 weights 文件夹下可直接写为 None 。
LtpModelPath = 'D:\KG\LTP_model\weights'


class LtpModel:
    '''
    该类用于实例化 LTP 模型，并进行相关操作
    '''
    def __init__(self, weights_type='base'):
        # 载入模型参数
        self.ltp_model = self.load_ltp_weights(weights_type)

        # 初始化用户词典
        # 确认用户自定义词典路径
        self.UserDictPath = os.path.join(os.path.join(os.path.dirname(__file__)), 'user_dict.txt')
        # 初始化最大前向分词窗口
        self.MaxWindow = self.init_user_dict_maxlength()
        self.ltp_model.init_dict(path=self.UserDictPath, max_window=self.MaxWindow)

    @staticmethod
    def load_ltp_weights(weights_type):
        '''
        加载 LTP 权重文件，实例化 LTP 模型
        :param weights_type: 载入模型文件类型，只能采用 base、small、tiny 三种类型
        :return: 载入权重参数后的 LTP 模型
        '''
        # 诊断模型类型
        assert weights_type in ['base', 'small', 'tiny'], 'LTP 模型只能采用 base、small、tiny三种类型的参数'

        # 确认文件路径
        if LtpModelPath is None:
            file_path = os.path.abspath(os.path.join(os.path.dirname('.'), 'weights', weights_type))
        else:
            file_path = os.path.abspath(os.path.join(LtpModelPath, weights_type))

        # 载入权重
        ltp = LTP(path=file_path)

        return ltp

    def init_user_dict_maxlength(self, max_word_len=4):
        '''
        此函数用于初始化最大前向分词窗口，即分词最大长度
        :param max_word_len: 最大前向分词窗口最小阈值，默认为 4
        :return: 分词最大长度
        '''
        # 读取用户自定义词典
        with open(self.UserDictPath, 'r', encoding='gbk') as fp:
            user_dict = fp.readlines()
        # 查询词典最大长度
        for word in user_dict:
            word_len = len(word) - 1
            if word_len > max_word_len:
                max_word_len = word_len

        return max_word_len

    def update_user_dict(self, new_words):
        '''
        此函数用于更新用户自定义词典
        :param new_words: 待更新的新单词，List/Str
        :return: None
        '''
        # 读取用户自定义词典文件
        with open(self.UserDictPath, 'a+', encoding='gbk') as fp:
            # List 类型批量添加
            if isinstance(new_words, list):
                for new_word in new_words:
                    # 在文件中写入新单词
                    fp.write(new_word + '\n')
                    # 词典更新
                    self.reload_user_dict(new_word)
            # Str 类型单个添加
            elif isinstance(new_words, str):
                # 在文件中写入新单词
                fp.write(new_words + '\n')
                # 词典更新
                self.reload_user_dict(new_words)
            # 若非 List/Str 类型则报错
            else:
                raise Exception('只能用 List/Str 更新用户词典！')

        return None

    def reload_user_dict(self, new_word):
        '''
        此函数用于更新用户自定义词典
        :param new_word: 需更新的新单词
        :return: None
        '''
        # 判断是否需要更新最大前向分词窗口
        new_word_length = len(new_word)
        if new_word_length > self.MaxWindow:
            self.MaxWindow = new_word_length

        # 更新用户自定义词典
        self.ltp_model.add_words(words=[new_word], max_window=self.MaxWindow)

        return None


if __name__ == '__main__':
    pass
