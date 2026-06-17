# RIT Math Professor Unofficial Guide

## Domain
This project builds a RAG system for RIT Mathematics Department professor reviews sourced from Rate My Professors. Official RIT channels provide no insight into teaching style, grading difficulty, or exam structure — students rely entirely on word of mouth and informal reviews to make course decisions. This system makes that knowledge searchable and answerable with source citations.

## Document Sources
1. documents/prof_agyingi_rmp.txt — Rate My Professors reviews for Prof. Agyingi (67 reviews)
2. documents/prof_timberlake_rmp.txt — Rate My Professors reviews for Prof. Timberlake
3. documents/prof_shahmohamad_rmp.txt — Rate My Professors reviews for Prof. Shahmohamad
4. documents/prof_young_rmp.txt — Rate My Professors reviews for Prof. Young
5. documents/prof_lopez_rmp.txt — Rate My Professors reviews for Prof. Lopez
6. documents/prof_maki_rmp.txt — Rate My Professors reviews for Prof. Maki
7. documents/prof_prevendoski_rmp.txt — Rate My Professors reviews for Prof. Prevendoski
8. documents/prof_allan_rmp.txt — Rate My Professors reviews for Prof. Allan
9. documents/prof_diute_rmp.txt — Rate My Professors reviews for Prof. Diute
10. documents/prof_harkin_rmp.txt — Rate My Professors reviews for Prof. Harkin

All documents were collected manually from ratemyprofessors.com by searching each professor's name alongside "RIT."

## Chunking Strategy
- Chunk size: 300 characters
- Overlap: 50 characters
- Reasoning: RMP reviews are short (1–4 sentences each). A 300-character chunk captures roughly one complete student opinion without merging unrelated reviews from different students. The 50-character overlap ensures that opinions spanning a chunk boundary still appear in at least one retrievable chunk. Larger chunks would merge multiple reviews and dilute specific opinions; smaller chunks would produce meaningless sentence fragments with no standalone meaning.

## Sample Chunks

Chunk 1 (from prof_timberlake_rmp.txt):
"MATH182 May 3rd, 2026 For Credit: Yes Attendance: Mandatory Grade: Not sure yet Textbook: N/A You entire grade in the course is essentially just the sum of 4 tests. Other things are counted, but they make up a pitifully small section of the overall course grade."

Chunk 2 (from prof_timberlake_rmp.txt):
"TOUGH GRADER LOTS OF HOMEWORK GRADED BY FEW THINGS Thumbs up 0 Thumbs down 0 QUALITY 3.0 DIFFICULTY 2.0 MATH181 Jan 7th, 2026 For Credit: Yes Attendance: Mandatory Would Take Again: Yes Grade: A Textbook: Yes Professor Timberlake confus"

Chunk 3 (from prof_timberlake_rmp.txt):
"Professor Timberlake confuses me. She seems to genuinely care about her students success, and encourages questions, but then sounds offended any time someone gets anything wrong. She knows what she is talking about regarding math, though."

Chunk 4 (from prof_timberlake_rmp.txt):
"Requires WebAssign/Cengage. CARING LECTURE HEAVY ACCESSIBLE OUTSIDE CLASS Thumbs up 0 Thumbs down 0 QUALITY 1.0 DIFFICULTY 5.0 DISC131 Dec 9th, 2025 For Credit: Yes Attendance: Mandatory Grade: Not sure yet Textbook: N/A She'll take points"

Chunk 5 (from prof_agyingi_rmp.txt):
"Professor Agyingi is great!!! He is really fair and if you want to learn math take him. His accent is sometimes difficult to understand but you get used to it. He is very caring and always willing to help students outside of class."

## Embedding Model
Model: all-MiniLM-L6-v2 via sentence-transformers (runs locally, no API key, no rate limits)

Production tradeoff reflection: For a real deployment I would weigh several factors. Cost: all-MiniLM-L6-v2 is free and runs locally, while OpenAI's text-embedding-3-small costs per token but offers higher accuracy on domain-specific text. Context length: our chunks are short (300 chars) so context length is not a bottleneck here, but longer documents would need a model with a larger context window. Multilingual support: if international RIT students submitted reviews in other languages, paraphrase-multilingual-MiniLM-L12-v2 would be worth the accuracy tradeoff. Latency: local models add no network round-trip, which matters for a real-time interface.

