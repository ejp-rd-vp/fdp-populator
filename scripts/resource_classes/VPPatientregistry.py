import Config
import chevron
from rdflib import Graph
from resource_classes import VPDataset


class VPPatientRegistry(VPDataset.VPDataset):
    """
    This class describes the patient registry class
    """
    URL = None
    POPULATIONCOVERAGE = None


    def __init__(self,* , parent_url, license, title, description, 
                 theme, publisher, contactpoint, language, personaldata, 
                 conformsto, vpconnection, keyword, logo, haspolicy, 
                 identifier, issued, modified, version, accessrights,
                 landingpage, distribution, populationcoverage):
        """
        :param parent_url: Parent's FDP URL of a patient registry

        :param license: Licence of a patient registry (e.g. http://rdflicense.appspot.com/rdflicense/cc-by-nc-nd3.0) (mandatory)
        :param title: Title of a patient registry (mandatory)
        :param description: Description of a patient registry (mandatory)
        :param theme: Themes of a patient registry (mandatory)
        :param publisher: Publisher of a patient registry (mandatory)
        :param contactpoint: Contactpoint of a patient registry (mandatory)
        :param langauge: Language of a patient registry (e.g. http://id.loc.gov/vocabulary/iso639-1/en) (mandatory)
        :param personaldata: Whether a patient registry is personal data (mandatory)

        :param conformsto: Specification the patient registry conforms to (optional)
        :param vpconnection: Connection of a patient registry to the Virtual platform (optional)
        :param keyword: Keyword of a patient registry (optional)
        :param logo: Logo of a patient registry (optional)
        :param haspolicy: ODRL policy belonging to a patient registry (optional)
        :param identifier: Identifier of a patient registry (optional)
        :param issued: The date a patient registry was issued (optional)
        :param modified: The date a patient registry was last modified (optional)
        :param version: The version of a patient registry (optional)

        :param accessrights: The accessrights of a patient registry (recommended)
        :param landingpage: The landingpage of a patient registry (recommended)

        :param distribution: The distribution of a patient registry (optional)

        :param populationcoverage: The population coverage of a patient registry (mandatory)
        """

        super().__init__(parent_url=parent_url, license=license, 
                        title=title, description=description,
                        theme=theme, publisher=publisher,
                        contactpoint=contactpoint, language=language, 
                        personaldata=personaldata, conformsto=conformsto, 
                        vpconnection=vpconnection, keyword=keyword, 
                        logo=logo, haspolicy=haspolicy, 
                        identifier=identifier, issued=issued, 
                        modified=modified, version=version,
                        accessrights=accessrights, landingpage=landingpage, 
                        distribution=distribution)

        self.POPULATIONCOVERAGE = populationcoverage

    def get_graph(self):
        """
        Method to get patient registry RDF

        :return: patient registry RDF
        """
        graph = super().get_graph()

        # Render RDF
        with open('../templates/vppatientregistry.mustache', 'r') as f:
            body = chevron.render(f, {'populationcoverage': self.POPULATIONCOVERAGE})
            if Config.DEBUG:
                print("RDF created with Mustache template:")
                print(body)
            graph.parse(data=body, format="turtle")

        return graph