# Project 1 Planning: The Unofficial Guide

## Domain
This guide covers student-generated reviews of RIT Mathematics Department professors, sourced from Rate My Professors. This knowledge is valuable because official RIT channels provide no insight into teaching style, grading difficulty, or exam structure — students rely entirely on word of mouth and informal reviews to make course decisions.

## Documents
| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Rate My Professors | Reviews for Prof. Agyingi | documents/prof_agyingi_rmp.txt |
| 2 | Rate My Professors | Reviews for Prof. Timberlake | documents/prof_timberlake_rmp.txt |
| 3 | Rate My Professors | Reviews for Prof. Shahmohamad | documents/prof_shahmohamad_rmp.txt |
| 4 | Rate My Professors | Reviews for Prof. Young | documents/prof_young_rmp.txt |
| 5 | Rate My Professors | Reviews for Prof. Lopez | documents/prof_lopez_rmp.txt |
| 6 | Rate My Professors | Reviews for Prof. Maki | documents/prof_maki_rmp.txt |
| 7 | Rate My Professors | Reviews for Prof. Prevendoski | documents/prof_prevendoski_rmp.txt |
| 8 | Rate My Professors | Reviews for Prof. Allan | documents/prof_allan_rmp.txt |
| 9 | Rate My Professors | Reviews for Prof. Diute | documents/prof_diute_rmp.txt |
| 10 | Rate My Professors | Reviews for Prof. Harkin | documents/prof_harkin_rmp.txt |

## Chunking Strategy
**Chunk size:** 300 characters
**Overlap:** 50 characters
**Reasoning:** Our documents are short student reviews — typically 1-4 sentences each. A 300-character chunk captures roughly one complete review without merging unrelated opinions from different students. Overlap of 50 characters ensures that if a key opinion spans a chunk boundary, it appears in at least one retrievable chunk. Larger chunks would merge multiple reviews and dilute specific opinions; smaller chunks would produce meaningless sentence fragments.

## Retrieval Approach
**Embedding model:** all-MiniLM-L6-v2 via sentence-transformers
**Top-k:** 5
**Production tradeoff reflection:** For a real deployment, I would consider OpenAI's text-embedding-3-small for higher accuracy on domain-specific text, but it costs money per token and requires an API key. all-MiniLM-L6-v2 runs locally with no cost or rate limits, making it ideal for this project. If multilingual support were needed (e.g. international students reviewing in other languages), a multilingual model like paraphrase-multilingual-MiniLM-L12-v2 would be worth the tradeoff. Context length is not a major concern here since our chunks are short.

## Evaluation Plan
| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do students say about Professor Agyingi's teaching style? | Students say Agyingi is caring, accessible outside class, and good at making sure students understand the material despite having a strong accent. |
| 2 | Is Professor Timberlake's class considered difficult? | Reviews should indicate whether Timberlake is regarded as easy, moderate, or hard based on student feedback. |
| 3 | Would students recommend Professor Lopez? | Reviews should reflect whether students would take Lopez again based on their RMP ratings and comments. |
| 4 | What do students say about Professor Shahmohamad's exams? | Reviews should describe exam difficulty, style, or grading approach based on student experience. |
| 5 | Which RIT math professor is considered the most lenient grader? | Based on reviews, the system should identify which professor students describe as easiest or most generous with grades. |

## Anticipated Challenges
1. **Noisy documents:** The raw RMP text includes ads, button labels, dates, and "Helpful 👍 0" UI text mixed in with real reviews. The cleaning step must strip this without removing actual review content.
2. **Chunk boundary splits:** A student opinion expressed across two sentences may get split across chunks, making retrieval return only half the context. The 50-character overlap partially mitigates this but may not catch all cases.

## AI Tool Plan
- **Ingestion + chunking (Milestone 3):** I will prompt Claude with this planning.md and ask it to generate an ingest.py script that loads all .txt files from the documents/ folder, cleans them, and splits them into 300-character chunks with 50-character overlap.
- **Embedding + retrieval (Milestone 4):** I will prompt Claude with the Retrieval Approach section and ask it to generate embed.py that embeds chunks using all-MiniLM-L6-v2 and stores them in ChromaDB, plus a retrieve() function that returns top-5 chunks for a query.
- **Generation + interface (Milestone 5):** I will prompt Claude with the grounding requirement and ask it to generate app.py using Gradio that takes a query, retrieves chunks, and returns a grounded answer with source attribution.

## Architecture
Document Ingestion (load .txt files from documents/)
        ↓
Chunking (300 chars, 50 char overlap)
        ↓
Embedding (all-MiniLM-L6-v2) + Vector Store (ChromaDB)
        ↓
Retrieval (top-5 semantic search)
        ↓
Generation (Groq llama-3.3-70b-versatile) → Grounded answer + source citation