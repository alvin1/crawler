from modules.file_helper import FileHelper
from modules.extracter import Extracter
from modules.settings import Settings
from modules.html_loader import HtmlLoader

httploader = HtmlLoader()
filehelper = FileHelper()

filehelper.write('var/tmp/2640.html', httploader.get_page_content(Settings.URL, 2640, Settings.RETRY_TIMES))
