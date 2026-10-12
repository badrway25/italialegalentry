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
        # The list page is always reachable: only its prescribed header/newsletter are gated (G3 / flag).
        register_public_paths("news", ["actualites/"])
