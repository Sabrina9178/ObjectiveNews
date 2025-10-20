# Objective News Website
A workflow that leverages generative AI and clustering to produce **objective and unbiased** news summaries from multiple media outlets.

### Project Overview
Many news outlets today report with inherent bias, often presenting only a single perspective to influence audience opinions.

This project aims to provide a **neutral, multi-perspective alternative** through the Objective News Website, supported by an end-to-end framework for generating unbiased reports.

### Workflow
Data Collection -> Text preprocessing → Embedding → Clustering → News Generation → Keyword Generation → Sentiment Analysis → Deployment

### Technical Detail
#### Data Collection
Automated news collection using **Python (Selenium)** from multiple websites with diverse political orientations.
- **Sources**: SETN, FTV, PTS, CNA, ETtoday, TVBS
- **Daily Volume**: ~2200 articles
- **Collected data**: included news topic, content, date, and source link

#### Data Processing
- **Text preprocessing**: Standardized raw text data using **regular expressions** to remove URLs, ads, emojis, slogans...etc.
- **Embedding**: Transformed textual data into vector representations using Chinese-compatible embedding models.

#### Clustering: 
Grouped related articles into event-based clusters.
  - **Algorithms**: **KMeans and DBSCAN**, with iterative parameter tuning to optimize clustering.
  - **Input**: embeddings of news titles.
  - **Average clusters**: approximately 100 clusters per day, excluding clusters with fewer than 3 articles.

#### Objective News Generation
Generated neutral, multi-perspective reports using the **GPT API** with event clusters and tailored prompts.
- **Model**: GPT-4 Turbo (gpt-4-0125-preview)
- **Parameters**:
  - `temperature = 0.5`
  - `frequency_penalty = 0.2`
- **Tasks/Prompt**:
  - Filter out unrelated news within each cluster.
  - Generate objective and neutral news titles, content, keywords, and categories.
  - Detect opposing perspectives in the content and summarize their arguments.
  
#### Keyword Generation
- **Word Segmentation**: CKIP word segmentation model
- **POS Tagging**: CKIP part-of-speech (POS) tagging model
- **Keyword Extraction**: CKPE (Chinese Keyphrase Extractor)
  
#### Sentiment Analysis
Applied sentiment evaluation to ensure neutrality and reduce emotional bias.
- **Regeneration**: Triggered if neutral score < 50%, up to 3 retries.

#### Deployment
- **Platform**: WordPress ([Objective News Website](https://fao.zcr.mybluehost.me/))

### Future Improvements
- **Fake News Filtering and Review**: Integrate post-review with fact-checking reports and mark verified articles.
- **News Timeline**: Present chronological timelines for news stories on the same topic.
- **International News Sources**: Expand data collection to global news outlets.
- **Real-Time Streaming Pipeline**: Implement streaming-based ingestion for real-time updates.

### Resources
- [Objective News Website](https://fao.zcr.mybluehost.me/) : Presentation website showcasing the generated news.
- [ClusterToGenerate Notebook](https://colab.research.google.com/drive/1CetUiQ4Qs3dJnFY0FNgo7MPOfQTU_r4F?usp=sharing) : End-to-end Colab notebook including preprocessing, clustering, and exporting generated data to .csv.
- [News Scraping Script](news_scraping) : Scripts for scraping English and Chinese news Websites
- [Example Data](example_data):
  - [Raw Data](example_data/raw_data): 24-hour scraped news articles
  - [Clustered Data](example_data/clustered_data): Results of clustering news articles by event
  - [Generated News](example_data/generated_news): Generated news articles including title, content, keywords, and category
