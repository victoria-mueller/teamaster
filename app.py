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
    find_cpt_prompt = f"List 3 CPT codes for the following medical procedure: {description}"
    find_cpt_response = chatgpt_request(find_cpt_prompt)
    cpt_codes = find_cpt_response.strip().split(',')
    keys = range(len(cpt_codes))
    results = []
    for i in keys:
      print(cpt_codes[i])
      result = {}
      result["code"] = cpt_codes[i]
      cpt_desc_prompt = f"give me a description for this cpt code: {cpt_codes[i]}"
      cpt_desc_response = chatgpt_request(cpt_desc_prompt)
      result["description"] = cpt_desc_response.strip()

      cpt_desc_prompt = f"what is claim submission limitation for cpt code: {cpt_codes[i]}"
      cpt_limitation_response= chatgpt_request(cpt_desc_prompt)
      result["limitation"] = cpt_limitation_response.strip()

      results.append(result)

    return jsonify(results=results)

  return render_template("index.html")

if __name__ == "__main__":
   app.run(debug=True)
