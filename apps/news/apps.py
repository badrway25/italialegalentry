from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "news"
    verbose_name = "Actualités"

    def ready(self):
        from core.public_routes import register_public_paths
        from core.sitemaps import register
        from news.sitemaps import ArticleSitemap, NewsIndexSitemap

        register("news_index", NewsIndexSitemap)
        register("news", ArticleSitemap)
        # V5.12 §8: the list page exists once one article is live (core.gates.news_public); its prescribed
        # header and newsletter keep their own gates (G3 / flag).
        register_public_paths("news", ["actualites/"], requires_gate="news_public")
