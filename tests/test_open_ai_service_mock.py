import pytest
from opentelemetry import trace

from app.services import *
from app.schema.api_schema import AskBody
from app.schema.auth_schema import UserContext

class TestOpenAiService:
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
                        'content': 'This is the answer.\nSOURCES:'
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
            "question": "what is this?",
            "lang": "en",
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
                    'finish_reason': 'stop',
                    'delta': {
                        'content': '\nSOURCES:'
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
            "question": "what is this?",
            "lang": "en",
        }
        async for message in openai_service.ask_stream(user_context, ask_body):
            assert isinstance(message, str)
            assert message.startswith('{"data": {"answer": "')
            assert message.endswith('"}}\n\n')

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
