# AskmyPDF 

An interactive AI-powered web tool that allows users to:

- Highlight keywords **directly inside PDF files** (with native PDF annotations)
- Ask **natural language questions** about PDF content using OpenAI GPT
- Download and preview the updated, annotated PDFs
- View human-readable summaries with visual keyword context

Built with **Gradio**, **PyMuPDF**, and **OpenAI GPT**, and deployable on Hugging Face Spaces or your own cloud environment.

---

## 💼 Why This Matters

> 📌 PDFs dominate the way knowledge is stored and shared — from compliance reports and research papers to contracts and technical documentation. Yet, **extracting insights and performing contextual search in PDFs remains slow, manual, and error-prone**.

This project solves that by providing:

✅ **Instant keyword highlighting** — directly into the PDF, like an analyst would  
✅ **Semantic understanding** — via LLMs, enabling users to ask open-ended questions (e.g., _“What does this document say about patient history?”_)

###  Real-world Use Cases:

- **🏥 Healthcare**  
  Extract patient conditions, medications, or diagnostic patterns from clinical reports.

- **⚖️ Legal & Compliance**  
  Highlight clauses, find obligations, or answer due diligence questions from contracts or policies.

- **📊 Finance**  
  Scan financial reports, detect terms like “net loss,” and ask semantic queries on trends.

- **📚 Academia**  
  Help researchers explore massive PDFs by highlighting terminology and enabling fast Q&A.

- **🔐 Internal Search Engines**  
  Power knowledge assistants for support teams to search through manuals, policy docs, or SOPs.

> 🚀 **This is a modular foundation for building document intelligence tools in enterprise workflows.**

---

## 🚀 Features

| Feature | Description |
|--------|-------------|
| 🖍️ PDF Keyword Highlight | Adds real highlight annotations inside uploaded PDF files |
| 📄 PDF Preview & Download | Displays the updated PDF for easy review |
| 📝 Keyword Summary | Shows all pages and lines where the keyword appears (with HTML `<mark>` highlights) |
| 🤖 Semantic Q&A | Ask any natural language question — answered contextually using OpenAI GPT |

---

## To enable semantic Q&A:

export OPENAI_API_KEY=your-key-here

## Deployment

Works seamlessly on Hugging Face Spaces (Gradio template)
Supports Hugging Face secrets for secure OpenAI key management

## 🤝 Contributions

Pull requests welcome! If you find this useful or adapt it for your organization, I’d love to hear about it.

📄 License

MIT License
