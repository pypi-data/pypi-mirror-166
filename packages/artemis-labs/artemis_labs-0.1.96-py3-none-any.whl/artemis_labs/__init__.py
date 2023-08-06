'''
Init for Artemis package.
This exposes TokenParser, Token, TokenType, and LineTransformer
'''
# Generic imports
import os 

# Clean super config
temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
with open(os.path.join(temp_dir, 'super_config.py'), 'w') as f:
    f.write('')

# Imports
from .artemis_token_parser import TokenParser
from .artemis_token import Token, TokenType
from .artemis_line_transformer import LineTransformer
