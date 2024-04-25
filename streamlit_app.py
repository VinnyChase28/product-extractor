import streamlit as st
from langchain_community.llms import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List, Optional

openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password', key='sidebar_api_key')

# Define the schema for extraction
class ProductSpecs(BaseModel):
    """Product specifications."""
    models: Optional[List[str]] = Field(default=None, description="Available models")
    mounting_options: Optional[List[str]] = Field(default=None, description="Mounting options")
    voltage_options: Optional[List[str]] = Field(default=None, description="Voltage options")
    casing_finish: Optional[str] = Field(default=None, description="Casing/finish details")
    gas_control_options: Optional[List[str]] = Field(default=None, description="Gas control options")
    electrical_control_options: Optional[List[str]] = Field(default=None, description="Electrical control options")
    intake_options: Optional[List[str]] = Field(default=None, description="Intake options")
    discharge_options: Optional[List[str]] = Field(default=None, description="Discharge options")
    other_options: Optional[List[str]] = Field(default=None, description="Other available options/accessories")

class DataExtractor:
    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(model="gpt-4-turbo", temperature=0, openai_api_key=api_key)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert product specification extraction algorithm. Only extract relevant specifications from the text. If a specification is not mentioned, return null for its value."),
            ("human", "{text}"),
        ])
        self.runnable = self.prompt | self.llm.with_structured_output(schema=ProductSpecs)

    def extract_from_text(self, text: str):
        result = self.runnable.invoke({"text": text})
        return result

class DataProcessor:
    def __init__(self, extractor: DataExtractor):
        self.extractor = extractor

    def process_data(self, text):
        extracted_data = self.extractor.extract_from_text(text)
        return extracted_data

class OpenAIInterface:
    def __init__(self, api_key):
        self.llm = OpenAI(temperature=0, openai_api_key=api_key)

    def generate_response(self, input_text):
        return self.llm(input_text)

class StreamlitInterface:
    def __init__(self, data_processor: DataProcessor, ai_interface: OpenAIInterface):
        self.data_processor = data_processor
        self.ai_interface = ai_interface

    def run(self):
        st.title('🦜🔗 Product Specification Extraction App')
        with st.form('my_form'):
            text_input = st.text_area("Enter product description text")
            submitted = st.form_submit_button('Submit')

            if submitted:
                if not openai_api_key.startswith('sk-'):
                    st.warning('Please enter your OpenAI API key!', icon='⚠️')
                else:
                    if text_input:
                        processed_data = self.data_processor.process_data(text_input)
                        
                        # Display the structured object
                        st.subheader("Extracted Specifications")
                        st.json(processed_data.dict())
                        
                        # Generate response using the AI interface
                        response = self.ai_interface.generate_response(str(processed_data))
                        st.subheader("AI Response")
                        st.write(response)
                    else:
                        st.warning('Please provide product description text.')

if __name__ == "__main__":
    extractor = DataExtractor(openai_api_key)
    processor = DataProcessor(extractor)
    ai_interface = OpenAIInterface(openai_api_key)
    streamlit_interface = StreamlitInterface(processor, ai_interface)
    streamlit_interface.run()
