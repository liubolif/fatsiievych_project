import os


class Config:
    SECRET_KEY = os.urandom(24)
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgres://vplrizcsxwbpap:ee67dfccbdb3cc5b4751c9fdb306ed59fd36996313feb849fb231b682fdd189f@ec2-107-22-83-3.compute-1.amazonaws.com:5432/d72pnrfr3lnlfm'#os.environ.get('DATABASE_URL') or 'sqlite:///site.db' ##
