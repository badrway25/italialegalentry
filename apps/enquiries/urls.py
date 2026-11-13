from django.urls import path

from enquiries import views

app_name = "enquiries"

PUBLIC_PATHS = {
    "company_needs": "entreprises/recueil-des-besoins/",
    "institution_proposal": "collaboration/institutions/",
    "university_proposal": "collaboration/universites-formation/",
    "contact": "contact/formulaire/",
    "done": "demande-transmise/",
}

urlpatterns = [
    path(PUBLIC_PATHS["company_needs"], views.company_needs, name="company_needs"),
    path(PUBLIC_PATHS["institution_proposal"], views.institution_proposal, name="institution_proposal"),
    path(PUBLIC_PATHS["university_proposal"], views.university_proposal, name="university_proposal"),
    path(PUBLIC_PATHS["contact"], views.contact, name="contact"),
    path(PUBLIC_PATHS["done"], views.done, name="done"),
]
