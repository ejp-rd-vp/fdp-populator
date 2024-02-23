import chevron
from rdflib import Graph
from resource_classes import VPResource


class VPBiobank():
    """
    This class describes the biobank class
    """
    URL = None
    POPULATIONCOVERAGE = None


    def __init__(self,* , parent_url, license, title, description, 
                 theme, publisher, contactpoint, language, personaldata, 
                 conformsto, vpconnection, keyword, logo, haspolicy, 
                 identifier, issued, modified, version, accessrights,
                 landingpage, populationcoverage):
        """
        :param parent_url: Parent's FDP URL of a biobank

        :param license: Licence of a biobank (e.g. http://rdflicense.appspot.com/rdflicense/cc-by-nc-nd3.0) (mandatory)
        :param title: Title of a biobank (mandatory)
        :param description: Description of a biobank (mandatory)
        :param theme: Themes of a biobank (mandatory)
        :param publisher: Publisher of a biobank (mandatory)
        :param contactpoint: Contactpoint of a biobank (mandatory)
        :param langauge: Language of a biobank (e.g. http://id.loc.gov/vocabulary/iso639-1/en) (mandatory)
        :param personaldata: Whether a biobank is personal data (mandatory)

        :param conformsto: Specification the biobank conforms to (optional)
        :param vpconnection: Connection of a biobank to the Virtual platform (optional)
        :param keyword: Keyword of a biobank (optional)
        :param logo: Logo of a biobank (optional)
        :param haspolicy: ODRL policy belonging to a biobank (optional)
        :param identifier: Identifier of a biobank (optional)
        :param issued: The date a biobank was issued (optional)
        :param modified: The date a biobank was last modified (optional)
        :param version: The version of a biobank (optional)

        :param accessrights: The accessrights of a biobank (recommended)
        :param landingpage: The landingpage of a biobank (recommended)

        :param pouplationcoverage: The population coverage of a biobank (mandatory)
        """

        super().__init__(self, parent_url, license, title, description, 
                theme, publisher, contactpoint, language, personaldata, 
                 conformsto, vpconnection, keyword, logo, haspolicy, 
                 identifier, issued, modified, version, accessrights,
                 landingpage)

        self.POPULATIONCOVERAGE = populationcoverage

    def get_graph(self):
        """
        Method to get biobank RDF

        :return: biobank RDF
        """
        # Create themes list
        theme_str = ""
        for theme in self.THEMES:
            theme_str = theme_str + " <" + theme + ">,"
        theme_str = theme_str[:-1]

        # Create pages list
        page_str = ""
        for page in self.LANDING_PAGES:
            page_str = page_str + " <" + page + ">,"
        page_str = page_str[:-1]

        # Render RDF
        graph = Graph()

        with open('../templates/vpbiobank.mustache', 'r') as f:
            body = chevron.render(f, {'parent_url': self.PARENT_URL,
                                      'title': self.TITLE,
                                      'description': self.DESCRIPTION,
                                      'populationcoverage': self.POPULATIONCOVERAGE,
                                      'themes': theme_str,
                                      'publisher': self.PUBLISHER_URL,
                                      'pages': page_str})
            graph.parse(data=body, format="turtle")

        return graph