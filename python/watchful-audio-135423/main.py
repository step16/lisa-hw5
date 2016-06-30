
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2
import cgi


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write("""<html>
	<head>
		<meta http-equiv="content-type" content="text/html; charset=utf-8">
	</head>
	<body>
		<form action="/wordshuffle" method="POST">
			<input type=text name=word1><br></input>
			<input type=text name=word2><br></input>
			<input type=submit value=Submit></input>
		</form>
	</body>
</html>""")


    def post(self):
		word1 = self.request.get("word1")
		word2 = self.request.get("word2")
		len1 = len(word1)
		len2 = len(word2)
		result  = ''

		for index in range(min(len1, len2)):
			result += word1[index]
			result += word2[index]

		self.response.headers["Content-Type"] = "text/html; charset=utf-8"
		self.response.out.write("""
                                <html>
                                  <body>
                                    result:
                                """)
		self.response.out.write(result.encode('utf-8'))
		self.response.out.write("""
                                  </body>
                                </html>
                                """
                                )


app = webapp2.WSGIApplication([("/wordshuffle", MainPage)],
                              debug=True)