import random
import string
from opentelemetry import trace
import pytest

from app.services import *
from app.services.html_service import HTMLMeta
from app.repository import *
from app.schema.api_schema import AskBody
from app.schema.auth_schema import UserContext


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class TestSupabaseRepository:
    @pytest.fixture(autouse=True)
    def setup_before_test(self, monkeypatch):
        # setup env
        monkeypatch.setenv('SUPABASE_KEY', 'my_key')
        monkeypatch.setenv('SUPABASE_URL', 'https://sample.co')
        monkeypatch.setenv('SUPABASE_DB', 'my_db')

    @pytest.mark.asyncio
    async def test_match_documents(self, mocker):
        # mock
        params = {}
        mocker.patch('requests.post', return_value=MockResponse({}, 200))
        repo = SupabaseRepository()
        result = repo.match_documents(params)
        assert result == {}


class TestCreatePrompt:
    @pytest.fixture(autouse=True)
    def setup_before_test(self, monkeypatch):
        # setup env
        monkeypatch.setenv('OPENAI_API_KEY', 'open_ai_value')

    # Tests that create_prompt returns a list of messages with the correct format
    @pytest.mark.asyncio
    async def test_create_prompt_returns_messages(self, mocker):
        # mock
        langchain_embedding_mock = mocker.patch(
            'langchain.embeddings.OpenAIEmbeddings.embed_query')
        langchain_embedding_mock.return_value = [0.1, 0.2, 0.3]
        mock_supabase_repository = mocker.Mock()
        mock_supabase_repository.match_documents.return_value = [
            {
                'url': 'https://example.com',
                'content': 'Example content'
            }
        ]

        openai_service = OpenAiService(mock_supabase_repository)
        user_context: UserContext = {
            "email": "test@example.com",
            "name": "Test User",
            "span": None,
            "tracer": trace.get_tracer("test")
        }
        ask_body: AskBody = {
            "question": "what is this?",
            "lang": "en",
        }
        messages = await openai_service.create_prompt(user_context, ask_body)
        assert len(messages) == 4
        assert messages[0]['role'] == 'system'
        assert messages[1]['role'] == 'user'
        assert messages[2]['role'] == 'assistant'
        assert messages[3]['role'] == 'user'

    # Tests that create_prompt handles documents with no content
    @pytest.mark.asyncio
    async def test_create_prompt_handles_documents_with_no_content(self, mocker):
        # mock
        langchain_embedding_mock = mocker.patch(
            'langchain.embeddings.OpenAIEmbeddings.embed_query')
        langchain_embedding_mock.return_value = [0.1, 0.2, 0.3]
        mock_supabase_repository = mocker.Mock()
        mock_supabase_repository.match_documents.return_value = [
            {
                'url': 'https://example.com',
                'content': None
            }
        ]

        openai_service = OpenAiService(mock_supabase_repository)
        user_context: UserContext = {
            "email": "test@example.com",
            "name": "Test User",
            "span": None,
            "tracer": trace.get_tracer("test")
        }
        ask_body: AskBody = {
            "question": "what is this?",
            "lang": "en",
        }
        messages = await openai_service.create_prompt(user_context, ask_body)
        assert len(messages) == 4

    # Tests that create_prompt handles documents with same urls
    @pytest.mark.asyncio
    async def test_create_prompt_handles_documents_with_same_urls(self, mocker):
        # mock
        langchain_embedding_mock = mocker.patch(
            'langchain.embeddings.OpenAIEmbeddings.embed_query')
        langchain_embedding_mock.return_value = [0.1, 0.2, 0.3]
        mock_supabase_repository = mocker.Mock()
        mock_supabase_repository.match_documents.return_value = [
            {
                'url': 'https://example.com',
                'content': 'Example content'
            },
            {
                'url': 'https://example.com',
                'content': 'another content'
            }
        ]

        openai_service = OpenAiService(mock_supabase_repository)
        user_context: UserContext = {
            "email": "test@example.com",
            "name": "Test User",
            "span": None,
            "tracer": trace.get_tracer("test")
        }
        ask_body: AskBody = {
            "question": "what is this?",
            "lang": "en",
        }
        messages = await openai_service.create_prompt(user_context, ask_body)
        assert len(messages) == 4

    # Tests that create_prompt handles format documents with token more than max
    @pytest.mark.asyncio
    async def test_create_prompt_handles_format_documents_with_token_more_than_max(self, mocker):
        # mock
        langchain_embedding_mock = mocker.patch(
            'langchain.embeddings.OpenAIEmbeddings.embed_query')
        langchain_embedding_mock.return_value = [0.1, 0.2, 0.3]
        mock_supabase_repository = mocker.Mock()
        mock_supabase_repository.match_documents.return_value = [
            {
                'url': 'https://example.com',
                'content': ''.join(random.choices(string.ascii_uppercase + string.digits, k=3000))
            }
        ]

        openai_service = OpenAiService(mock_supabase_repository)
        user_context: UserContext = {
            "email": "test@example.com",
            "name": "Test User",
            "span": None,
            "tracer": trace.get_tracer("test")
        }
        ask_body: AskBody = {
            "question": "what is this?",
            "lang": "en",
        }
        messages = await openai_service.create_prompt(user_context, ask_body)
        assert len(messages) == 4

    # Tests that create_prompt handles documents with no URLs
    @pytest.mark.asyncio
    async def test_create_prompt_handles_documents_with_no_URLs(self, mocker):
        # mock
        langchain_embedding_mock = mocker.patch(
            'langchain.embeddings.OpenAIEmbeddings.embed_query')
        langchain_embedding_mock.return_value = [0.1, 0.2, 0.3]
        mock_supabase_repository = mocker.Mock()
        mock_supabase_repository.match_documents.return_value = [
            {
                'url': '',
                'content': 'Example content'
            }
        ]

        openai_service = OpenAiService(mock_supabase_repository)
        user_context: UserContext = {
            "email": "test@example.com",
            "name": "Test User",
            "span": None,
            "tracer": trace.get_tracer("test")
        }
        ask_body: AskBody = {
            "question": "what is this?",
            "lang": "en",
        }
        messages = await openai_service.create_prompt(user_context, ask_body)
        assert len(messages) == 4


