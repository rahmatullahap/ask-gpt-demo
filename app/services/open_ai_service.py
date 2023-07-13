from langchain.llms import OpenAI
from app.schema.ask_schema import AskBody


class OpenAiService():
    def __init__(self):
        super().__init__()

    def chat_completion(self, ask_body: AskBody):
        prompt = ask_body.message
        llm = OpenAI(model_name='text-davinci-003', temperature=1)
        template_prompt = '''
        Pertanyaan:
        {question}
        """
        '''.strip() + '\n'
        llm_out = llm(template_prompt.format(question=prompt))
        response = {
            "message": llm_out,
            "success": True
        }
        return response
