import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.pdf

@anvil.server.callable
def l_create_pdf():
      media_object=anvil.pdf.render_form("Test.Form1")
      return media_object