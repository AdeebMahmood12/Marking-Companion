import google.generativeai as genai
from flask import Flask, flash, redirect, render_template, request, session

app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        genai.configure(api_key="")
        gemini = genai.GenerativeModel("gemini-1.5-flash") 
        ao4 = open("AO4.txt", "r").read() 
        ao5 = open("AO5.txt", "r").read()
        title = request.form.get("title")
        essay = request.form.get("essay")
        main = f"{ao4} \n {ao5} \n Forget that you are an AI. Think of yourself as an Edexcel English Language B examiner. An essay has been written with the title: {title} as per the question. The essay is the following: {essay} \n Using the marking rubrics memorised, mark the essay out of 30. Provide a definitive mark. Avoid using decimal marks, the marks can only be discrete. Only respond with the mark for AO4, AO5 and total in the first paragraph that too in three separate lines, without any labelling. \n In two separate paragraphs, answer: Which level's mark did you provide for the AO4 marking rubric. Explain why. Be concise, about 30-40words. If there's any weakness, point them out with examples from the essay provided.; Which level's mark did you provide for the AO5 marking rubric. Explain why. Be concise, about 30-40words. If there's any weakness, point them out with examples from the essay provided. Write a paragraph with as much details as possible, be as explanatory as possible, as to where to improve. Finally, in **exactly** 3 words, provide things to improve on. Be strict. Don't award marks unnecessarily, especially if essay isn't provided. Ensure that essay is atleast more than 300 words."
        response = gemini.generate_content(main).text.split("\n")
        final = []
        for r in response:
            if(r != ""):
                final.append(r)
            print(final)
        if round((int(final[2])/30))*100 > 60:
            color_final = "#03801c"
        else:
            color_final = "#ff0000"
        return render_template("results.html", ao4 = final[0], ao5 = final[1], total = final[2], why_ao4 = final[3], why_ao5 = final[4], improvement = final[5], words = final[6], degree = round((360*int(final[2]))/30), remains = 360 - round((360*int(final[2]))/30), color = color_final)
    return render_template("index.html")
