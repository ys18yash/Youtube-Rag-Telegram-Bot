from typing import Dict, Optional


class UserSession:
    def __init__(self):
        self.state: str = "WAITING_FOR_LINK"
        self.video_id = None
        self.transcript = None
        self.chunks = None
        self.vector_index = None
        self.output_language: str = "en"


class SessionManager:
    def __init__(self):
        self.sessions: Dict[int, UserSession] = {}

    def get_session(self, user_id: int) -> UserSession:
        if user_id not in self.sessions:
            self.sessions[user_id] = UserSession()
        return self.sessions[user_id]

    def clear_session(self, user_id: int):
        if user_id in self.sessions:
            self.sessions[user_id] = UserSession()