import webbrowser
import urllib.parse

text = "This is the text for my note."
encoded_text = urllib.parse.quote(text)
shortcut_name = "CreateNote"

url = f'shortcuts://run-shortcut?name={shortcut_name}&input={encoded_text}'
webbrowser.open(url)
