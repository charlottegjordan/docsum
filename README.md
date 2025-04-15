# Docsum Project / Topic 10 Lab

My docsum.py file takes in a file path and calls on Groq to return a summary of the contents of the inputted file. The inputted file can be a txt file, a PDF, an HTML link or file, or an image link or file.


## Requirements
To get the necessary libraries, run this command:
```
$ pip3 install -r requirements.txt
```


## Instructions
You can use the function with the general formula ```python3 docsum.py filename```.

Here are some example cases:

```
$ python3 docsum.py docs/news-mx.html
The US Supreme Court has lifted the suspension of a 1798 law that allows President Trump to deport immigrants accused of being members of a criminal gang. The law was invoked by Trump to deport Venezuelans accused of being part of the "Tren de Aragua" gang, which is not recognized as a nation or entity by the US. The four dissenting judges argued that the law is illegal and allows for indefinite detention without due process, while the five majority judges allowed the deportation to proceed, citing the need to maintain national security.
```
```
$ python3 docsum.py docs/constitution-mx.txt
The Mexican Constitution of 1917 is a fundamental document that guarantees individual rights and freedoms, as well as the rights of indigenous peoples. It outlines the rights and obligations of citizens, including the right to education, health, housing, and a safe environment, and establishes the principles of due process and the protection of individual rights. The Constitution also regulates the government's powers, including the separation of powers, the electoral process, and the role of the judiciary, and establishes measures to ensure the swift and honest administration of agrarian justice.
```
```
$ python3 docsum.py docs/research_paper.pdf
The paper proposes DOCSPLIT, an unsupervised pretraining method for large document embeddings that takes into account the global context of a document. DOCSPLIT outperforms other pretraining methods on document classification, few-shot learning, and document retrieval tasks. The authors demonstrate DOCSPLIT's effectiveness on three downstream tasks, achieving significant improvements in macro-F1 scores compared to other models.
```
```
$ python3 docsum.py https://elpais.com/us/
The article covers various news topics, including the death of author Mario Vargas Llosa, the Trump administration's immigration policies, and the struggles faced by immigrants. The article also reports on the US economy, climate change, and popular culture, including the release of new music and movies. Overall, the article provides a snapshot of current events and trends in the United States and around the world.
```
```
$ python3 docsum.py https://www.cmc.edu/sites/default/files/about/images/20170213-cube.jpg
The image depicts a modern glass-walled building with a pool of water in front of it, surrounded by other buildings. The scene is illuminated in the evening or nighttime, with the pool reflecting the lights from the building and the sky. The overall setting is peaceful and modern, suggesting a corporate campus or luxury hotel.
```