# Webis-QInC-22

The Webis Query Interpretation Corpus 2022 (Webis-QInC-22) contains manually selected explicit entities, implicit entities and entity based interpretations for 2,800 web queries. These web queries were either obtained from existing entity linking datasets or ambiguity queries from various sources.

## Directory structure

```
webis-qinc-22.zip           
|
| - evaluation                  # Evaluation logs based on the datasets test split
|   |
|   | - exer                    # Evaluation logs of explicit entity recognition
|   |
|   | - interpretation          # Evaluation logs of query interpretation
|
| - test                        # Test split of dataset
| 
| - train                       # Training split of dataset
|
| - webis-qinc-22.json          # Whole dataset
```

## Dataset file structure

All dataset files are provided in JSON format with the following fields.

### Query

* <code>id</code>
  * Internal id of the query 
  * Concatenation of origin corpus and original id
* <code>query</code>
  * Query text
* <code>difficulty</code>
  * Query difficulty in the range 1-5
* <code>categories</code>
  * Array of assigned categories
    * Categorical queries (CatQ)
    * Conceptual queries (ConQ)
    * Question queries (QQ)
    * Relational queries (RQ)
    * Surface queries (SurQ)
    * Solutional entity query (SolEnQ) (queries with an entity as "answer")
* <code>explicit_entities</code>
  * Array of explicit entities (cf. [Entity](#entity))
* <code>implicit_entities</code>
    * Array of implicit entities (cf. [Entity](#entity))
* <code>related_entities</code>
  * Array of related entities (cf. [Entity](#entity))
* <code>interpretations</code>
  * Array of entity-based interpretatations (cf. [Interpretation](#interpretation))

### Entity

* <code>mention</code>
  * textual excerpt from the query text
* <code>entity</code>
  * array of urls from referred entities
  * multiple coherent entities can be referred by a single mention
* <code>relevance</code>
  * relevance assessment in range 1-2

### Interpretation

* <code>id</code>
  * local numeric id in the scope of a single query
* <code>interpretation</code>
  * array containing all parts of an interpretation (i.e., segments or entities)
* <code>relevance</code>
  * relevance assessments in range 1-3
* <code>equivalent</code>
  * local id of semantically equivalent interpretation (or null if there are none)
* <code>comment</code>
  * optional comment to clarify the described intent (or null if intent is clear)

## Cite

If you use this resource, kindly city the following article:

```
@InProceedings{kasturia:2022,
  author =                {Vaibhav Kasturia and Marcel Gohsen and Matthias Hagen},
  booktitle =             {15th ACM International Conference on Web Search and Data Mining (WSDM 2022)},
  doi =                   {10.1145/3488560.3498532},
  month =                 feb,
  publisher =             {ACM},
  site =                  {Tempe, AZ, USA},
  title =                 {{Query Interpretations from Entity-Linked Segmentations}},
  year =                  2022
}
```
You'll find additional information about this data in the article above. 