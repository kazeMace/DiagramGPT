from sanic import Sanic, HTTPMethod, Request
from sanic.response import text, html
from sanic_ext import Extend
import openai
import os
import re
openai.api_key = ""

os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""

index_html = "".join(open("./index.html", "r").readlines())
app = Sanic("diagram-gpt")
Extend(app)
@app.route("/", methods=[HTTPMethod.GET, HTTPMethod.POST])
def process(request: Request):
    if request.method == "GET":
        return html(index_html)
    elif request.method == "POST":
        query = request.json["query"]
        types = request.json["type"]
        print(query)
        mermaid_code = logic(types, query)
        print("================ mermaid code ==================")
        print(mermaid_code)
        return text(mermaid_code)

def logic(types, query):
    new_query = f"使用中文回答我接下来的问题。使用 markdown 画一个专业的{types}，内容为：“{query}”"
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": new_query}])
    html_text = completion.choices[0].message.content
    print("*******************************************")
    print(html_text)
    print("*******************************************")
    pattern = r"```mermaid\n([\w\s]+[\n]+[\s\S]+?)```"
    code_blocks = re.findall(pattern, html_text)
    mermaid_code = "".join(code_blocks)
    return mermaid_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
