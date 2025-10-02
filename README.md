# Objective News Website
A workflow that leverages generative AI and clustering techniques to produce **objective and unbiased** news summaries from multiple media outlets.

### Project Overview
Many news outlets today report with inherent bias, often presenting only a single perspective to influence audience opinions.

This project aims to provide a **neutral, multi-perspective alternative** through the Objective News Website, supported by an end-to-end framework for generating unbiased reports.

### Workflow
- **Web scraping**: Automated news collection using **Python (Selenium)** from multiple websites with diverse political orientations.
- **Text preprocessing**: Standardized raw text data using **regular expressions**.
- **Vector embeddings**: Converted textual data into vector representations.
- **clustering**: Grouped related articles into event-based clusters.
- **Generative AI**:
  - Generated neutral, multi-perspective reports using the **GPT API** with event clusters and tailored prompts.
  - Produced outputs including titles, content, arguments from different perspectives, keywords, and categories.
- **Sentiment analysis**: Applied sentiment evaluation to ensure neutrality and reduce emotional bias.
- **Presentation**: Deployed results to a **WordPress-based news platform**.

### Technical Detail
#### Data Collection
- **Language**: Python
- **Library**: Selenium
- **Format**: HTML scraping
- **Sources**: SETN, FTV, PTS, CNA, ETtoday, TVBS
- **Daily Volume**: ~2200 articles

#### Data Processing
- **Preprocessing**: Regex-based cleaning (remove URLs, ads, emojis, slogans, redundant whitespace)
- **Embedding**: Chinese-compatible embedding models
- **Clustering**: KMeans, DBSCAN (iteratively tested combinations)
  - Input: article titles + content embeddings
  - Average clusters: ~100 per day after filtering


#### Objective News Generation
- **Model**: GPT-4 Turbo (gpt-4-0125-preview)
- **Parameters**:
  - `temperature = 0.5`
  - `frequency_penalty = 0.2`
- **Process**:
  1. Filter unrelated articles
  2. Identify multiple perspectives & arguments
  3. Generate objective, structured news in Traditional Chinese

#### Neutrality Check
- **Sentiment analysis model** ensures neutrality
- If `neutral score < 50%`, regeneration is triggered (up to 3 retries)

#### Keyword & Category Generation
- Tokenization + POS filtering
- GPT-based keyword generation

#### Deployment
- **Platform**: WordPress (Objective News site)
- **Publishing Workflow**: CSV → Plugin → Website

### Future Improvements
- **Fake News Filtering and Review**:
  Integrate post-review using reports from fact-checking organizations, and mark verified articles directly on the website.
- **News Timeline**:
  Organize and present chronological timelines for news stories on the same topic.
- **International News Sources**:
  Expand data collection beyond Taiwan to include global news outlets.
- **Real-Time Streaming Pipeline**:
  Build a streaming-based ingestion pipeline for real-time news updates.

### Resources
- [Objective News Website](https://fao.zcr.mybluehost.me/)
- [ClusterToGenerate Notebook](https://colab.research.google.com/drive/1CetUiQ4Qs3dJnFY0FNgo7MPOfQTU_r4F?usp=sharing)

### Repository Structure
news_scraping/

  ├── ch_news/          # Raw news data in Chinese
  
  └── en_news/          # Raw news data in English

ClusterToGenerate.ipynb   # Colab notebook for preprocessing, clustering, and news generation

example_data/

  ├── raw_data/          # 24-hour scraped news articles

  ├── clustered_data/    # Results of clustering news articles by event

  └── generated_news/    # Generated news articles including title, content, keywords, and category
