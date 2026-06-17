# RIT Math Professor Unofficial Guide

## Domain
This project builds a RAG system for RIT Mathematics Department professor reviews sourced from Rate My Professors. Official RIT channels provide no insight into teaching style, grading difficulty, or exam structure — students rely entirely on word of mouth. This system makes that informal knowledge searchable and answerable.

## Document Sources
1. documents/prof_agyingi_rmp.txt — Rate My Professors reviews for Prof. Agyingi
2. documents/prof_timberlake_rmp.txt — Rate My Professors reviews for Prof. Timberlake
3. documents/prof_shahmohamad_rmp.txt — Rate My Professors reviews for Prof. Shahmohamad
4. documents/prof_young_rmp.txt — Rate My Professors reviews for Prof. Young
5. documents/prof_lopez_rmp.txt — Rate My Professors reviews for Prof. Lopez
6. documents/prof_maki_rmp.txt — Rate My Professors reviews for Prof. Maki
7. documents/prof_prevendoski_rmp.txt — Rate My Professors reviews for Prof. Prevendoski
8. documents/prof_allan_rmp.txt — Rate My Professors reviews for Prof. Allan
9. documents/prof_diute_rmp.txt — Rate My Professors reviews for Prof. Diute
10. documents/prof_harkin_rmp.txt — Rate My Professors reviews for Prof. Harkin

## Chunking Strategy
- Chunk size: 300 characters
- Overlap: 50 characters
- Reasoning: RMP reviews are short (1–4 sentences each). A 300-character chunk captures roughly one complete student opinion without merging unrelated reviews. The 50-character overlap ensures opinions that span chunk boundaries still appear in at least one retrievable chunk.

## Sample Chunks

Chunk 1 (from prof_timberlake_rmp.txt):
"MATH182 May 3rd, 2026 For Credit: Yes Attendance: Mandatory Grade: Not sure yet Textbook: N/A You entire grade in the course is essentially just the sum of 4 tests."

Chunk 2 (from prof_timberlake_rmp.txt):
"TOUGH GRADER LOTS OF HOMEWORK GRADED BY FEW THINGS Thumbs up 0 Thumbs down 0 QUALITY 3.0 DIFFICULTY 2.0 MATH181 Jan 7th, 2026"

Chunk 3 (from prof_timberlake_rmp.txt):
"Professor Timberlake confuses me. She seems to genuinely care about her students success, and encourages questions, but then sounds offended any time someone gets anything wrong."

Chunk 4 (from prof_timberlake_rmp.txt):
"Requires WebAssign/Cengage. CARING LECTURE HEAVY ACCESSIBLE OUTSIDE CLASS Thumbs up 0 Thumbs down 0 QUALITY 1.0 DIFFICULTY 5.0 DISC131"

Chunk 5 (from prof_timberlake_rmp.txt):
"She'll take points off on tests if she doesn't like you. She probably won't even have a valid reason for disliking you. Also, she can be really condescending when you ask questions."

## Embedding Model
Model: all-MiniLM-L6-v2 via sentence-transformers (runs locally, no API key needed)

Production tradeoffs: For a real deployment I would consider OpenAI's text-embedding-3-small for higher accuracy on domain-specific text, but it costs money per token. If multilingual support were needed (international students reviewing in other languages), paraphrase-multilingual-MiniLM-L12-v2 would be worth the tradeoff. Context length is not a concern here since chunks are short (300 chars).

## Retrieval Test Results

Query 1: "What do students say about Professor Agyingi's teaching style?"
Top chunks returned from prof_agyingi_rmp.txt. Relevant because they contain direct student opinions about Agyingi's classroom behavior, pacing, and personality.

Query 2: "Is Professor Timberlake difficult?"
Top chunks returned from prof_timberlake_rmp.txt. Relevant because they contain difficulty ratings and student comments about workload and grading.

Query 3: "Which RIT math professor is the most lenient grader?"
Top chunks returned from prof_harkin_rmp.txt, prof_prevendoski_rmp.txt, prof_agyingi_rmp.txt, prof_shahmohamad_rmp.txt. Relevant because they contain grading-related language, though no chunk explicitly names the leniency comparison across professors.

