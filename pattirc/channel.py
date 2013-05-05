import json

from message import Message

class Channel:
    def __init__(self, client, id, name):
        self.client = client
        self.id = id
        self.name = name
        self.observers = []
        self.messages = []
        self.retrieve_messages()

    def retrieve_messages(self):
        messages_str = self.client.api.getMessageChannel(self.id)
        messages_adn = json.loads(messages_str)['data']
        
        for m in messages_adn:
            m_id = m['id']
            m_authorname = m['user']['username']
            m_text = m['text']
            m_time = m['created_at']
            
            m_found = False
            for msg in self.messages:
                if msg.id == m_id:
                    m_found = True

            if not m_found:
                self.messages.insert(0, Message(id=m_id, authorname=m_authorname,
                    text=m_text, time=m_time))   

    def update(self):
        for o in self.observers:
            o.update()

    def send_message(self, string):
        api = self.client.api
        api.createMessage(self.id, text=string)

    def render(self):
        lines = []
        for m in sorted(self.messages, key=lambda x: x.time):
            lines.append(m.render())

        return lines
