content = """
<p id='i1' a='123' b='999'>
	<script>alert(123)</script>
</p>

<p id='i2'>
	<div>
		<p>asdfasdf</p>
	</div>
	<img id='i3' src="/static/imgs\6.jpg" alt="" />
</p>
"""

# # pip3 install beautifulsoup4
# from bs4 import BeautifulSoup
#
# valid_tag = {
# 	'p': ['class','id'],
# 	'img':['src'],
# 	'div': ['class']
# }
#
# soup = BeautifulSoup(content,'html.parser')
#
# tags = soup.find_all()
# for tag in tags:
# 	if tag.name not in valid_tag:
# 		tag.decompose()
# 	if tag.attrs:
# 		for k in list(tag.attrs.keys()): # {id:'i1',a=123,b=999}
# 			if k not in valid_tag[tag.name]:
# 				del tag.attrs[k]
# content_str = soup.decode()
# print(content_str)
# v = soup.find(name='p',attrs={'id':'i2'})
# print(v)


# tag = soup.find(name='p')
# sc = tag.find('script')
# print(sc)

# tag = soup.find(name='p')
# sc = tag.find('script')
# print(sc)

# v = "asdfasd{0}asdfasdf{1}".format()