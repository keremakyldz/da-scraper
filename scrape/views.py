from django.shortcuts import  get_object_or_404, render
from django.http import HttpResponse
from .models import Brands
from .scrape_utils import MonitorScraper

# Create your views here.

def brand(request):
    latest_brand_list = Brands.objects.order_by("-price_tag")[:10]
    return render(request, "scrape/brands.html",{"latest_brand_list": latest_brand_list})

def detail(request, brand_id):
    brands = get_object_or_404(Brands, pk= brand_id)
    return render(request, "scrape/detail.html",{"brands": brands})

def scrape_and_show(request):
    scraper = MonitorScraper()
    try:
        df = scraper.scrape_all()
    except Exception as e:
        print(f"Error during scraping: {e}")
        return render(request,'scrape/scrape_results.html',{'scraped_data': [], 'error': 'Scraping failed'})
    
    if df.empty:
        return render(request,'scrape/scrape_results.html', {'scraped_data': [], 'error': 'No data found'})
    
    for index, row in df.iterrows():
        Brands.objects.update_or_create(
            brand_name = row['Product Name'],
            defaults={
                'model_name':row.get('Product Name', 'N/A'),
                'price_tag' : row['Price']
            }
        )
    
    scraped_data = df.to_dict(orient='records')
    return render(request, 'scrape/scrape_results.html',{'scraped_data': scraped_data})
