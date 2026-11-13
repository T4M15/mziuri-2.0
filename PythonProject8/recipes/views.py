import random
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import redirect

RECIPES = [
    {"id": 1, "slug": "khinkali", "name": "ხინკალი", "category": "main", "minutes": 90, "vegetarian": False, "ingredients": ["ფქვილი", "საქონლის ხორცი", "ღორის ხორცი", "ხახვი", "კვლიავი"]},
    {"id": 2, "slug": "khachapuri", "name": "ხაჭაპური", "category": "bakery", "minutes": 60, "vegetarian": True, "ingredients": ["ფქვილი", "იმერული ყველი", "კვერცხი", "კარაქი"]},
    {"id": 3, "slug": "lobiani", "name": "ლობიანი", "category": "bakery", "minutes": 75, "vegetarian": True, "ingredients": ["ფქვილი", "ლობიო", "ხახვი", "კარაქი"]},
    {"id": 4, "slug": "pkhali", "name": "ფხალი", "category": "snack", "minutes": 30, "vegetarian": True, "ingredients": ["ისპანახი", "ნიგოზი", "ნიორი", "ქინძი"]},
    {"id": 5, "slug": "churchkhela", "name": "ჩურჩხელა", "category": "dessert", "minutes": 240, "vegetarian": True, "ingredients": ["ნიგოზი", "ყურძნის წვენი", "ფქვილი"]},
    {"id": 6, "slug": "chakapuli", "name": "ჩაქაფული", "category": "main", "minutes": 120, "vegetarian": False, "ingredients": ["ცხვრის ხორცი", "ტყემალი", "ტარხუნა", "თეთრი ღვინო"]},
]

def page(title, body):
    return HttpResponse(f"<h1>{title}</h1>{body}<br><br><a href='/recipes/'>← ყველა რეცეპტი</a>")

def recipe_list(request):
    filtered = RECIPES
    if cat := request.GET.get("category"):
        filtered = [r for r in filtered if r["category"] == cat]
    if max_t := request.GET.get("max_time"):
        if max_t.isdigit():
            filtered = [r for r in filtered if r["minutes"] <= int(max_t)]
    if request.GET.get("vegetarian") == "yes":
        filtered = [r for r in filtered if r["vegetarian"]]

    if not filtered:
        body = "<p>ვერაფერი მოიძებნა</p>"
    else:
        items = "".join([f"<li><a href='/recipes/{r['id']}/'>{r['name']}</a> · {r['minutes']} წთ</li>" for r in filtered])
        body = f"<ul>{items}</ul>"
    return page("ქართული რეცეპტები", body)

def recipe_detail(request, pk):
    recipe = next((r for r in RECIPES if r["id"] == pk), None)
    if not recipe: raise Http404("ვერ მოიძებნა")
    ings = "".join([f"<li>{i}</li>" for i in recipe["ingredients"]])
    body = f"<p>კატეგორია: {recipe['category']}</p><p>დრო: {recipe['minutes']} წთ</p><p>ვეგეტარიანული: {'კი' if recipe['vegetarian'] else 'არა'}</p><h3>ინგრედიენტები:</h3><ul>{ings}</ul>"
    return page(recipe["name"], body)

def category_detail(request, cat_name):
    cat_recipes = [r for r in RECIPES if r["category"] == cat_name]
    if not cat_recipes: raise Http404("კატეგორია არ მოიძებნა")
    items = "".join([f"<li><a href='/recipes/{r['id']}/'>{r['name']}</a> · {r['minutes']} წთ</li>" for r in cat_recipes])
    return page(f"კატეგორია: {cat_name}", f"<ul>{items}</ul>")

def search(request):
    q = request.GET.get("q", "").strip()
    if not q: body = "<p>ჩაწერე საძიებო სიტყვა</p>"
    else:
        matched = [r for r in RECIPES if any(q.lower() in i.lower() for i in r["ingredients"])]
        items = "".join([f"<li><a href='/recipes/{r['id']}/'>{r['name']}</a></li>" for r in matched]) if matched else "<p>ვერაფერი მოიძებნა</p>"
        body = f"<ul>{items}</ul>"
    return page(f"ძებნა: {q}", body)

def random_recipe(request):
    return redirect("recipes:detail", pk=random.choice(RECIPES)["id"])

def stats(request):
    cats = {}
    for r in RECIPES: cats[r["category"]] = cats.get(r["category"], 0) + 1
    avg = sum(r["minutes"] for r in RECIPES) / len(RECIPES)
    return JsonResponse({"count": len(RECIPES), "categories": cats, "avg_minutes": avg}, json_dumps_params={"ensure_ascii": False})