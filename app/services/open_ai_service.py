from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from app.schema.api_schema import AskBody
from app.schema.user_schema import UserContext
from app.repository.supabase_repository import SupabaseRepository

# MAX_GPT_TOKENS is maximum GPT-3 token allowed in context
MAX_GPT_TOKENS = 1500


class OpenAiService():
    """Open AI Service"""

    def __init__(self, supabase_repository: SupabaseRepository):
        self.supabase_repository = supabase_repository
        super().__init__()

    async def match_document(self, ctx: UserContext, query_embedding: [float], similarity_threshold: float, match_count: int):
        params = {
            "query_embedding":      query_embedding,
            "similarity_threshold": similarity_threshold,
            "match_count":          match_count,
        }
        data = self.supabase_repository.match_documents(
            "match_test_documents", params)
        return data

    def format_documents(self, objects):
        unique_urls = {}
        filtered_objects = []
        context_text = ''

        for doc in objects:
            url = doc['url']
            if url not in unique_urls:
                unique_urls[url] = True

                # set limit token
                token_count = len(doc["url"])
                if token_count <= MAX_GPT_TOKENS:
                    context_text += doc["content"].strip() + \
                        "\nSOURCE: " + doc["url"] + "\n---\n"
                    filtered_objects.append(doc)

        return [filtered_objects, context_text]

    async def create_prompt(self, ctx: UserContext, question: AskBody):
        embedding_req = {
            "model": "text-embedding-ada-002",
            "input": question["question"],
        }

        embeddings_model = OpenAIEmbeddings(model=embedding_req.get("model"))
        question_vect = embeddings_model.embed_query(
            embedding_req.get("input"))

        raw_docs = await self.match_document(ctx, question_vect, 0.1, 10)

        [_, context_text] = self.format_documents(raw_docs)

        language = "Bahasa Indonesia"
        if question["lang"] == "en":
            language = "English"

        system_content = f"You are a smart legal assistant. When given CONTEXT you answer questions using only that information. If the answer is not in the CONTEXT, answer the question with your own knowledge. You always format your output in markdown, you always respond in {language}. If the CONTEXT includes source URLs include them under a SOURCES heading at the end of your response. Always include all of the relevant source urls from the CONTEXT, but never list a URL more than once (ignore trailing forward slashes when comparing for uniqueness). Never include URLs that are not in the CONTEXT sections. Never make up URLs"
        user_content = """CONTEXT:
Next.js is a React framework for creating production-ready web applications. It provides a variety of methods for fetching data, a built-in router, and a Next.js Compiler for transforming and minifying JavaScript code. It also includes a built-in Image Component and Automatic Image Optimization for resizing, optimizing, and serving images in modern formats.
SOURCE: nextjs.org/docs/faq

QUESTION: 
what is nextjs?"""

        assistant_content = """Next.js is a framework for building production-ready web applications using React. It offers various data fetching options, comes equipped with an integrated router, and features a Next.js compiler for transforming and minifying JavaScript. Additionally, it has an inbuilt Image Component and Automatic Image Optimization that helps resize, optimize, and deliver images in modern formats.

SOURCES:
nextjs.org/docs/faq

"""

        user_message = f"""CONTEXT:
            {context_text}

            USER QUESTION: 
            {question}
        """

        messages = [
            {
                "Role": "system",
                "Content": system_content
            },
            {
                "Role": "user",
                "Content": user_content
            },
            {
                "Role": "assistant",
                "Content": assistant_content
            },
            {
                "Role": "user",
                "Content": user_message
            }
        ]

        return messages

    async def ask(self, ask_body: AskBody):
        prompt = await self.create_prompt(self, ask_body)

        llm = OpenAI(model_name='text-davinci-003', temperature=1)
        llm_out = llm(prompt[3]["Content"])
        response = {
            "answer": llm_out,
            "source": ""
        }

        return response

    async def ask_stream(self, ask_body: AskBody):
        # get user context
        # TODO set span tracer ?

        # calculate token usage
        tokenUsage = {
            "PromptTokens":     0,
            "CompletionTokens": 0,
            "TotalTokens":      0,
        }
        tokenUsage["TotalTokens"] = tokenUsage.get("CompletionTokens") + tokenUsage.get("PromptTokens")
        # set token usage to span

        message = await self.create_prompt(None, ask_body)

        llm = OpenAI(model_name='text-davinci-003', temperature=1)
        llm_out = llm(message[3]["Content"])
        response = {
            "answer": llm_out,
            "source": ""
        }
