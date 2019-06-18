import pickle
import sys
import numpy as np
import torch
import tkinter
import test_wav

def load_data():
    with open('./data/Bosondata.pkl', 'rb') as inp:
        word2id = pickle.load(inp)
        id2word = pickle.load(inp)
        tag2id = pickle.load(inp)
        id2tag = pickle.load(inp)
        x_train = pickle.load(inp)
        y_train = pickle.load(inp)
        x_test = pickle.load(inp)
        y_test = pickle.load(inp)
        x_valid = pickle.load(inp)
        y_valid = pickle.load(inp)
        return word2id, id2word, id2tag


def predict_dict(sentence, predict_tag_array):
    # 将预测的标签转化为字典，用于GUI中显示
    predict_tag_dict = {}
    index = 0

    while index != len(sentence):
        if predict_tag_array[index] == 0:
            index += 1
            continue
        else:
            tag = predict_tag_array[index]
            temp_word = ''
            index1 = index
            while index1 != len(sentence):
                if tag != predict_tag_array[index1]:
                    index = index1
                    break
                else:
                    temp_word = temp_word + sentence[index1]
                    index1 += 1
                    if index1 == len(sentence):
                        index = index1
            predict_tag_dict[len(predict_tag_dict)] = {temp_word: tag}
    return predict_tag_dict


def test_predict_tag_dict(sentence):

    sentence_wordId = []
    for word in sentence:
        if word in word2id.index:
            sentence_wordId.append(word2id[word])
        else:
            sentence_wordId.append(word2id['unknow'])

    if len(sentence_wordId) < 60:
        for i in range(60-len(sentence_wordId)):
            sentence_wordId.append(0)
    else:
        print('句子长度超过60，请重新输入!')
        sys.exit(0)
    # 分词   不需要，模型用用字输入
    # seg_list = jieba.cut(sentence)  # 默认是精确模式
    # print(", ".join(seg_list))
    sentence_tensor = torch.from_numpy(np.array(sentence_wordId)).long()
    score, predict_tags = model(sentence_tensor)

    # 设置这句话对应的文字预测标识
    predict_tag_array = []
    for i in range(len(predict_tags)):
        if predict_tags[i] != 0:
            if id2tag[predict_tags[i]] == 'O':
                predict_tag_array.append(0)
            else:
                id2tag_list = id2tag[predict_tags[i]].split('_')
                if id2tag_list[1] == 'time':
                    predict_tag_array.append(1)
                elif id2tag_list[1] == 'location':
                    predict_tag_array.append(2)
                elif id2tag_list[1] == 'person':
                    predict_tag_array.append(3)
                elif id2tag_list[1] == 'org':
                    predict_tag_array.append(4)
                elif id2tag_list[1] == 'company':
                    predict_tag_array.append(5)
                else:
                    predict_tag_array.append(6)
        else:
            pass
    predict_tag_dict = predict_dict(sentence, predict_tag_array)
    return predict_tag_dict

class APP:
    def __init__(self, root):
        frame = tkinter.Frame(root, relief=tkinter.RAISED, borderwidth=2, width=1000, height=1000)

        frame.pack(side=tkinter.TOP, fill=tkinter.BOTH, ipadx=5, ipady=5, expand=1)

        self.label_title = tkinter.Label(root, text='短文本中文命名实体识别DEMO', bg='red', font=('Arial', 25))
        self.label_title.place(x=200, y=100, anchor=tkinter.W, width=600, height=60)  # 固定窗口位置

        self.label_record_voice = tkinter.Label(root, text='', bg='green', font=('Arial', 25))
        self.label_record_voice.place(x=50, y=300, anchor=tkinter.W, width=800, height=60)  # 固定窗口位置

        self.record_data = ''
        self.button_voice_record = tkinter.Button(frame, text="语音录入", background='red', font=('Arial', 12),
                                             command=self.button_record_voice)
        self.button_voice_record.place(x=900, y=300, anchor=tkinter.W, width=80, height=60)

        self.button_ner = tkinter.Button(frame, text="开始识别", background='blue', font=('Arial', 12),
                                         command=self.button_ner_fun)
        self.button_ner.place(x=450, y=400, anchor=tkinter.W, width=80, height=60)

    def button_record_voice(self):
        record_result = test_wav.voice_record()
        self.label_record_voice['text'] = record_result
        self.record_data = record_result

    def button_ner_fun(self):
        if self.record_data == '':
            print('没有录入语音')
            sys.exit(-1)
        record_word = self.record_data
        predict_tag_dict = test_predict_tag_dict(record_word)

        record_y = 500
        for i in range(len(predict_tag_dict)):

            content = predict_tag_dict[i]
            word = list(content.keys())[0]
            tag = list(content.values())[0]
            tag_content = ''
            if tag == 1:
                tag_content = 'NER:时间'
            elif tag == 2:
                tag_content = 'NER:地点'
            elif tag == 3:
                tag_content = 'NER:人名'
            elif tag == 4:
                tag_content = 'NER:组织名'
            elif tag == 5:
                tag_content = 'NER:公司名'
            else:
                tag_content = 'NER:产品名'
            output_content = word + '  ' + tag_content
            label = tkinter.Label(root, text=output_content, bg='green', font=('Arial', 25))
            label.place(x=50, y=record_y, anchor=tkinter.W, width=800, height=60)
            if i == 0:
                record_y = record_y + (i+1)*100
            else:
                record_y = record_y + 100

if __name__ == '__main__':

    word2id, id2word, id2tag = load_data()
    model = torch.load("C:\\Users\\Administrator\\PycharmProjects\\ChineseNER\\save_model\\model4.pkl")
    root = tkinter.Tk(className='中文NER交互界面')
    app =APP(root)
    root.mainloop()





