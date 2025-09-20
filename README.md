# Objective News Website
A system that leverages generative AI and clustering techniques to produce **objective and unbiased** news summaries from multiple media outlets.

### 📌 Project Overview
Most news outlets report with inherent bias, often presenting only one perspective. To address this, Objective News aims to provide readers with a **neutral, fact-based alternative**.

The system collects articles from diverse media sources, clusters them by event, and uses **large language models (LLMs)** to generate objective news summaries. These summaries are then checked for neutrality before being published on the website.

### 🎯 Key Features
- Automated **news scraping** from multiple Taiwanese outlets with different political orientations.
- **Text preprocessing** to clean and standardize raw data.
- **Vector embeddings & clustering** to group related articles into event-based clusters.
- **Generative AI** to rewrite news into a neutral, fact-focused summary.
- **Sentiment analysis** to ensure objectivity and prevent emotional bias.
- Automatic generation of **keywords and categories** for publication.
- Deployment to a **WordPress-based news platform**.

### 🛠️ Tech Stack
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

### 🚀 Future Improvements
- **Fake News Filtering and Review**:
  Integrate post-review using reports from fact-checking organizations, and mark verified articles directly on the website.
- **News Timeline**:
  Organize and present chronological timelines for news stories on the same topic.
- **International News Sources**:
  Expand data collection beyond Taiwan to include global news outlets.
- **Real-Time Streaming Pipeline**:
  Build a streaming-based ingestion pipeline for real-time news updates.

### 🔗 Resources
- [Objective News Website](https://fao.zcr.mybluehost.me/)
- [ClusterToGenerate Notebook](https://colab.research.google.com/drive/1gQ8Ysw7PNyKP__XrN4ghtE3f8__rmKnK?usp=sharing)

### 📂 Repository Structure
├── NewsScraping/              # Web scraping scripts

├── ClusterToGenerate.ipynb     # Colab notebook for preprocessing, clustering, generation

├── models/                     # Saved clustering/embedding models

├── exampleData/                       # Raw and processed datasets

└── exampleOutput/                     # Generated news, categories, keywords
