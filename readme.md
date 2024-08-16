General idea: a project that fills an input Questionnaire file based on the company's ISO27001 policies.

Main pillars:
- many work with unstructured data (xls, pdf, doc, etc)
- RAG different appraches (naive, cluster, parent, rerank approaches)
- Ensemble method for final LLM generation

Run the script: 
`python main.py --policies_path data/raw_ISO27001policies --questionnare_path data/questionnare_to_fill`

High-level flow:
- read policies
- preprocess data
- populate vector DB + index it
- read questionnare, find questions 
- request DB to find similar text
- generate response useing LLM


Думав може відразу під'єднати фреймворк що був чат, плюси в тому що можуть підключатися до багатьох каналів спілкування (whatsapp, telegram, viber, etc, voice), можуть підключатися до БД і векторних. Але то складна система буде, мені треба щось простіше... Ось список хороших: [microsoft botbuilder](https://github.com/microsoft/botbuilder-python), [botpress](https://github.com/botpress/botpress), [rasa](https://github.com/RasaHQ/rasa).
Повертаюсь до ідеї рану зі скрипта, далі буде видно.
