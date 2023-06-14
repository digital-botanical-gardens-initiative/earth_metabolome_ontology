# This Python script generates the Natural product taxonomy as defined by the NPClassifier tool. The output file
#is saved at the current directory of this script execution with the name "npc_taxonomy.ttl" and using the TURTLE RDF
# serialization.
import json
import urllib.parse
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import SKOS, RDFS, RDF, OWL, DCTERMS, VANN


def get_subtaxonomy_list(json_file: str) -> []:
    """ Parse a json object obtained from the html view of the natural product classification defined
    by the NPClassifier tool.

    :param json_file: a json file that is obtained from the NPClassifier_tree4.html file, the JSON object embedded in
      this html page is as follows: {"ids": [...]}.
     NPClassifier_tree4.html:  https://github.com/mwang87/NP-Classifier/blob/master/NPClassifier_tree4.html
    :return: a list of lists where each sublist is composed of at least a Pathway,
     and optionally, a Superclass and Class in this order (e.g., [["Pathway", "Superclass", "Class"], ...]).
    """
    npc_raw_file = open(json_file)
    npc_raw = json.load(npc_raw_file)
    taxonomy = []
    for taxons in npc_raw['ids']:
        subtaxonomy = []
        for taxon in taxons.split('/'):
            if "NPClassifer" not in taxon:
                subtaxonomy.append(taxon.replace("<br>", ""))
        taxonomy.append(subtaxonomy)
    return taxonomy


def generate_rdf_graph(subtaxonomy_list: [], prefix: str) -> Graph:
    """ Generate the Natural Product taxonomy based on the Pathway, Superclass, and Class hierarchy from
    the NPClassifier tool.

    :param subtaxonomy_list: a list of lists where each sublist is composed of at least a Pathway,
     and optionally, a Superclass and Class in this order (e.g., [["Pathway", "Superclass", "Class"], ...]).
    :param prefix: the  prefix of the natural product taxonomy (e.g., "https://purl.org/npc#")
    :return: Natural Product Taxonomy as an RDF Graph
    """
    graph = Graph()
    npc_class = URIRef(prefix + "Class")
    npc_superclass = URIRef(prefix + "Superclass")
    npc_pathway = URIRef(prefix + "Pathway")
    for subtaxonomy in subtaxonomy_list:
        if len(subtaxonomy) >= 1:
            tax_pathway = subtaxonomy[0].strip()
            tax_pathway_uri = URIRef(prefix +
                                     urllib.parse.quote(tax_pathway.replace(" ", "_").upper(), safe=''))
            graph.add((tax_pathway_uri, RDFS.label, Literal(tax_pathway)))
            graph.add((tax_pathway_uri, RDF.type, npc_pathway))
        if len(subtaxonomy) >= 2:
            tax_superclass = subtaxonomy[1].strip()
            tax_superclass_label = tax_superclass
            if tax_superclass == tax_pathway:
                tax_superclass = tax_superclass + "_SUPERCLASS"
            tax_superclass_uri = URIRef(prefix +
                                        urllib.parse.quote(tax_superclass.replace(" ", "_").upper(), safe=''))
            graph.add((tax_superclass_uri, SKOS.broader, tax_pathway_uri))
            graph.add((tax_superclass_uri, RDFS.label, Literal(tax_superclass_label)))
            graph.add((tax_superclass_uri, RDF.type, npc_superclass))
        if len(subtaxonomy) == 3:
            tax_class = subtaxonomy[2].strip()
            tax_class_label = tax_class
            if tax_class == tax_superclass:
                tax_class = tax_class + "_CLASS"
            tax_class_uri = URIRef(prefix +
                                   urllib.parse.quote(tax_class.replace(" ", "_").upper(), safe=''))
            graph.add((tax_class_uri, SKOS.broader, tax_superclass_uri))
            graph.add((tax_class_uri, RDFS.label, Literal(tax_class_label)))
            graph.add((tax_class_uri, RDF.type, npc_class))
    graph.bind("rdf", RDF)
    graph.bind("rdfs", RDFS)
    graph.bind("skos", SKOS)
    NPC = Namespace(prefix)
    graph.bind("npc", NPC)
    npc_vocab = URIRef(prefix.replace("#", ""))
    graph.add((npc_vocab, RDF.type, OWL.Ontology))
    graph.add((npc_vocab, RDF.type, SKOS.ConceptScheme))
    graph.add((npc_vocab, OWL.imports, URIRef(str(SKOS))))
    graph.add((npc_vocab, OWL.versionInfo, Literal("0.1")))
    graph.add((npc_vocab, DCTERMS.creator, URIRef("https://orcid.org/0000-0002-3175-5372")))
    graph.add(
        (npc_vocab, DCTERMS.description, Literal("A natural product taxonomony derived from the NPClassifier tool.")))
    graph.add((npc_vocab, DCTERMS.title, Literal("The natural product taxonomony.")))
    graph.add((npc_vocab, VANN.preferredNamespacePrefix, Literal("npc")))
    graph.add((npc_vocab, VANN.preferredNamespaceUri, Literal(NPC)))
    graph.add((URIRef(prefix + "UNKNOWN"), RDF.type, SKOS.Concept))
    graph.add((npc_class, RDFS.subClassOf, SKOS.Concept))
    graph.add((npc_superclass, RDFS.subClassOf, SKOS.Concept))
    graph.add((npc_pathway, RDFS.subClassOf, SKOS.Concept))
    graph.add((npc_class, RDFS.label, Literal("Natural product class")))
    graph.add((npc_class, RDFS.comment, Literal("The Superclasses are subdivided into Classes that represent specific"
                                                " compound families (e.g., erythromycins, penicillins, or cannabinoids),"
                                                " characteristic functional groups (e.g., chromones, azaphilones, indole"
                                                " alkaloids, or 3-spiro tetramic acids), or scaffold diversity within"
                                                " a Superclass (e.g., flavans, flavones, and chalcones from flavonoids).")))
    graph.add((npc_superclass, RDFS.label, Literal("Natural product superclass")))
    graph.add((npc_superclass, RDFS.comment, Literal("The Superclasses represent subcategories within the Pathways."
                                                     " The categories in the Superclass originate from the general "
                                                     "classes of metabolites (e.g., flavonoids, meroterpenoids, or"
                                                     " steroids), the general chemical or molecular shapes (e.g.,"
                                                     " chromanes, phloroglucinols, or macrolides), or biosynthetic"
                                                     " information (e.g., tryptophan alkaloids, aromatic polyketides,"
                                                     " or pseudo alkaloids).")))
    graph.add((npc_pathway, RDFS.label, Literal("Natural product pathway")))
    graph.add((npc_pathway, RDFS.comment, Literal("The highest level of a hierarchical chemical structure "
                                                  "classification such as those defined with the NPClassifier,"
                                                  " a deep-learning tool for the automated structural classification "
                                                  "of natural products (NP) from their counted Morgan fingerprints."
                                                  " The Pathways of NPClassifier consist of seven categories:"
                                                  " fatty acids, polyketides, shikimates–phenylpropanoids,"
                                                  " terpenoids, alkaloids, amino acids/peptides, and carbohydrates.")))
    return graph


if __name__ == '__main__':
    subtaxonomy_list = get_subtaxonomy_list("npc-taxonomy.json")
    graph = generate_rdf_graph(subtaxonomy_list, "https://purl.org/npc#")
    graph.serialize(format='turtle', destination="./npc_taxonomy.ttl")
