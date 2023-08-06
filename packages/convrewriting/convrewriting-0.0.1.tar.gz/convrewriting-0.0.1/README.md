## This is an official source code repository of the paper: Mele et al., Adaptive Utterance Rewriting for Conversational Search, IP&M, 2021.

### Authors: Ida Mele, Cristina Ioana Muntean, Franco Maria Nardini, Raffaele Perego, Nicola Tonellotto, Ophir Frieder.

Code: https://github.com/hpclab/adaptive-utterance-rewriting-conversational-search

## Data
- Datasets: CAsT 2019 dataset divided into training and test sets as specified in the paper. 


## Query resolution
The query resolution module uses both supervised and unsupervised methods for rewriting queries. 

For the supervised classification based rewriting run either of the following rewriting strategies "Standard", "Enriched", "LastSE", "First_and_Last_SE", "First_or_Last_SE":
```python
from convrewriting.supervised.pipeline_classification import rewrite_strategy

rewrite_strategy("Standard")
```


For the unsupervised based rewriting strategy run either of the following:
```python
from convrewriting.unsupervised.pipeline_nlp import rewrite_context, rewrite_first_topic, rewrite_topic_shift

rewrite_context()
rewrite_first_topic()
rewrite_topic_shift()
```

## Citation Licence

This source code is subject to the following citation license:

By downloading and using the source code stored in this GitHub repository, you agree to cite at the undernoted paper in any kind of material you produce where this code has been used to conduct search or experimentation, whether be it a research paper, dissertation, article, poster, presentation, or documentation. By using this software, you have agreed to the citation licence.

[Ida Mele, Cristina Ioana Muntean, Franco Maria Nardini, Raffaele Perego, Nicola Tonellotto, Ophir Frieder. 2021. Adaptive Utterance Rewriting in Conversational Search. Information Processing \& Management.](https://doi.org/10.1016/j.ipm.2021.102682)

```bibtex

@article{mele2021adaptive,
	title = {Adaptive Utterance Rewriting for Conversational Search},
	journal = {Information Processing \& Management},
	volume = {58},
	number = {6},
	pages = {102682},
	year = {2021},
	issn = {0306-4573},
	doi = {https://doi.org/10.1016/j.ipm.2021.102682},
	url = {https://www.sciencedirect.com/science/article/pii/S0306457321001679},
	author = {Ida Mele and Cristina Ioana Muntean and Franco Maria Nardini and Raffaele Perego and Nicola Tonellotto and Ophir Frieder},
}

```

## Contact Us
For any other question/comment, write us an email: {cristina.muntean@isti.cnr.it}

