import os
import re
import openai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_cpt_codes(cpt_codes):
    keys = range(len(cpt_codes))
    for i in keys:
        raw = cpt_codes[i].strip()
        print(raw)
        print(extract_cpt(raw))

def extract_cpt(string):
    regex = "^[a-zA-Z0-9]{5}$"
    split_array = string.split(" ")
    keys = range(len(split_array))
    for i in keys:
        if (re.match(regex, split_array[i])):
            return split_array[i]

def is_cpt(string):
    regex = "^[a-zA-Z0-9]{5}$"
    if re.match(regex, string):
        return True
    else:
        return False

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
    find_cpt_prompt = f"List 3 CPT codes for the following medical procedure in format of cpt code1, cpt code 2, cpt code 3: {description}"
    find_cpt_response = chatgpt_request(find_cpt_prompt)
    cpt_codes = find_cpt_response.strip().split(',')
    # parse_cpt_codes(cpt_codes)
    keys = range(len(cpt_codes))
    results = []
    for i in keys:
      print(cpt_codes[i].strip())
      if not is_cpt(cpt_codes[i].strip()):
          return "result not found", 400

      result = {}
      result["code"] = cpt_codes[i].strip()
      cpt_desc_prompt = f"give me a description for this cpt code: {cpt_codes[i]}"
      cpt_desc_response = chatgpt_request(cpt_desc_prompt)
      result["description"] = cpt_desc_response.strip()

      results.append(result)

    return jsonify(results=results)

  return render_template("index.html")

if __name__ == "__main__":
   app.run(debug=False)
