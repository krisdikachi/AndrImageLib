# views.py
from django.shortcuts import render
import requests
from django.http import JsonResponse, Http404, HttpResponse
from django.conf import settings
import json

def app(request):
    image_data = []
    if request.GET.get("search"):
        search_query = request.GET.get("search")
        quantity = request.GET.get("quantity")
        url = f"https://api.unsplash.com/search/photos?query={search_query}&per_page={quantity}&client_id={settings.UNSPLASH_CLIENT_ID}"
        response = requests.get(url)
        
        if response.status_code == 200:
            image_data = response.json()
            if "results" in image_data:
                image_data = [images["urls"]["full"] for images in image_data["results"]]
            else:
                image_data = []
        else:
            print(f"Error fetching data from Unsplash API: {response.status_code}")
            image_data = []

    context = {"images": image_data}
    return render(request, "app.html", context=context)



def trigger_download(request,image_id):
    url = f"https://api.unsplash.com/photos/{image_id}/download"
    headers = {"Authorization": f"Client-ID {settings.UNSPLASH_CLIENT_ID}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return JsonResponse({"message": "Download triggered"})
    return JsonResponse({"error": "Failed to trigger download"}, status=400)


def fetch_images(query):
    url = f"https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {settings.UNSPLASH_ACCESS_KEY}"}
    params = {"query": query, "per_page": 10}
    response = requests.get(url, headers=headers, params=params)
    return response.json() if response.status_code == 200 else {}

def image_gallery(request):
    query = request.GET.get("query", "nature")
    images = fetch_images(query)
    return render(request, "app.html", {"images": images.get("results", [])})


def image_gallery(request):
    query = request.GET.get("query", "nature")
    images = fetch_images(query)
    print(json.dumps(images, indent=4))  # Print the API response to inspect it
    return render(request, "app.html", {"images": images.get("results", [])})





def download_image(request):
    image_url = request.GET.get(f"https://api.unsplash.com/search/photos")  # URL of the image from the API
    if not image_url:
        return Http404("Image URL not provided")

    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        # Extract the file name from the URL
        file_name = image_url.split("/")[-1]

        # Create an HTTP response with the image data
        file_response = HttpResponse(response.content, content_type=response.headers['Content-Type'])
        file_response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return file_response
    else:
        return Http404("Failed to fetch the image")