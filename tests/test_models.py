"""Tests for database models."""

import pytest


class TestBaseModel:
    """Tests for the BaseModel mixin methods."""

    def test_update_does_not_change_id(self, app):
        """update() must never mutate the primary key."""
        from app.web.db.models import User

        user = User.create(email="nopk@example.com", password="pw")
        original_id = user.id
        user.update(id=999, email="changed@example.com")
        assert user.id == original_id

    def test_update_changes_non_pk_attribute(self, app):
        """update() should update non-PK attributes normally."""
        from app.web.db.models import User

        user = User.create(email="before@example.com", password="pw")
        user.update(email="after@example.com")
        assert user.email == "after@example.com"


class TestUserModel:
    """Tests for the User model."""

    def test_create_user(self, app):
        """Test creating a user."""
        from app.web.db.models import User

        user = User.create(email="test@example.com", password="hashed-password")
        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.password == "hashed-password"

    def test_user_as_dict(self, app):
        """Test User.as_dict excludes password."""
        from app.web.db.models import User

        user = User.create(email="test@example.com", password="secret")
        result = user.as_dict()
        assert result["email"] == "test@example.com"
        assert "password" not in result

    def test_find_user_by_email(self, app):
        """Test finding a user by email."""
        from app.web.db.models import User

        User.create(email="find@example.com", password="pw")
        found = User.find_by(email="find@example.com")
        assert found.email == "find@example.com"


class TestPdfModel:
    """Tests for the Pdf model."""

    def test_create_pdf(self, app):
        """Test creating a PDF linked to a user."""
        from app.web.db.models import User, Pdf

        user = User.create(email="pdf@example.com", password="pw")
        pdf = Pdf.create(name="test.pdf", user_id=user.id)
        assert pdf.id is not None
        assert pdf.name == "test.pdf"
        assert pdf.user_id == user.id

    def test_pdf_as_dict(self, app):
        """Test Pdf.as_dict returns expected fields."""
        from app.web.db.models import User, Pdf

        user = User.create(email="pdf2@example.com", password="pw")
        pdf = Pdf.create(name="doc.pdf", user_id=user.id)
        result = pdf.as_dict()
        assert result["name"] == "doc.pdf"
        assert result["user_id"] == user.id


class TestConversationModel:
    """Tests for the Conversation model."""

    def test_create_conversation(self, app):
        """Test creating a conversation linked to user and PDF."""
        from app.web.db.models import User, Pdf, Conversation

        user = User.create(email="conv@example.com", password="pw")
        pdf = Pdf.create(name="conv.pdf", user_id=user.id)
        conv = Conversation.create(pdf_id=pdf.id, user_id=user.id)
        assert conv.id is not None
        assert conv.pdf_id == pdf.id
        assert conv.user_id == user.id

    def test_conversation_as_dict(self, app):
        """Test Conversation.as_dict returns expected fields."""
        from app.web.db.models import User, Pdf, Conversation

        user = User.create(email="conv2@example.com", password="pw")
        pdf = Pdf.create(name="conv2.pdf", user_id=user.id)
        conv = Conversation.create(pdf_id=pdf.id, user_id=user.id)
        result = conv.as_dict()
        assert "id" in result
        assert "pdf_id" in result
        assert "messages" in result


class TestMessageModel:
    """Tests for the Message model."""

    def test_create_message(self, app):
        """Test creating a message in a conversation."""
        from app.web.db.models import User, Pdf, Conversation, Message

        user = User.create(email="msg@example.com", password="pw")
        pdf = Pdf.create(name="msg.pdf", user_id=user.id)
        conv = Conversation.create(pdf_id=pdf.id, user_id=user.id)
        msg = Message.create(
            role="human", content="Hello", conversation_id=conv.id
        )
        assert msg.id is not None
        assert msg.role == "human"
        assert msg.content == "Hello"

    def test_message_as_dict(self, app):
        """Test Message.as_dict returns expected fields."""
        from app.web.db.models import User, Pdf, Conversation, Message

        user = User.create(email="msg2@example.com", password="pw")
        pdf = Pdf.create(name="msg2.pdf", user_id=user.id)
        conv = Conversation.create(pdf_id=pdf.id, user_id=user.id)
        msg = Message.create(
            role="ai", content="Hi there", conversation_id=conv.id
        )
        result = msg.as_dict()
        assert result == {"id": msg.id, "role": "ai", "content": "Hi there"}

    def test_message_as_lc_message_human(self, app):
        """Test converting a human message to a LangChain message."""
        from langchain.schema.messages import HumanMessage
        from app.web.db.models import User, Pdf, Conversation, Message

        user = User.create(email="lc1@example.com", password="pw")
        pdf = Pdf.create(name="lc1.pdf", user_id=user.id)
        conv = Conversation.create(pdf_id=pdf.id, user_id=user.id)
        msg = Message.create(
            role="human", content="test", conversation_id=conv.id
        )
        lc_msg = msg.as_lc_message()
        assert isinstance(lc_msg, HumanMessage)
        assert lc_msg.content == "test"

    def test_message_as_lc_message_ai(self, app):
        """Test converting an AI message to a LangChain message."""
        from langchain.schema.messages import AIMessage
        from app.web.db.models import User, Pdf, Conversation, Message

        user = User.create(email="lc2@example.com", password="pw")
        pdf = Pdf.create(name="lc2.pdf", user_id=user.id)
        conv = Conversation.create(pdf_id=pdf.id, user_id=user.id)
        msg = Message.create(
            role="ai", content="response", conversation_id=conv.id
        )
        lc_msg = msg.as_lc_message()
        assert isinstance(lc_msg, AIMessage)
        assert lc_msg.content == "response"

    def test_message_as_lc_message_system(self, app):
        """Test converting a system message to a LangChain message."""
        from langchain.schema.messages import SystemMessage
        from app.web.db.models import User, Pdf, Conversation, Message

        user = User.create(email="lc3@example.com", password="pw")
        pdf = Pdf.create(name="lc3.pdf", user_id=user.id)
        conv = Conversation.create(pdf_id=pdf.id, user_id=user.id)
        msg = Message.create(
            role="system", content="You are a bot", conversation_id=conv.id
        )
        lc_msg = msg.as_lc_message()
        assert isinstance(lc_msg, SystemMessage)
        assert lc_msg.content == "You are a bot"

    def test_message_as_lc_message_unknown_role(self, app):
        """Test that unknown roles raise an exception."""
        from app.web.db.models import User, Pdf, Conversation, Message

        user = User.create(email="lc4@example.com", password="pw")
        pdf = Pdf.create(name="lc4.pdf", user_id=user.id)
        conv = Conversation.create(pdf_id=pdf.id, user_id=user.id)
        msg = Message.create(
            role="unknown", content="oops", conversation_id=conv.id
        )
        with pytest.raises(Exception, match="Unknown message role"):
            msg.as_lc_message()
