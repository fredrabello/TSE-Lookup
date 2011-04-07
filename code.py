from tseclasses import *
import web

render = web.template.render('templates/', globals={'re':re})

urls = (
	'/', 'index',
	'/json', 'jason'
)


app = web.application(urls, globals())

class index:
	def GET(self):
		conn = connectDb(database)		
		companies = loadEmpresas(conn)
		i = web.input(url='')		
		if (i.url):		
			story = Article(i.url)
			hits = story.checkStory(companies)
			results = story.checkDonations(conn)
		else:
			results = []
			story = None
		return render.index(story, results)


if __name__ == "__main__": app.run()

