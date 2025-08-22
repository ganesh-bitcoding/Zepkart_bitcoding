from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Product, ProductImage
from UserAccounts.models import Seller

class AddProductView(LoginRequiredMixin, generic.View):
    template_name = "Product/addProduct.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        user = request.user


        # Get normal form fields
        name = request.POST.get("name")
        description = request.POST.get("description")
        category = request.POST.get("category")
        price = request.POST.get("price")
        discount_price = request.POST.get("discount_price")
        stock_quantity = request.POST.get("stock_quantity")

        # Validation (basic example)
        if not name or not price or not stock_quantity:
            return render(request,self.template_name, context={"success": False, "message": "Name, price and stock are required."})
        # Save product
        seller = Seller.objects.get(user=request.user)
        product = Product.objects.create(
            seller=seller,
            name=name,
            description=description,
            category=category,  
            price=price,
            discount_price=discount_price or None,
            stock_quantity=stock_quantity,
        )

        # Handle multiple images
        images = request.FILES.getlist("images")
        for img in images:
            ProductImage.objects.create(product=product, image=img)
        return redirect('myproductlist')
class SellerProductView(LoginRequiredMixin, generic.View):
    template_name = "Product/SellerPrductDisplay.html"
    def get(self, request, *args, **kwargs):
        user = request.user
        seller = Seller.objects.get(user=user)
        products = seller.products.all()
        return render(request, self.template_name, context={"products":products, "user" : seller.store_name})
    
class SellerProductUpdateView(LoginRequiredMixin, generic.View):
    template_name = "Product/updateProduct.html"

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk") 
        seller = get_object_or_404(Seller, user=request.user)
        product = get_object_or_404(Product, pk=pk, seller=seller)
        return render(request, self.template_name, {"product": product})

    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk") 
        seller = get_object_or_404(Seller, user=request.user)
        product = get_object_or_404(Product, pk=pk, seller=seller)
        # update fields manually (since you’re using custom HTML form)
        product.name = request.POST.get("name")
        product.description = request.POST.get("description")
        product.price = request.POST.get("price")
        product.stock = request.POST.get("stock")
        product.save()

        # handle new images
        if request.FILES.getlist("images"):
            # product.images.all().delete()
            for img in request.FILES.getlist("images"):
                ProductImage.objects.create(product=product, image=img)
        return redirect("myproductlist")
    
class SellerProductDeleteView(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk") 
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return redirect("myproductlist")
    
class SellerProductDetailsView(LoginRequiredMixin, generic.View):
    template_name = "Product/ProductDetails.html"
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        product = get_object_or_404(Product, pk=pk)
        return render(request,self.template_name, context={"product":product})