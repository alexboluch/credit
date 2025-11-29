from django.urls import path, include
from rest_framework.routers import DefaultRouter
from product.views import CreditCreateView, ChangePaymentView


router = DefaultRouter()
router.register(r'credits', CreditCreateView)


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/change_payment/', ChangePaymentView.as_view())
]