from django.urls import path, include
from django.http import HttpResponse
from .views import *

app_name = "api"

urlpatterns = [
    path("<int:username>/", get_curr_user),
    path("<int:username>/first/<path:first_name>/", update_first),
    path("<int:username>/last/<path:last_name>/", update_last),
    path("<int:username>/post/cat/<path:category>/", update_category),
    path("<int:username>/post/disaster/<int:pk>/", update_disaster),
    path("<int:username>/post/amount/<int:amount>/", update_amount),
    path("disasters/", get_disasters),
    path("<int:username>/post/<path:message>/", create_post),
    path("<int:merchant_phone>/transaction/<path:pk>/", make_transaction),
    path("<int:username>/user/<path:cat>/", update_score),
]

