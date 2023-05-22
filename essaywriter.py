import openai
import re
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

memory = []

topic = "疫情期间的生活"


topic = "疫情期间的生活"
msg = [
    {"role":"system","content":"你是一个用于写作的大师AI"},
    {"role":"user","content":str("列出一个“%s”的论文大纲，格式为：\n标题：\n摘要：\n关键字:（3到5个）\n引言:\n（正文部分）\n1.\n1.1\n1.1.1\n总结:" % topic)}
]        
completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=msg,temperature = 0.3,max_tokens = 2048)
response = completion.choices[0].message.content
print(response)
msg.append({"role":"assistant","content":response})

title = re.search(r'标题：(.*)\n',response).group(1)
abstract = re.search(r'摘要：(.*)\n',response).group(1)
keywords = re.search(r'关键字：(.*)\n',response).group(1)
introduction = re.search(r'引言：(.*)\n',response).group(1)

content = ""
content += title + "\n"
content += abstract + "\n"
content += keywords + "\n"
content += introduction + "\n"

titles = re.findall(r'(((\d+)\.(\d+)\.(\d+))\s+(.*))\n?', response)

for title in titles:
    msg.append({"role":"user","content":str("请详细展开%s部分" % title[0])})
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=msg,temperature = 0.3,max_tokens = 2048)
    res = completion.choices[0].message.content
    print(res)    
    content += response + "\n"
    msg = msg[:-1]

    

summary = re.search(r'总结：(.*)\n',response).group(1)
content += summary + "\n"

print(content)



    