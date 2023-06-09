# Earth Metabolome Semantic Model
The first version of a draft of the Earth Metabolome semantic model is available in [`em.ttl`](em.ttl) that can replace the enpkg vocabulary. This model should import the [Natural Product taxonomy](#Natural_Product_taxonomy) described below. 

## Natural Product taxonomy
The [`npc_taxonomy.ttl`](npc_taxonomy.ttl) file is an OWL ontology for the structural classification of natural products derived from the [NPClassifier tool](https://pubs.acs.org/doi/10.1021/acs.jnatprod.1c00399). This OWL ontology was generated with the script in [`scripts`](scripts/natural_product_taxonomy).

This taxonomy is structured with the [SKOS vocabulary](https://www.w3.org/TR/skos-reference). `skos:broder` is used to represent the hierarchy among `Class`es, `Superclass`es and `Pathway`s.  `npc:Class`, `npc:Superclass` and `npc:Pathway` are subclasses of `skos:Concept`. `rdfs:label` is assigned for each term of the taxonomy that are instances of one of the subclasses of `skos:Concept`.






