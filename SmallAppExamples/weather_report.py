import urllib,appuifw

def decc():

	def getWeather(city):

    

    		url = 'http://www.google.com/ig/api?weather='

    		try:

      			f = urllib.urlopen(url + city)

    		except:

        		return "Error opening url"

    		s = f.read().replace('\r','').replace('\n','')

    		weather = s.split('</current_conditions>')[0]  \

               .split('<current_conditions>')[-1]  \

               .strip('</>')                       
    

    		for i in weather.split('"/><'):

			w1 = i.split(' data="')

			print w1       

    		return 0	


	def main():

    		while True:

			
        		city = raw_input("Give me a city: ")

        		weather = getWeather(city)

       		print(weather)



	if __name__ == "__main__":

    		main()
