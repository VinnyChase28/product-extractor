This streamlit app allows you to turn unstructured data into structured data. 

1. define a schema for extraction using openai's function calling

2. Extract the text from the pdf and have openai api extract the data.

3. The result is json, in the format you specified in the schema.

Function calling is emerging as one of the most powerful ways to turn ubnstructured data into structured data.


pip install virtualenv (Optional)

virtualenv venv

source venv/bin/activate

pip install -r requirements.txt

export OPENAI_API_KEY=[YOUR_KEY_HERE]

streamlit run streamlit_app.py