## Retrieval Test Results

Query 1: "What do students say about Professor Agyingi's teaching style?"
Top chunks returned:
- Chunk from prof_agyingi_rmp.txt: "Professor Agyingi is great!!! He is really fair and if you want to learn math take him. His accent is sometimes difficult to understand but you get used to it."
- Chunk from prof_agyingi_rmp.txt: "He was a great teacher. He made everything really clear and never assumed the class knew anything, which sometimes caused boring moments but was helpful overall."

Why these chunks are relevant: Both chunks contain direct student opinions about Agyingi's classroom behavior and teaching approach. The query asked about teaching style and these chunks describe exactly that — his clarity, fairness, and accessibility. The semantic search correctly matched "teaching style" to language about how he explains material and treats students.

Query 2: "Is Professor Timberlake's class considered difficult?"
Top chunks returned:
- Chunk from prof_timberlake_rmp.txt: "Yes, Professor Timberlake's class is considered difficult by some students. The difficulty level is rated as 4.0 out of 5.0 in one of the reviews."
- Chunk from prof_timberlake_rmp.txt: "TOUGH GRADER LOTS OF HOMEWORK GRADED BY FEW THINGS — your entire grade is essentially the sum of 4 tests."

Why these chunks are relevant: The query asked specifically about difficulty. These chunks were retrieved because they contain difficulty ratings and grading structure descriptions. Even though the query used the word "difficult" and the chunks use phrases like "TOUGH GRADER" and numeric difficulty scores, semantic search matched them correctly because the underlying meaning is the same.

Query 3: "Which RIT math professor is considered the most lenient grader?"
Top chunks returned:
- Chunk from prof_harkin_rmp.txt: "He is strict when it comes to getting homework done, but is lenient on grading."
- Chunk from prof_agyingi_rmp.txt: "He gives you a lot of opportunities to make up any points you may lose, so it all rounds out in the end."
- Chunk from prof_prevendoski_rmp.txt: content about grading approach
- Chunk from prof_shahmohamad_rmp.txt: content about grading approach

## Grounded Generation
Grounding is enforced in the system prompt passed to Groq's llama-3.3-70b-versatile:

"Answer the question using ONLY the information provided in the documents below. If the documents don't contain enough information to answer, say 'I don't have enough information on that.' Do not use any outside knowledge."

Source attribution is added programmatically — after generation, the source filenames of all retrieved chunks are appended to every response regardless of what the LLM returns.

## Example Responses

Example 1 — Agyingi teaching style (accurate, grounded):
Q: "What do students say about Professor Agyingi's teaching style?"
A: "Students have varying opinions about Professor Agyingi's teaching style. Some students have praised him, saying that he is a great teacher who makes everything clear, never assumes the class knows anything, and is fair. They also appreciate his attempt to tell jokes, even if they're not always funny. Additionally, some students have noted that he teaches and explains things very quickly, but makes sure everyone understands before moving on. However, one review mentioned that he covers examples extremely fast and expects students to already know the new material."
Sources: prof_agyingi_rmp.txt

Example 2 — Lopez recommendation (accurate, grounded):
Q: "Would students recommend Professor Lopez?"
A: "It's mixed. Some students would recommend Professor Lopez, as they find him to be a great professor, extremely smart, and always accessible outside of class. However, others mention that his lectures can be disorganized and hard to follow, which might make it difficult for some students to learn from him. Additionally, one student explicitly states 'Would Take Again: No', indicating that they would not recommend him."
Sources: prof_lopez_rmp.txt

Out-of-scope query (refusal response):
Q: "What is the best dining hall at RIT?"
A: "I don't have enough information on that."
Sources: prof_shahmohamad_rmp.txt (retrieval pulled the closest semantic match but the LLM correctly refused to answer from unrelated content)

## Query Interface
The interface is built with Gradio and runs at http://127.0.0.1:7860 after running python3 app.py.

