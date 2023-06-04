import openai, re, time, os
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

from DocumentTest import *


class EssayWriter:
    topic = ""
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    def __init__(self, topic):
        self.topic = topic
        self.document = Document()
    
    def generate(self, msg=[], n=10):
        print("generating:\n" + str(msg))
        try:
            completion = openai.ChatCompletion.create(model="gpt-3.5-turbo-0301", messages=msg,temperature = 0.2,max_tokens = 2048)
            response = completion.choices[0].message.content
        except Exception as e:
            print(e)
            if n > 0:
                print("retrying,n = %d..." % n)
                time.sleep(5)
                return self.generate(msg, n-1)
            else:
                print("Max retries exceeded.")
                return ""
        return response
            
            

    def generate_outline(self):
        
        msg = [
            {"role":"system","content":"你是一个用于写作的大师AI"},
            {"role":"user","content":str("列出一个“%s”的论文大纲，格式为：\n标题：\n摘要：\n关键字:（3到5个）\n引言:\n（正文采用阿拉伯数字分级标题，如:）\n1.\n1.1\n1.1.1\n总结:" % self.topic)}
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

        first_titles = re.findall(r'(?<!\d\.)((\d+)\.\s+(.*))\n?', response)
        third_titles = re.findall(r'(((\d+)\.(\d+)\.(\d+))\s+(.*))\n?', response)
        second_titles = re.findall(r'(?<!\d\.)(((\d+)\.(\d+))\s+(.*))(?!\.\d)', response)

        print("一级标题：" + str(first_titles))
        print("二级标题：" + str(second_titles))
        print("三级标题：" + str(third_titles))

        if len(third_titles) == 0:
            third_titles = second_titles
        else:
            #sort the third_titles and second_titles
            third_titles += second_titles
            third_titles.sort(key=lambda x: (x[1], x[2], x[3]))

        temp = ''
        for title in third_titles:
            if title[2] != temp:
                temp = title[2]
                docPlayer.add_para("\n" + first_titles[int(temp) - 1][0], size=14, isBold=True)
            msg.append({"role":"user","content":str("请根据大纲内容阐述%s部分，但不要涉及其他部分或阐述子部分" % title[0])})
            res = self.generate(msg)
            print(res)
            content += res + "\n\n"

            docPlayer.add_text("\n" + res.replace(title[0],''),size = 12,paragraph=docPlayer.add_para(title[0], size=12, isBold=True))
            msg = msg[:-1]

        summary = re.search(r'总结：(.*)',response).group(1)
        content += "结语:" + summary + "\n"

        docPlayer.add_text("\n" + summary,size = 12,paragraph=docPlayer.add_para("结语:", size=14, isBold=True))
        docPlayer.save(filepath)
        return content
        
if __name__ == "__main__":
    name = "张三"
    unit = "南方科技大学"

    topic = "随机选题"
    filepath = "document/{}.docx".format(topic.replace(" ", ""))
    docPlayer = DocumentTest()
    my_writer = EssayWriter(topic)
    outline = my_writer.generate_outline()
    print("\n\n\n" + outline)