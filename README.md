# Earth Metabolome Semantic Model
The first version of a draft of the Earth Metabolome semantic model is available in [`em.ttl`](em.ttl) that can replace the enpkg vocabulary. This model should import the [Natural Product taxonomy](#Natural_Product_taxonomy) described below. 

## Natural Product taxonomy
The [`npc_taxonomy.ttl`](npc_taxonomy.ttl) file is an SKOS-based OWL ontology for the structural classification of natural products derived from the [NPClassifier tool](https://pubs.acs.org/doi/10.1021/acs.jnatprod.1c00399). This OWL ontology was generated with the script in [`scripts`](scripts/natural_product_taxonomy).

This taxonomy is structured with the [SKOS vocabulary](https://www.w3.org/TR/skos-reference). `skos:broder` is used to represent the hierarchy among `Class`es, `Superclass`es and `Pathway`s.  `npc:Class`, `npc:Superclass` and `npc:Pathway` are subclasses of `skos:Concept`. `rdfs:label` is assigned for each term of the taxonomy that are instances of one of the subclasses of `skos:Concept`.

## Spectrum annotation provenance
To describe annotation provenace (i.e., information source), we are importing and applying the [PROV-Ontology](https://www.w3.org/TR/prov-o/) (a W3C reccomendantion).

`emi:SpectrumAnnotation` may assing the belown PROV-O properties:
`prov:wasAttributedTo` (range `prov:Agent`)
`prov:wasDerivedFrom`  (range `emi:InformationSource`)


# Organising Sample and Observation data

## Overview

As a suggestion, we can apply the [SOSA ontology](https://www.w3.org/TR/vocab-ssn/) as a data schema for struturing the Sample and Observation data. SOSA (Sensor, Observation, Sample, and Actuator) is a subset of SSN (Semantic Sensor Network Ontology) that is a W3C recommendation. Although the SSN  was developed with ontology engineers in mind as the primary audience. They addressed changes in scope and audience that currently also includes  scientific observations that may make heavy use of sampling strategies, and, therefore, the Sampling, Sampler, and Sample classes, as well as their corresponding properties, have been added to SOSA and SSN. 

## Data modelling proposal
Below, we show a concrete suggestion of how we could use this ontology for the EMI use case.

### Actuator-Sensor
We consider a Mass Spectrometer as a sosa:Platform. We interpret the MS detector that belongs to a Mass Spectrometer as being a Sensor. This sensor (a MS detector) is able to make an obervation by observing a Mass Spectrum (recommendation: to use the [CHMO controlled vocabulary]( http://purl.obolibrary.org/obo/CHMO_0000806)  as instances of the sosa:ObservableProperty).  Note that if we do not want to capture the equipment (Mass Spectrometer for provenance) of the generated LCMS analysis we can ignore/ommit them. The observation is interpreted as a [prov:Activity](https://www.w3.org/TR/prov-o/#Activity)/[sosa:Observation](https://www.w3.org/TR/vocab-ssn/#Observation)/emi:Analysis (the Analysis as defined in the Earth Metabolome Intiative model). This observation (aka LCMS Analysis) uses (prov:use/sosa:hasFeatureOfInterest) some sample. This sample comes from some emi:System (e.g. species or we can detail more here to be another sample like a Raw Material, a broader specimen). In addition, the LCMS analysis uses a Procedure (we can detail here the parameters etc used in the analysis). Finally, we can classify each Specimen by using some Specimen taxonomy such as in https://isamplesorg.github.io/models/generated/vocabularies/specimenType.html that relies on SKOS, similar to our other taxonomies in the project (NPClassifier) !

Moreover, we can also classify a sample with an external material taxonomy https://isamplesorg.github.io/models/generated/vocabularies/materialType.html#organicmaterial. All EMI model classes related to samples are subclasses of sosa:Sample, notably  emi:BlankSample, emi:ExtractSample and emi:QualityControlSample. 

```mermaid
graph TD
	d[":Mass-Spectrometer-A"]-->|rdf:type|sosa:Platform
	d-->|sosa:hosts|samp["Sampler-A"]
	d-->|sosa:hosts|d2["Detector-A"]
	d2-->|rdf:type|sosa:Sensor
	d2-->|sosa:observes|pp["<a href='http://purl.obolibrary.org/obo/CHMO_0000806'>a Mass Spectrum</a>"]
	d2-->|sosa:madeObservation|oo["LCMS Analysis"]
	d-->|sosa:hosts|act["Actuator-A"]
	act-->|rdf:type|sosa:Actuator
	act-->|sosa:madeActuation|oo["LCMS Analysis"]
	oo-->|sosa:hasResult|res["Mass_Spectrometry_results"]
	oo-->|sosa:resultTime|xsd:dateTime
        oo-->|rdf:type|a["prov:Activity, sosa:Observation,<br/> sosa:Actuation, emi:Analysis"]
        oo-->|"sosa:hasFeatureOfInterest -> prov:used"|s["Aliquot-S1"]
        s-->|rdf:type|aliq["sosa:Sample <- emi:Aliquot"]
        s-->|sosa:isSampleOf|t["Extract-sample-S1"]
        t-->|sosa:isSampleOf|rs["Raw-Sample-R1"]
	rs-->|rdf:type|emi:RawMaterial
	rs-->|sosa:isSampleOf|sys["System-S1"]
	sys-->|rdf:type|sosa:System
        t-->|"emi:isClassifiedWith (optional)"|w2["Specimen Type Vocabulary"]
        oo-->|sosa:usedProcedure|proc["Mass_Spectrometry_Analysis_Procedure"]
        proc-->|rdf:type|sosa:Procedure
```

The raw material (emi:RawMaterial) is also a sample/specimen. In case it is needed to describe the "Mass Spectrometer" as a sampler too, we can use the  sosa:Sampler class to define it as suggested below. (:Sampler-A) hosted by the :Mass-Spectrometer-A makes the sampling that resuts on subsamples (emi:Aliquot). The extract sample can be classified with an external taxonomy [such as the Specimen taxonomy ](https://isamplesorg.github.io/models/generated/vocabularies/specimenType.html) with the term emi:isClassifiedWith .

```mermaid
graph TD
	d[":Mass-Spectrometer-A"]-->|rdf:type|sosa:Platform
	d-->|sosa:hosts|d2["Sampler-A"]
	d2-->|rdf:type|sosa:Sampler
	d2-->|sosa:madeSampling|oo["Sampling-S1"]
        oo-->|rdf:type|a["sosa:Sampling"]
        oo-->|"sosa:hasFeatureOfInterest -> prov:used"|s["Extract-S1"]
        oo-->|sosa:hasResult|es1["Aliquot-S1"]
	es1-->|rdf:type|emi:Aliquot
        s-->|rdf:type|sSample["sosa:Sample, emi:ExtractSample"]
        s-->|sosa:isSampleOf|t["Extract-S0"]
	t-->|rdf:type|emi:ExtractSample
        oo-->|sosa:usedProcedure|proc["Sampling-procedure-S1"]
        proc-->|rdf:type|sosa:Procedure   

```

Detailed modelling of EMI actions



### Schema of an EMI Observation procedure

```mermaid
graph TD

		Camera-A -->|rdf:type|sosa:Sensor
		Camera-A -->|sosa:madeObservation|Field_Observation["Field_Observation"]
		Camera-A -->|sosa:observes|Pictures["Pictures"]
    Field_Observation -->|rdf:type|sosa:Observation["sosa:Observation"]
    Field_Observation -->|sosa:observedProperty|Pictures["Pictures"]
    Pictures --> |rdf:type|sosa:Observable_property["sosa:ObservableProperty"]
    Field_Observation -->|sosa:usedProcedure|Observation_Procedure["Observation_Procedure"]
    Field_Observation -->|sosa:resultTime|xsd:dateTime
    Field_Observation -->|"sosa:hasFeatureOfInterest"|o_a["System-1"]
    Field_Observation -->|sosa:hasResult|iNaturalist_Observation["iNaturalist_Observation"]
    o_a-->|rdf:type|emi:System
    o_a-->|sosa:hasSample|org["a Subsystem"]
    org-->|sosa:isSampleOf|o_a

   org-->|rdf:type|os["emi:System, sosa:Sample"]
```

### Schema of an EMI Collection procedure

```mermaid
graph TD

		Collector -->|rdf:type|sosa:Sampler
		Collector -->|sosa:madeSampling|Field_Sampling["Field_Sampling"]
    Field_Sampling -->|rdf:type|sosa:Sampling["sosa:Sampling"]
    Field_Sampling -->|sosa:usedProcedure|Sampling_Procedure["Sampling_Procedure"]
    Field_Sampling -->|sosa:resultTime|xsd:dateTime
    Field_Sampling -->|"sosa:hasFeatureOfInterest"|System["System-1"]
    Field_Sampling -->|sosa:hasResult|Field_Sample["Raw-Sample-R1"]
    Field_Sample -->|"emi:isClassifiedWith (optional)"|w2["Specimen Vocabulary"]
```
## Deprecated data modelling patterns
###  Schema of an EMI Extraction procedure (DEPRECATED)
(DEPRECATED: the same patterns from previous section can be applied by replacing the collector with the extractor. The extraction procedure is also a sampling procedure (i.e., it transforms one sample into another).
```mermaid
graph TD

		Extractor -->|rdf:type|sosa:Actuator
		Extractor -->|sosa:madeActuation|Lab_Extraction["Lab_Extraction"]
    Lab_Extraction -->|rdf:type|sosa:Actuation["sosa:Actuation"]
    Lab_Extraction -->|sosa:usedProcedure|Lab_Extraction_Procedure["Lab_Extraction_Procedure"]
    Lab_Extraction -->|sosa:resultTime|xsd:dateTime
    Lab_Extraction -->|"sosa:hasFeatureOfInterest"|Field_Sample["Field_Sample"]
    Lab_Extraction -->|sosa:hasResult|Lab_Extract["Lab_Extract"]
```


### Schema of an EMI Mass Spectrometry analysis procedure (DEPRECATED)
DEPRECATED - Please refer to [Actuator/Sensor modelling](#Actuator-Sensor)

```mermaid
graph TD

		Mass_Spectrometer -->|rdf:type|MS_Actuator["sosa:Actuator"]
		Mass_Spectrometer -->|rdf:type|MS_Sampler["sosa:Sampler"]
		Mass_Spectrometer -->|sosa:madeActuation|Mass_Spectrometry_Analysis["Mass_Spectrometry_Analysis"]
		Mass_Spectrometer -->|sosa:madeSampling|Mass_Spectrometry_Analysis["Mass_Spectrometry_Analysis"]
    Mass_Spectrometry_Analysis -->|rdf:type|MS_Actuation["sosa:Actuation"]
    Mass_Spectrometry_Analysis -->|sosa:usedProcedure|Mass_Spectrometry_Analysis_Procedure["Mass_Spectrometry_Analysis_Procedure"]
    Mass_Spectrometry_Analysis -->|sosa:resultTime|ms_time["xsd:dateTime"]
    Mass_Spectrometry_Analysis -->|"sosa:hasFeatureOfInterest"|Lab_Extract["Lab_Extract"]
    Mass_Spectrometry_Analysis -->|sosa:hasResult|Mass_Spectrometry_Results["Mass_Spectrometry_Results"]

```


### Schema of an EMI overall procedure (DEPRECATED)


```mermaid

graph TD

    subgraph field
    
    subgraph collection
		Collector -->|rdf:type|sosa:Sampler
		Collector -->|sosa:madeSampling|Field_Sampling["Field_Sampling"]
    Field_Sampling -->|rdf:type|sosa:Sampling["sosa:Sampling"]
    Field_Sampling -->|sosa:usedProcedure|Sampling_Procedure["Sampling_Procedure"]
    Field_Sampling -->|sosa:resultTime|fs_time["xsd:dateTime"]

    end 

    subgraph observation
		Smartphone -->|rdf:type|sosa:Sensor
		Smartphone -->|sosa:madeObservation|Field_Observation["Field_Observation"]
		Smartphone -->|sosa:observes|Pictures["Pictures"]
    Field_Observation -->|rdf:type|sosa:Observation["sosa:Observation"]
    Field_Observation -->|sosa:observedProperty|Pictures["Pictures"]
    Pictures --> |rdf:type|sosa:Observable_property["sosa:Observable_property"]
    Field_Observation -->|sosa:usedProcedure|Observation_Procedure["Observation_Procedure"]
    Field_Observation -->|sosa:resultTime|fo_time["xsd:dateTime"]
    Field_Observation -->|sosa:hasResult|iNaturalist_Observation["iNaturalist_Observation"]

    end

    Field_Observation -->|"sosa:hasFeatureOfInterest"|Living_System["Living_System"]
    Field_Sampling -->|"sosa:hasFeatureOfInterest"|Living_System["Living_System"]
    Living_System -->|skos:narrower|t_a["ex:Taxon_a"]
    Living_System -->|skos:narrower|t_b["ex:Taxon_b"]

    end
    
    Lab_Extraction -->|"sosa:hasFeatureOfInterest"|Field_Sample["Field_Sample"]
    t_a -->|rdf:type|w["<a href=http://www.wikidata.org/entity/Q16521>wikidata:Q16521</a>"]
    t_b -->|rdf:type|w["<a href=http://www.wikidata.org/entity/Q16521>wikidata:Q16521</a>"]
    t_a -->|"emi:isClassifiedWith (optional)"|w2["Specimen Type Vocabulary"]
    t_b -->|"emi:isClassifiedWith (optional)"|w2["Specimen Type Vocabulary"]

    Field_Sampling -->|sosa:hasResult|Field_Sample["Field_Sample"]

    subgraph lab


    direction TB
    subgraph mass_spectrometry
		Mass_Spectrometer -->|rdf:type|MS_Actuator["sosa:Actuator"]
		Mass_Spectrometer -->|rdf:type|MS_Sampler["sosa:Sampler"]
		Mass_Spectrometer -->|sosa:madeActuation|Mass_Spectrometry_Analysis["Mass_Spectrometry_Analysis"]
		Mass_Spectrometer -->|sosa:madeSampling|Mass_Spectrometry_Analysis["Mass_Spectrometry_Analysis"]
    Mass_Spectrometry_Analysis -->|rdf:type|MS_Actuation["sosa:Actuation"]
    Mass_Spectrometry_Analysis -->|sosa:usedProcedure|Mass_Spectrometry_Analysis_Procedure["Mass_Spectrometry_Analysis_Procedure"]
    Mass_Spectrometry_Analysis -->|sosa:resultTime|ms_time["xsd:dateTime"]
    Mass_Spectrometry_Analysis -->|sosa:hasResult|Mass_Spectrometry_Results["Mass_Spectrometry_Results"]
    end

    subgraph extraction
		Extractor -->|rdf:type|sosa:Actuator
		Extractor -->|sosa:madeActuation|Lab_Extraction["Lab_Extraction"]
    Lab_Extraction -->|rdf:type|sosa:Actuation["sosa:Actuation"]
    Lab_Extraction -->|sosa:usedProcedure|Lab_Extraction_Procedure["Lab_Extraction_Procedure"]
    Lab_Extraction -->|sosa:resultTime|xsd:dateTime
    Lab_Extraction -->|sosa:resultTime|le_time["xsd:dateTime"]

    end

    Lab_Extraction -->|sosa:hasResult|Lab_Extract["Lab_Extract"]
    Mass_Spectrometry_Analysis -->|"sosa:hasFeatureOfInterest"|Lab_Extract["Lab_Extract"]

    end

```


