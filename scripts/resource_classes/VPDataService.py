import Utils
import Config
import chevron
from rdflib import Graph
from resource_classes import VPResource

class VPDataService(VPResource.VPResource):
    """
    This class extends Resource class with properties specific to dataset properties
    """
    OTYPE = None
    SERVERSDATASET = []
    ENDPOINTURL = []
    ENDPOINTDESCRIPTION = []


    def __init__(self, *, parent_url, license, title, description,
                 theme, publisher, contactpoint, language, personaldata, 
                 conformsto, vpconnection, keyword, logo, haspolicy, 
                 identifier, issued, modified, version, accessrights,
                 landingpage, otype, servesdataset, endpointurl, 
                 endpointdescription):
        """

        :param parent_url: Parent's FDP URL of a dataset

        :param license: Licence of a dataset (e.g. http://rdflicense.appspot.com/rdflicense/cc-by-nc-nd3.0) (mandatory)
        :param title: Title of a dataset (mandatory)
        :param description: Description of a dataset (mandatory)
        :param theme: Themes of a dataset (mandatory)
        :param publisher: Publisher of a dataset (mandatory)
        :param contactpoint: Contactpoint of a dataset (mandatory)
        :param langauge: Language of a dataset (e.g. http://id.loc.gov/vocabulary/iso639-1/en) (mandatory)
        :param personaldata: Whether a dataset is personal data (mandatory)

        :param conformsto: Specification the dataset conforms to (optional)
        :param vpconnection: Connection of a dataset to the Virtual platform (optional)
        :param keyword: Keyword of a dataset (optional)
        :param logo: Logo of a dataset (optional)
        :param haspolicy: ODRL policy belonging to a dataset (optional)
        :param identifier: Identifier of a dataset (optional)
        :param issued: The date a dataset was issued (optional)
        :param modified: The date a dataset was last modified (optional)
        :param version: The version of a dataset (optional)

        :param accessrights: The accessrights of a dataset (recommended)
        :param landingpage: The landingpage of a dataset (recommended)

        :param otype: Type of the dataservice (edam operation) (mandatory)
        :param servesdataset: The datasets the dataservice serves (optional)
        :param endpointurl: Url of the endpoint (recommended)
        :param endpointdescription: Description of the endpoint (recommended)
        """
        # Pass core properties to parent class
        super().__init__(parent_url, license, title, description, 
                 theme, publisher, contactpoint, language, personaldata, 
                 conformsto, vpconnection, keyword, logo, haspolicy, 
                 identifier, issued, modified, version, accessrights,
                 landingpage)
        
        self.OTYPE = otype
        self.SERVERSDATASET = servesdataset
        self.ENDPOINTURL = endpointurl
        self.ENDPOINTDESCRIPTION = endpointdescription

    def get_graph(self):
        """
        Method to get dataservice RDF

        :return: dataservice RDF
        """
        utils = Utils.Utils()
        graph = super().get_graph()

        servesdataset_str = utils.list_to_rdf_URIs(self.SERVERSDATASET)
        endpointdescription_str = utils.list_to_rdf_URIs(self.ENDPOINTDESCRIPTION)

        with open('../templates/vpdataservice.mustache', 'r') as f:
            body = chevron.render(f, {'type': self.OTYPE, 'serversdataset_str': servesdataset_str,
                                      'endpointurl': self.ENDPOINTURL,
                                      'endpointdescription_str': endpointdescription_str})
            if Config.DEBUG:
                print("RDF created with Mustache template:")
                print(body)
            graph.parse(data=body, format="turtle")

        return graph