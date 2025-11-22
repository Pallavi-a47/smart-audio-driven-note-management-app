import os

class Config:
    SECRET_KEY = os.environ.get('qheouq3oerqtirscdjysfdjd', 'glm2sgilmfglegflqgriygwrytqeywrtqywet')
    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://root:your_password@localhost/speech_to_text'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
