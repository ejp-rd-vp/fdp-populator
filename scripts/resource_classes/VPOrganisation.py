import Config
import chevron
from rdflib import Graph

class VPOrganisation():
    """
    This class describes the organisation class
    """
    URL = None
    PARENT_URL = None
    TITLE = None
    DESCRIPTION = None
    LOCATION_TITLE = None
    LOCATION_DESCRIPTION = None
    LANDING_PAGES = None


    def __init__(self,* , parent_url, title, description, pages, logo, location, identifier):
        """
        :param parent_url: Parent's catalog URL of an organisation. NOTE this url should exist in an FDP (mandatory)
        :param title: Title of an organisation (mandatory)
        :param description: Description of an organisation (mandatory)
        :param pages: Landing page URLs of an organisation (mandatory)
        :param logo: Logo of an organisation (optional)
        :param location_title: title of a location of an organisation (optional)
        :param identifier: identifier of an organisation (optional)
        """
        self.PARENT_URL = parent_url
        self.TITLE = title
        self.DESCRIPTION = description
        self.LANDING_PAGES = pages
        self.LOGO = logo
        self.LOCATION = location
        self.IDENTIFIER = identifier
    
    def get_graph(self):
        """
        Method to get organisation RDF

        :return: organisation RDF
        """
        # Create pages list
        page_str = ""
        for page in self.LANDING_PAGES:
            page_str = page_str + " <" + page + ">,"
        page_str = page_str[:-1]

        # Render RDF
        graph = Graph()

        with open('../templates/vporganisation.mustache', 'r') as f:
            body = chevron.render(f, {'parent_url': self.PARENT_URL,
                                      'title': self.TITLE,
                                      'description': self.DESCRIPTION,
                                      'pages': page_str,
                                      'logo': self.LOGO,
                                      'location': self.LOCATION,
                                      'identifier': self.IDENTIFIER})
            if Config.DEBUG:
                print("RDF created with Mustache template:")
                print(body)
            graph.parse(data=body, format="turtle")

        return graph