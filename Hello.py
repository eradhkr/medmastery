# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from openai import OpenAI
import json
import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def simple_classify(client, question_to_nurse_string: str, nurse_response_string: str, prompt_string:str) -> str:

  #instruction to the model
  #"You are training instructor for Nurses and you are assessing the Nurse's response to questions asked to the nurse. 
  # I am going to give you the question asked to the Nurse and the Nurse's response for you to review. 
  # You need to assess the Nurses's response and rank the Nurses's response on a scale of 1 to 10, 
  # with 1 being most negative and 10 being most positive. 
  # Do not return any other ouput other than the score of 1 to 10, with 1 being most negative and 10 being most positive
  # Sentiment of Positive, Negative or Neutral"

  completion = client.completions.create(model='gpt-3.5-turbo-instruct',
                                         prompt=f"{prompt_string}: {question_to_nurse_string} {nurse_response_string}")
  response=completion.choices[0].text
  print(f"For, response is:\n----------{response}\n=============")
  #print(dict(completion).get('usage'))
  #print(completion.model_dump_json(indent=2))
  return response

def run():
    st.set_page_config(page_title="MedMastery", page_icon="🤪")
    st.markdown("A training websiste for doctors and nurses")
    st.write("""Using ChatGpt Sentiment Analysis""")

    password = st.text_input("Enter your OpenAI key: ")
    prompt = st.text_input("What is the sentiment of this statement?")
    question_to_nurse = st.text_area("Enter a question to the nurse: ")
    nurse_response = st.text_area("Enter the Nurse's response: ")

    if password:  
      client = OpenAI(api_key=password)
      response = simple_classify(client, question_to_nurse, nurse_response, prompt) 
  
      st.write(f"response is{response}")


if __name__ == "__main__":
  run()


