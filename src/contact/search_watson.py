from watson import search as watson

class ContactPointSearchAdapter(watson.SearchAdapter):

    def get_title(self, obj):
        """
        Returns the title of this search result. This is given high priority in search result ranking.

        You can access the title of the search result as `result.title` in your search results.

        The default implementation returns `unicode(obj)`.
        """
        return "{} {}".format(obj.category.title, obj.title_or_organisation)

    def get_description(self, obj):
        """
        Returns the description of this search result. This is given medium priority in search result ranking.

        You can access the description of the search result as `result.description` in your search results. Since
        this should contains a short description of the search result, it's excellent for providing a summary
        in your search results.

        The default implementation returns `u""`.
        """
        keywords = list(obj.keywords.values_list('title', flat=True))
        return obj.slug + " ".join(keywords)

    def get_content(self, obj):
        """
        Returns the content of this search result. This is given low priority in search result ranking.

        You can access the content of the search result as `result.content` in your search results, although
        this field generally contains a big mess of search data so is less suitable for frontend display.

        The default implementation returns all the registered fields in your model joined together.
        """
        return obj.description
