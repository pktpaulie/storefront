from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F
from store.models import Product, Customer, Collection, Order, OrderItem



def say_hello(request):
    # keyword=value
    #filter products with price range from 20 to 30 returns a string
    #queryset = Product.objects.filter(unit_price__range=(20, 30))
    # contains - case sensitiver search, icontains - case insensitive
    # startswith - istartswith, endswith - iendswith
    #queryset = Product.objects.filter(title__icontains='coffee')
    #check if its description is null: description__isnull=True
    # date lookup - last_update__year
    #queryset = Product.objects.filter(last_update__year=2021)
    #except ObjectDoesNotExist:

    #Filtering Exercise
    ''' 
    Customers with .com accounts 
    Collections that dont have a featured product - worked
     ---change html to order in products (products here is just a name used in the render)
      ----customer.email
    Products with low inventory (less than 10) - worked
    Orders placed by customer with id = 1 --seems to have worked
        ----
    Order items for products in collection 3 --seems to have worked
    '''
    #queryset = Customer.objects.filter(email__contains='.com')
    #queryset = Collection.objects.filter(featured_product__isnull=True) #worked
    #queryset = Product.objects.filter(inventory__lt=10) # worked
    #queryset = Order.objects.filter(customer__id=1)
    #queryset = OrderItem.objects.filter(product__collection__id=3)

    '''
    multiply filters/ complex lookups
    '''
    #queryset = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
    #queryset = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)
    # using Q - Query
    #queryset = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20)) # OR
    #queryset = Product.objects.filter(Q(inventory__lt=10) & ~Q(unit_price__lt=20)) # ~ NOT
    # using F function
    #queryset = Product.objects.filter(inventory=F('unit_price'))

    #sorting - add a negative to sort by Descending Order
    #queryset = Product.objects.order_by('unit_price', '-title').reverse()
    #queryset = Product.objects.filter(collection__id=1).order_by('unit_price')
    #product = Product.objects.order_by('unit_price')[0] #gives an individual element
    products = Product.objects.earliest('unit_price')

    return render(request, 'hello.html', {'name': 'Pauline', 'products': products})