## Grounded Generation
Grounding is enforced via the system prompt passed to Groq's llama-3.3-70b-versatile:
"Answer the question using ONLY the information provided in the documents below. If the documents don't contain enough information to answer, say 'I don't have enough information on that.' Do not use any outside knowledge."
Source attribution is added programmatically by appending the source filenames of all retrieved chunks to every response.

## Example Responses

Example 1 — Agyingi teaching style (accurate, grounded):
Q: "What do students say about Professor Agyingi's teaching style?"
A: "Students have varying opinions about Professor Agyingi's teaching style. Some students have praised him, saying that he is a great teacher who makes everything clear, never assumes the class knows anything, and is fair. Additionally, some students have noted that he teaches and explains things very quickly, but makes sure everyone understands before moving on."
Source: prof_agyingi_rmp.txt

Example 2 — Lopez recommendation (accurate, grounded):
Q: "Would students recommend Professor Lopez?"
A: "It's mixed. Some students would recommend Professor Lopez, as they find him to be a great professor, extremely smart, and always accessible outside of class. However, others mention that his lectures can be disorganized and hard to follow."
Source: prof_lopez_rmp.txt

Out-of-scope query:
Q: "What is the best dining hall at RIT?"
A: "I don't have enough information on that."
Source: prof_shahmohamad_rmp.txt (retrieval pulled closest match but LLM correctly refused to answer)

## Query Interface
Input: a text box labeled "Your question"
Output: two text boxes — "Answer" (the grounded LLM response) and "Sources" (list of source .txt files)
To run: python3 app.py, then open http://127.0.0.1:7860

Sample interaction:
User: "Is Professor Timberlake's class considered difficult?"
System: "Yes, Professor Timberlake's class is considered difficult by some students. The difficulty level is rated as 4.0 out of 5.0 in one of the reviews, and another review mentions that the coursework is challenging."
Sources: prof_timberlake_rmp.txt

## Evaluation Report

| # | Question | Expected Answer | System Response | Accuracy |
|---|----------|----------------|-----------------|----------|
| 1 | What do students say about Professor Agyingi's teaching style? | Caring, accessible, good at explaining | Detailed response about being fair, clear, fast-paced but thorough | Accurate |
| 2 | Is Professor Timberlake's class considered difficult? | Yes, considered difficult | Yes, rated 4.0/5.0 difficulty, challenging coursework | Accurate |
| 3 | Would students recommend Professor Lopez? | Mixed reviews | Mixed — smart and accessible but disorganized lectures | Accurate |
| 4 | What do students say about Professor Shahmohamad's exams? | Well-structured and fair | "Well-structured and fair" | Accurate |
| 5 | Which RIT math professor is considered the most lenient grader? | Should identify a specific professor | Could not name a specific professor | Partially Accurate |

## Failure Case
Question 5 ("Which RIT math professor is considered the most lenient grader?") returned a partially accurate response. The system retrieved relevant chunks containing grading language from multiple professors, but the chunks did not include the professor's name alongside the grading description — the RMP raw text stores review text and metadata in separate parts of the page, and my chunking split them apart. As a result, the LLM had grading opinions but no professor names to attach them to, and correctly refused to guess. This is a chunking boundary failure: the professor's name and the review content ended up in different chunks, so retrieval returned the opinion without the identity.

## Spec Reflection
The spec helped most during chunking — deciding on 300 characters with 50 overlap before writing any code forced me to think about what a "good chunk" looks like for short review text, which made the implementation straightforward. One divergence: the spec anticipated cleaner source documents, but the raw RMP text included UI elements (ratings, dates, "Thumbs up 0") mixed into the review text. The cleaning step had to be more aggressive than planned, though some noise still remains in the chunks.

## AI Usage
1. Claude generated the full ingest.py script from the chunking strategy section of planning.md. I reviewed the output and confirmed the chunk size and overlap matched the spec before running it.
2. Claude generated embed.py and app.py from the retrieval approach and grounding requirements. I ran both scripts, debugged a missing module error (chromadb not found in venv), and verified retrieval results before adding generation.