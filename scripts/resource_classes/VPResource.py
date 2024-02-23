import chevron
from rdflib import Graph

class VPResource:
    """
    Super class contents generic resource metadata properties
    """
    URL = None
    PARENT_URL = None

    LICENSE = None
    TITLE = None
    DESCRIPTION = None
    THEME = []
    PUBLISHER = None
    CONTACTPOINT = None
    LANGUAGE = None
    PERSONALDATA = None

    CONFORMSTO = None
    VPCONNECTION = None
    KEYWORD = []
    LOGO = None
    HASPOLICY = None
    IDENTIFIER = None
    ISSUED = None
    MODIFIED = None
    VERSION = None

    ACCESSRIGHTS = None
    LANDINGPAGE = None


    def __init__(self, parent_url, license, title, description, theme, 
                 publisher, contactpoint, language, personaldata, 
                 conformsto, vpconnection, keyword, logo, haspolicy, 
                 identifier, issued, modified, version, accessrights,
                 landingpage):
        """
        :param parent_url: Parent's FDP URL of a resource

        :param license: Licence of a resource (e.g. http://rdflicense.appspot.com/rdflicense/cc-by-nc-nd3.0) (mandatory)
        :param title: Title of a resource (mandatory)
        :param description: Description of a resource (mandatory)
        :param theme: Themes of a resource (mandatory)
        :param publisher: Publisher of a resource (mandatory)
        :param contactpoint: Contactpoint of a resource (mandatory)
        :param langauge: Language of a resource (e.g. http://id.loc.gov/vocabulary/iso639-1/en) (mandatory)
        :param personaldata: Whether a resource is personal data (mandatory)

        :param conformsto: Specification the resource conforms to (optional)
        :param vpconnection: Connection of a resource to the Virtual platform (optional)
        :param keyword: Keyword of a resource (optional)
        :param logo: Logo of a resource (optional)
        :param haspolicy: ODRL policy belonging to a resource (optional)
        :param identifier: Identifier of a resource (optional)
        :param issued: The date a resource was issued (optional)
        :param modified: The date a resource was last modified (optional)
        :param version: The version of a resource (optional)

        :param accessrights: The accessrights of a resource (recommended)
        :param landingpage: The landingpage of a resource (recommended)
        """

        self.PARENT_URL = parent_url

        self.LICENSE = license
        self.TITLE = title
        self.DESCRIPTION = description
        self.THEME = theme
        self.PUBLISHER = publisher
        self.CONTACTPOINT = contactpoint
        self.LANGUAGE = language
        self.PERSONALDATA = personaldata

        self.CONFORMSTO = conformsto
        self.VPCONNECTION = vpconnection
        self.KEYWORD = keyword
        self.LOGO = logo
        self.HASPOLICY = haspolicy
        self.IDENTIFIER = identifier
        self.ISSUED = issued
        self.MODIFIED = modified
        self.VERSION = version

        self.ACCESSRIGHTS = accessrights
        self.LANDINGPAGE = landingpage

    def get_graph(self):
        graph = Graph()

        if self.ACCESS_TYPE == "Access Information":
            self.ACCESS_TYPE = "dct:accessRight"
        elif self.ACCESS_TYPE == "ODRL Policy":
            self.ACCESS_TYPE = "odrl:hasPolicy"
        else:
            print("Unexcepted access type: ", self.ACCESS_TYPE, ", defaulting to no access information")
            self.ACCESS = ""

        with open('../templates/vpresource.mustache', 'r') as f:
            body = chevron.render(f, {'parent_url': self.PARENT_URL, 'title': self.TITLE,
                                      'description': self.DESCRIPTION, 'publisher_url': self.PUBLISHER_URL,
                                      'license_url': self.LICENSE_URL, 'version': self.VERSION,
                                      'access': self.ACCESS, 'access_type': self.ACCESS_TYPE})
            graph.parse(data=body, format="turtle")

        return(graph)
