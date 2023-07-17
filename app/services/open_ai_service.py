import re
import json
from urllib.parse import urlparse
import openai

# from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from app.schema.api_schema import AskBody, TokenUsage
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
                "role": "system",
                "content": system_content
            },
            {
                "role": "user",
                "content": user_content
            },
            {
                "role": "assistant",
                "content": assistant_content
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        return messages

    async def ask(self, ask_body: AskBody):
        prompt = await self.create_prompt(self, ask_body)

        # llm = OpenAI(model_name='text-davinci-003', temperature=1)
        # llm_out = llm(prompt[3]["Content"])
        # response = {
        #     "answer": llm_out,
        #     "source": ""
        # }

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=prompt,
            stream=False,
            temperature=0.00000001,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            max_tokens=2000,
            n=1,
        )

        return response

    def get_product_from_url(self, url):
        # check if url matches these product categories
        prore = re.compile(r"pro\.hukumonline\.com")
        klinikre = re.compile(r"hukumonline\.com/klinik")
        psre = re.compile(r"hukumonline\.com/stories")
        product = "Hukumonline"

        if prore.search(url):
            product = "Hukumonline Pro"
        elif klinikre.search(url):
            product = "Klinik Hukumonline"
        elif psre.search(url):
            product = "Premium Stories"

        return product

    async def ask_stream(self, ask_body: AskBody):
        # get user context
        # set span tracer ?

        # calculate token usage
        token_usage = TokenUsage()
        # set token usage to span

        prompt = await self.create_prompt(None, ask_body)

        for pro in prompt:
            token_usage.prompt_tokens += len(pro["content"])

        source_tag = False
        url_regex = re.compile(
            r'((http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/|\/|\/\/)?[A-z0-9_-]*?[:]?[A-z0-9_-]*?[@]?[A-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?)\n$')
        total_answer = ""
        answer_only = ""
        source_url_string = ""
        source_urls = []

        for chunk in openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=prompt,
            stream=True,
            temperature=0.00000001,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            max_tokens=2000,
            n=1,
        ):
            # content = chunk["choices"][0].get("delta", {}).get("content")
            # if content is not None:
            #     yield content
            finish = chunk["choices"][0].get("finish_reason") == "stop"
            if len(chunk["choices"]) == 0:
                continue
            delta = chunk["choices"][0].get("delta", {}).get("content")
            if (delta is None or len(delta) == 0) and not finish:
                continue

            if finish:
                if (delta is None or len(delta) == 0):
                    delta = ""
                delta += "\n"

            total_answer += delta.replace("\n", "\n")

            if not source_tag:
                if "SOURCES:\n" in total_answer:
                    answer_only = total_answer
                    source_tag = True
                    total_answer = ""
                    token_usage.completion_tokens += len(answer_only)
                else:
                    source_url_string += delta

                token_usage.completion_tokens += len(delta)

            answer = {
                "answer": "",
                "source": ""
            }
            if source_tag:
                if url_regex.search(total_answer):
                    urls = url_regex.findall(total_answer)[:1]
                    source_url = urls[0][0].strip("-").strip()
                    total_answer = url_regex.sub(
                        "", total_answer).strip("-").strip()
                    parsed_url = urlparse(source_url)
                    if not parsed_url.scheme:
                        source_url = "http://" + source_url
                        parsed_url = urlparse(source_url)
                    source_urls.append(source_url)
                    source = {"URL": source_url,
                              "Product": self.get_product_from_url(source_url)}

                    # try:
                    #     meta = get_metadata_from_source_url(ctx, source_url)
                    #     source["Title"] = meta.Title
                    #     source["Text"] = meta.Description
                    # except Exception as e:
                    #     print("%v failed to get metadata", e)

                    answer["source"] = source
                else:
                    continue
            else:
                answer["answer"] = delta

            # print("answer chunk: %v", answer)
            yield json.dumps({"data": answer})+'\n'

        print("total token", token_usage.get_all())
