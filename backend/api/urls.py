from django.urls import path
from . import views

urlpatterns = [
    path('v1/health', views.health,name="health"),
    path('v1/authenticate',views.authenticate,name='authenticate'),
    path('v1/upload', views.file_upload,name="file-upload"),
    path('v1/get-products',views.getProducts,name='get-products'),
    path('v1/get-categories',views.getCategories,name='get-categories'),
    path('v1/get-products-stock-filters',views.getProductStockFilters,name='get-product-stock-filters'),
    path('v1/create-product',view=views.createProduct,name='create-product'),
    path('v1/complete-cart',view=views.completeCart,name='complete-cart'),
    path('v1/get-product-updates',view=views.getProductUpdates,name='get-product-updates'),
    path('v1/get-employee-details',view=views.getEmployeeDetails,name='get-employee-details'),
    path('v1/get-teller-sales',views.getTellerSales,name='get-teller-sales')
]
