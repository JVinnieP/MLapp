import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models 

BASE_MLIB_URL = 'https://listado.mercadolibre.com.co/instrumentos-musicales/{}'

def home(request):
	return render(request, 'base.html')

def new_search(request):
	search = request.POST.get('search')
	models.Search.objects.create(search=search)
	final_url = BASE_MLIB_URL.format(quote_plus(search))
	response = requests.get(final_url)
	data = response.text
	soup = BeautifulSoup(data, features='html.parser')

	post_listings = soup.find_all('li', {'class': "results-item"})

	final_postings =[]

	for post in post_listings:
		post_title = post.find(class_='main-title').text
		post_url = post.find('a').get('href')
		post_price = post.find(class_='price__fraction').text
		post_image = post.find('img').get('src') or post.find('img').get('data-src')

		final_postings.append((post_title, post_url, post_price, post_image))

	stuff_for_frontend = {
		'search': search,
		'final_postings': final_postings,
	}

	return render(request, 'mlib_app/new_search.html', stuff_for_frontend)