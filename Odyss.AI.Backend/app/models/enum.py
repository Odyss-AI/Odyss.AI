from enum import Enum

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'xlsx', 'pptx', 'jpg', 'jpeg', 'png', 'gif', 'bmp'}

class AvailibleModels(Enum):
    MISTRAL = 'mistral'
    CHATGPT = 'chatgpt'