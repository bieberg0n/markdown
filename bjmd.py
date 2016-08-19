import markdown
import re

# h1,h2,h3,h4,h5,h6 {font-family:微软雅黑;}
# p {font-family:黑体;}
def add_font(html):
	new_html = '''<html>
	<head>
	<style type="text/css">
	body {font-family:新宋体;}
	blockquote {
	  margin: 1em 3em;
	  padding: 5px 5px;
	  padding-left: 1em;
	  border-left: 10px solid #D6DBDF;
	  background: none repeat scroll 0 0 rgba(102,128,153,.05);
	  background-color: #f2f3f1;}
	</style>
	</head>
	<body>''' + html +\
		'''</body>
		</html>'''
	return new_html

def bjmd(text):
	p = re.compile('\n')
	text = p.sub('  \n', text)
	pp = re.compile(' +\n')
	text = pp.sub('  \n', text)

	html = add_font(markdown.markdown(text))
	return html
