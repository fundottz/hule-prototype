from langchain.chat_models import ChatOpenAI
from personal_details import PersonalDetails
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain.chains import create_tagging_chain_pydantic
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, api_key=OPENAI_API_KEY)

# Check if fields are empty
def check_what_is_empty(user_peronal_details):
    ask_for = []
    for field, value in user_peronal_details.dict().items():
        if value in [None, "", 0]: 
            print(f"Field '{field}' is empty.")
            ask_for.append(f'{field}')
    return ask_for

def add_non_empty_details(current_details: PersonalDetails, new_details: PersonalDetails):
    non_empty_details = {k: v for k, v in new_details.dict().items() if v not in [None, "", 0]}
    updated_details = current_details.copy(update=non_empty_details)
    return updated_details

def ask_for_info(ask_for = ['fullname', 'gender', 'age', 'city', 'global_coverage_need', 'visa_coverage_need']):
    # prompt template 1
    first_prompt = ChatPromptTemplate.from_template(
        "Bellow are some things to ask the user for in a coversation way. You should only ask one question at a time even if you don't get all the info \
        don't ask as a list! Don't greet the user! Don't say Hi. Explain you need to get some info. If the ask_for list is empty then thank them and ask how you can help them \n\n \
        ### ask_for list: {ask_for}"
    )

    # info_gathering_chain
    info_gathering_chain = LLMChain(llm=llm, prompt=first_prompt)
    ai_chat = info_gathering_chain.run(ask_for=ask_for)
    return ai_chat

def filter_response(text_input, user_details):
    tagging_chain = create_tagging_chain_pydantic(PersonalDetails, llm)
    res = tagging_chain.run(text_input)
    # add filtered info to the
    user_details = add_non_empty_details(user_details,res)
    ask_for = check_what_is_empty(user_details)
    return user_details, ask_for