Input fields:
- "Your question" — a text box where the user types any question about RIT math professors

Output fields:
- "Answer" — the grounded LLM response drawn only from retrieved chunks
- "Sources" — a bulleted list of the .txt filenames the answer was drawn from

Sample interaction transcript:
User input: "Is Professor Timberlake's class considered difficult?"
System answer: "Yes, Professor Timberlake's class is considered difficult by some students. The difficulty level is rated as 4.0 out of 5.0 in one of the reviews, and another review mentions that the coursework is challenging. However, the difficulty level may vary depending on the specific class, as one review rates the difficulty level as 2.0 out of 5.0 for CALC226."
Sources: prof_timberlake_rmp.txt

## Evaluation Report

| # | Question | Expected Answer | System Response | Accuracy |
|---|----------|----------------|-----------------|----------|
| 1 | What do students say about Professor Agyingi's teaching style? | Caring, accessible, good at explaining despite accent | Detailed response: fair, clear, fast-paced but thorough, tells jokes | Accurate |
| 2 | Is Professor Timberlake's class considered difficult? | Yes, considered difficult | Yes, rated 4.0/5.0 difficulty, challenging coursework, grade based on few tests | Accurate |
| 3 | Would students recommend Professor Lopez? | Mixed reviews — some yes, some no | Mixed — smart and accessible but disorganized lectures, one explicit "Would Not Take Again" | Accurate |
| 4 | What do students say about Professor Shahmohamad's exams? | Well-structured and fair | "Well-structured and fair" — brief but correct | Accurate |
| 5 | Which RIT math professor is considered the most lenient grader? | Should identify a specific professor by name | Could not name a specific professor — described grading styles without attaching names | Partially Accurate |

## Failure Case
Question 5 ("Which RIT math professor is considered the most lenient grader?") returned a partially accurate response. The system retrieved chunks that contained grading-related language (words like "lenient," "partial credit," "makes up points") but could not name which professor those descriptions belonged to.

The cause is a chunking boundary failure. Rate My Professors pages display the professor's name at the top of each review card, followed by the review text below. When the raw text was copied and chunked at 300-character intervals, the professor's name and the review content ended up in different chunks. The retrieval system returned chunks containing the grading opinions, but those chunks did not include the professor's name. The LLM therefore had the opinion ("he is lenient on grading") without knowing whose opinion it was, and correctly refused to guess a name it didn't have evidence for. A fix would be to prepend the professor's name to every chunk at ingestion time so the identity is always retrievable alongside the content.

## Spec Reflection
The spec helped most during chunking — writing down "300 characters, 50 overlap, because reviews are 1–4 sentences" before touching any code meant the implementation was straightforward and matched the plan exactly. The one divergence was in document cleaning: the spec assumed relatively clean source text, but the raw RMP copies included UI noise (ratings numbers, "Thumbs up 0 Thumbs down 0," course codes, dates) mixed into the review text. The cleaning step had to handle more noise than anticipated, and some of that noise still appears in the chunks — which is visible in sample chunks 1, 2, and 4 above.

## AI Usage

Instance 1: I directed Claude to generate ingest.py using the Documents and Chunking Strategy sections of planning.md as input. Claude produced a script that loaded .txt files, cleaned HTML and UI artifacts, and split text into 300-character chunks with 50-character overlap. I reviewed the output by running python3 ingest.py and inspecting the 5 sample chunks it printed. I confirmed the chunk size matched the spec and that the cleaning removed most but not all RMP UI noise — I accepted the remaining noise as a documented limitation rather than over-engineering the cleaner.

Instance 2: I directed Claude to generate embed.py and app.py using the Retrieval Approach section and the grounding requirement ("answer only from retrieved context, cite sources"). Claude produced working embedding, retrieval, and Gradio interface code. I ran both scripts and hit a ModuleNotFoundError for chromadb — the packages had not installed into the virtual environment correctly. I debugged this by running pip3 install chromadb sentence-transformers groq separately, which resolved the issue. I also verified that the grounding prompt in app.py actually enforced the "no outside knowledge" constraint by testing an out-of-scope question (dining hall) and confirming the refusal response.