class TestOpenAiService:
    @pytest.fixture(autouse=True)
    def setup_before_test(self, monkeypatch):
        # setup env
        monkeypatch.setenv('OPENAI_API_KEY', 'open_ai_value')

    # Tests that ask returns a dictionary with the answer and source
    @pytest.mark.asyncio
    async def test_ask_returns_answer_and_source(self, mocker):
        # mock
        langchain_embedding_mock = mocker.patch(
            'langchain.embeddings.OpenAIEmbeddings.embed_query')
        langchain_embedding_mock.return_value = [0.1, 0.2, 0.3]
        mock_supabase_repository = mocker.Mock()
        mock_supabase_repository.match_documents.return_value = [
            {
                'url': 'https://example.com',
                'content': 'Example content'
            }
        ]
        openai_mock = mocker.patch('openai.ChatCompletion.create')
        openai_mock.return_value = {
            'usage': {
                'prompt_tokens': 1,
                'completion_tokens': 1,
                'total_tokens': 2,
            },
            'choices': [
                {
                    'message': {
                        'content': 'This is the answer.\nSOURCES:\n-https://pro.hukumonline.com/a/abcd'
                    }
                }
            ]
        }

        openai_service = OpenAiService(mock_supabase_repository)
        user_context: UserContext = {
            "email": "test@example.com",
            "name": "Test User",
            "span": None,
            "tracer": trace.get_tracer("test")
        }
        ask_body: AskBody = {
            "question": "apa saja yang diatur uu cipta kerja?",
            "lang": "id",
        }
        response = await openai_service.ask(user_context, ask_body)
        assert 'answer' in response
        assert 'source' in response

    # Tests that ask returns a dictionary with source url is empty
    @pytest.mark.asyncio
    async def test_ask_with_source_url_empty(self, mocker):
        # mock
        langchain_embedding_mock = mocker.patch(
            'langchain.embeddings.OpenAIEmbeddings.embed_query')
        langchain_embedding_mock.return_value = [0.1, 0.2, 0.3]
        mock_supabase_repository = mocker.Mock()
        mock_supabase_repository.match_documents.return_value = [
            {
                'url': 'https://example.com',
                'content': 'Example content'
            }
        ]
        openai_mock = mocker.patch('openai.ChatCompletion.create')
        openai_mock.return_value = {
            'usage': {
                'prompt_tokens': 1,
                'completion_tokens': 1,
                'total_tokens': 2,
            },
            'choices': [
                {
                    'message': {
                        'content': 'This is the answer.\nSOURCES:\n-'
                    }
                }
            ]
        }

        openai_service = OpenAiService(mock_supabase_repository)
        user_context: UserContext = {
            "email": "test@example.com",
            "name": "Test User",
            "span": None,
            "tracer": trace.get_tracer("test")
        }
        ask_body: AskBody = {
            "question": "apa saja yang diatur uu cipta kerja?",
            "lang": "id",
        }
        response = await openai_service.ask(user_context, ask_body)
        assert 'answer' in response
        assert 'source' in response

    # Tests that ask_stream yields a JSON string with the answer and source
    @pytest.mark.asyncio
    async def test_ask_stream_yields_JSON_string(self, mocker):
        # mock
        langchain_embedding_mock = mocker.patch(
            'langchain.embeddings.OpenAIEmbeddings.embed_query')
        langchain_embedding_mock.return_value = [0.1, 0.2, 0.3]
        mock_supabase_repository = mocker.Mock()
        mock_supabase_repository.match_documents.return_value = [
            {
                'url': 'https://example.com',
                'content': 'Example content'
            }
        ]
        openai_mock = mocker.patch('openai.ChatCompletion.create')
        openai_mock.return_value = [{
            'choices': [
                {
                    'finish_reason': '',
                    'delta': {
                        'content': 'This is the answer'
                    }
                }
            ]
        },
            {
            'choices': [
                {
                    'finish_reason': '',
                    'delta': {
                        'content': '\nSOURCES:\n'
                    }
                }
            ]
        },
        {
            'choices': [
                {
                    'finish_reason': 'stop',
                    'delta': {
                        'content': ''
                    }
                }
            ]
        }]

        openai_service = OpenAiService(mock_supabase_repository)
        user_context: UserContext = {
            "email": "test@example.com",
            "name": "Test User",
            "span": None,
            "tracer": trace.get_tracer("test")
        }
        ask_body: AskBody = {
            "question": "apa saja yang diatur uu cipta kerja?",
            "lang": "id",
        }
        async for message in openai_service.ask_stream(user_context, ask_body):
            assert isinstance(message, str)
            assert message.startswith('{"data": {"answer": "')
            assert message.endswith('"}}\n\n')

    # Tests that ask_stream yields a JSON string with sources
    @pytest.mark.asyncio
    async def test_ask_stream_yields_JSON_strin_with_sources(self, mocker):
        # mock
        langchain_embedding_mock = mocker.patch(
            'langchain.embeddings.OpenAIEmbeddings.embed_query')
        langchain_embedding_mock.return_value = [0.1, 0.2, 0.3]
        mock_supabase_repository = mocker.Mock()
        mock_supabase_repository.match_documents.return_value = [
            {
                'url': 'https://example.com',
                'content': 'Example content'
            }
        ]
        openai_mock = mocker.patch('openai.ChatCompletion.create')
        openai_mock.return_value = [
        {
            'choices': []
        },
        {
            'choices': [
                {
                    'finish_reason': '',
                    'delta': {
                        'content': None
                    }
                }
            ]
        },
        {
            'choices': [
                {
                    'finish_reason': '',
                    'delta': {
                        'content': 'This is the answer'
                    }
                }
            ]
        },
        {
            'choices': [
                {
                    'finish_reason': '',
                    'delta': {
                        'content': '\nSOURCES:\n'
                    }
                }
            ]
        },
        {
            'choices': [
                {
                    'finish_reason': '',
                    'delta': {
                        'content': '-pro.hukumonline.com/a/abcd\n'
                    }
                }
            ]
        },
        {
            'choices': [
                {
                    'finish_reason': 'stop',
                    'delta': {
                        'content': '-https://pro.hukumonline.com/a/abcd'
                    }
                }
            ]
        }]
        get_meta_mock = mocker.patch('app.services.open_ai_service.get_metadata_from_source_url')
        hm = HTMLMeta()
        hm.Title = "Title"
        hm.Description = "Description"
        get_meta_mock.return_value = hm
        get_meta_mock.return_value = hm

        openai_service = OpenAiService(mock_supabase_repository)
        user_context: UserContext = {
            "email": "test@example.com",
            "name": "Test User",
            "span": None,
            "tracer": trace.get_tracer("test")
        }
        ask_body: AskBody = {
            "question": "apa saja yang diatur uu cipta kerja?",
            "lang": "id",
        }
        async for message in openai_service.ask_stream(user_context, ask_body):
            assert isinstance(message, str)

    # Tests that ask_stream yields a JSON string with error get meetadata
    @pytest.mark.asyncio
    async def test_ask_stream_yields_JSON_strin_with_error_getmetadata(self, mocker):
        # mock
        langchain_embedding_mock = mocker.patch(
            'langchain.embeddings.OpenAIEmbeddings.embed_query')
        langchain_embedding_mock.return_value = [0.1, 0.2, 0.3]
        mock_supabase_repository = mocker.Mock()
        mock_supabase_repository.match_documents.return_value = [
            {
                'url': 'https://example.com',
                'content': 'Example content'
            }
        ]
        openai_mock = mocker.patch('openai.ChatCompletion.create')
        openai_mock.return_value = [
        {
            'choices': []
        },
        {
            'choices': [
                {
                    'finish_reason': '',
                    'delta': {
                        'content': None
                    }
                }
            ]
        },
        {
            'choices': [
                {
                    'finish_reason': '',
                    'delta': {
                        'content': 'This is the answer'
                    }
                }
            ]
        },
        {
            'choices': [
                {
                    'finish_reason': '',
                    'delta': {
                        'content': '\nSOURCES:\n'
                    }
                }
            ]
        },
        {
            'choices': [
                {
                    'finish_reason': '',
                    'delta': {
                        'content': '-pro.hukumonline.com/a/abcd\n'
                    }
                }
            ]
        },
        {
            'choices': [
                {
                    'finish_reason': 'stop',
                    'delta': {
                        'content': '-https://pro.hukumonline.com/a/abcd'
                    }
                }
            ]
        }]
        get_meta_mock = mocker.patch('app.services.open_ai_service.get_metadata_from_source_url', side_effect=Exception("Error"))
        get_meta_mock = mocker.patch('app.services.open_ai_service.get_metadata_from_source_url', side_effect=Exception("Error"))

        openai_service = OpenAiService(mock_supabase_repository)
        user_context: UserContext = {
            "email": "test@example.com",
            "name": "Test User",
            "span": None,
            "tracer": trace.get_tracer("test")
        }
        ask_body: AskBody = {
            "question": "apa saja yang diatur uu cipta kerja?",
            "lang": "id",
        }
        async for message in openai_service.ask_stream(user_context, ask_body):
            assert isinstance(message, str)
