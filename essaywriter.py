import openai, re, time, os
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

from DocumentTest import *


class EssayWriter:
    topic = ""
    openai.api_key = os.environ["OPENAI_API_KEY"]
    def __init__(self, topic):
        self.topic = topic
        self.document = Document()
    
    def generate(self, msg=[], n=10):
        print("generating:\n" + str(msg))
        try:
            completion = openai.ChatCompletion.create(model="gpt-3.5-turbo-0301", messages=msg,temperature = 0.3,max_tokens = 2048)
            response = completion.choices[0].message.content
        except Exception as e:
            print(e)
            if n > 0:
                print("retrying,n = %d..." % n)
                time.sleep(1)
                return self.generate(msg, n-1)
            else:
                print("Max retries exceeded.")
                return ""
        return response
            
            

    def generate_outline(self):
        
        msg = [
            {"role":"system","content":"你是一个用于写作的大师AI"},
            {"role":"user","content":str("列出一个“%s”的论文大纲，格式为：\n标题：\n摘要：\n关键字:（3到5个）\n引言:\n（正文部分采用分级标题，如:）\n1.\n1.1\n1.1.1\n总结:" % self.topic)}
        ]
        response = self.generate(msg)
        print(response)
        msg.append({"role":"assistant","content":response})

        title = re.search(r'标题：(.*)\n',response).group(1)
        abstract = re.search(r'摘要：(.*)\n',response).group(1)
        keywords = re.search(r'关键字：(.*)\n',response).group(1)
        introduction = re.search(r'引言：(.*)\n',response).group(1)

        print("大纲：" + response)





        content = "标题：" + title + "\n" + "摘要：" + abstract + "\n" + "关键词：" + keywords + "\n" + "引言：" + introduction + "\n"
        print(content)

        docPlayer.add_para('\n\n\n' + title, size=16, font="黑体", isBold=True, isCenter=True)
        docPlayer.add_para("\n" + name, size=14, isCenter=True)
        docPlayer.add_para(f"({unit})", size=12, isCenter=True)
        docPlayer.add_text(abstract, size=10.5, font="仿宋",paragraph=docPlayer.add_para("\t摘要：", size=10.5, font="仿宋", isBold=True))
        docPlayer.add_text(keywords, size=10.5, font="仿宋",paragraph=docPlayer.add_para("\t关键词：", size=10.5, font="仿宋", isBold=True))
        docPlayer.add_para(introduction, size=12)

        titles = re.findall(r'(((\d+)\.(\d+)\.(\d+))\s+(.*))\n?', response)
        main_titles = re.findall(r'(((\d+)\.(\d+))\s+(.*))\n?', response)


        print(titles)
        print(main_titles)
        for i in main_titles:
            if i[4] in [x[5] for x in titles] or i[4] in [x[4] for x in titles]:
                print ("remove" + str(i))
                main_titles.remove(i)
        if len(titles) == 0:
            titles = main_titles
        else:
            #sort the titles and main_titles
            titles += main_titles
            titles.sort(key=lambda x: (x[1], x[2], x[3]))

        for title in titles:
            msg.append({"role":"user","content":str("请根据大纲内容展开%s部分，不要过多涉及其他部分或子部分" % title[0])})
            res = self.generate(msg)
            res_list = res.split('\n')
            print(res)
            content += res + "\n\n"

            docPlayer.add_text("\n" + res_list[1:],size = 12,paragraph=docPlayer.add_para(res_list[0], size=14, isBold=True))
            msg = msg[:-1]

        summary = re.search(r'总结：(.*)',response).group(1)
        content += "结语:" + summary + "\n"

        docPlayer.add_text("\n" + summary,size = 12,paragraph=docPlayer.add_para("结语:", size=14, isBold=True))
        docPlayer.save(filepath)
        return content
        
if __name__ == "__main__":
    name = "张三"
    unit = "南方科技大学"

    topic = "习近平是境外势力搞乱中国的证据"
    filepath = "data/{}.docx".format(topic.replace(" ", ""))
    docPlayer = DocumentTest()
    my_writer = EssayWriter(topic)
    outline = my_writer.generate_outline()
    print("\n\n\n" + outline)