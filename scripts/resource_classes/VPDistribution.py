import Utils
import Config
import chevron
from rdflib import Graph

class VPDistribution():
    """
    This class extends Resource class with properties specific to dataset properties
    """

    URL = None
    PARENT_URL = None
    LICENSE = None
    TITLE = None
    DESCRIPTION = None
    PUBLISHER = None
    VERSION = None
    ACCESSRIGHTS = None
    HASPOLICY = None
    MEDIATYPE = None
    ISPARTOF = []
    ACCESSURL = None
    DOWNLOADURL = None
    ACCESSSERVICE = None
    CONFORMSTO = None


    def __init__(self,* , parent_url, license, title, description, 
                 publisher, version, accessrights, haspolicy, 
                 mediatype, ispartof, accessurl, downloadurl,
                 accessservice, conformsto):
        """
        :param parent_url: Parent's FDP URL of a distribution (mandatory)

        :param license: Licence of a distribution (e.g. http://rdflicense.appspot.com/rdflicense/cc-by-nc-nd3.0) (mandatory)
        :param title: Title of a distribution (mandatory)
        :param description: Description of a distribution (mandatory)
        :param publisher: Publisher of a distribution (mandatory)
        :param version: The version of a distribution (mandatory)

        :param accessrights: The accessrights of a distribution (recommended)
        :param haspolicy: ODRL policy belonging to a distribution (optional)
        :param mediatype: mediatype of a distribution (optional)
        :param ispartof: (optional)
        :param accessurl: access url of a distribution (optional)
        :param downloadurl: download url of a distribution (optional)
        :param accessservice: access service of a distribution (optional)
        :param conformsto: conforms to of distribution (recommended)
        """
        self.PARENT_URL = parent_url
        self.LICENSE = license
        self.TITLE = title
        self.DESCRIPTION = description
        self.PUBLISHER = publisher
        self.VERSION = version
        self.ACCESSRIGHTS = accessrights
        self.HASPOLICY = haspolicy
        self.MEDIATYPE = mediatype
        self.ISPARTOF = ispartof
        self.ACCESSURL = accessurl
        self.DOWNLOADURL = downloadurl
        self.ACCESSSERVICE = accessservice
        self.CONFORMSTO = conformsto

    
    def get_graph(self):
        """
        Method to get dataset RDF

        :return: dataset RDF
        """
        utils = Utils.Utils()
        graph = Graph()

        ispartof_str = utils.list_to_rdf_URIs(self.ISPARTOF)

        with open('../templates/vpdistribution.mustache', 'r') as f:
            body = chevron.render(f, {'license': self.LICENSE, 'title': self.TITLE,
                                      'description': self.DESCRIPTION, 'publisher': self.PUBLISHER,
                                      'version': self.VERSION, 'accessrights': self.ACCESSRIGHTS,
                                      'haspolicy': self.HASPOLICY, 'mediatype': self.MEDIATYPE,
                                      'ispartof': ispartof_str, 'accessurl': self.ACCESSURL,
                                      'downloadurl': self.DOWNLOADURL, 'accessservice': self.ACCESSSERVICE,
                                      'conformsto': self.CONFORMSTO})
            if Config.DEBUG:
                print("RDF created with Mustache template:")
                print(body)            
            graph.parse(data=body, format="turtle")

        return graph
    