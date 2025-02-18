from dotenv import load_dotenv
import os
load_dotenv()

spreadsheet_url = os.getenv('spreadsheet_url')
credentials_path = os.getenv('credentials_path')

room_keys = [i for i in range(5)]
