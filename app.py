import os
import random
import openai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

def chatgpt_request(prompt):
   response = openai.Completion.create(
       engine="text-davinci-002",
       prompt=prompt,
       max_tokens=50,
       n=1,
       temperature=0.5,
   )

   response_json = response.choices
   if not response_json:
       raise Exception("Unexpected response format from the API")

   return response_json[0].text

@app.route("/", methods=["GET", "POST"])
def index():
   if request.method == "POST":
       description = request.form.get("description")
       prompt = f"List 3 CPT codes for the following medical procedure: {description}"
       response_text = chatgpt_request(prompt)
       cpt_codes = response_text.strip().split(',')
       cpt_code = random.choice(cpt_codes)
       return jsonify(cpt_code0=cpt_codes[0],cpt_code1=cpt_codes[1], cpt_code2=cpt_codes[2])

   return render_template("index.html")

if __name__ == "__main__":
   app.run(debug=True)