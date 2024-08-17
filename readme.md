### General idea
The aqf-ai project answers a specific question based on a previously filled questionnaire(s).

#### Limitations:
- only .xlsx files for now, provide regex sheet names to search within files in .env
- english only

#### Steps to use:
1. run `./scripts/setup.sh` to set up the project
2. add your xls files in `data/raw_filled_security_questionnaire`
3. create and add all the environmental variables (description below)
4. run `python main.py --action indexdb --filled-questionnaire-files-path {files_path}`. If you followed this instruction then 'data/raw_filled_security_questionnaire' instead of {files_path}
5. run `python main.py --action answer --question {your_question}`. Is disciplinary or sanction policy exists for employees who have violated security policies?

Env variables:
- OPENAI_API_KEY="sk-***" -- openai api key, openai platform [link](https://platform.openai.com/api-keys)
- OPENAI_LLM_MODEL="gpt-3.5-turbo"  -- openai model that will be used
- OPENAI_EMBEDDING_MODEL="text-embedding-ada-002" -- openai model for embeddings (keep embedding-ada-002, it is cheap)
- COLLECTION_NAME="aqf-ai-vector-store" -- vector store, string
- TARGET_SHEET_NAMES="uestion, Questionnaire, QAsheet" -- list of possible sheet names to search for within .xlsx files. Use most common part of the sheet names.

----
Main pillars and other ideas:
- many work with unstructured data (xls, pdf, doc, etc)
- RAG different appraches (naive, cluster, parent, rerank approaches)
- Ensemble method for final LLM generation
- read the file and automatically fill it based on a previously filled questionnaire(s). 


Думав може відразу під'єднати фреймворк що був чат, плюси в тому що можуть підключатися до багатьох каналів спілкування (whatsapp, telegram, viber, etc, voice), можуть підключатися до БД і векторних. Але то складна система буде, мені треба щось простіше... Ось список хороших: [microsoft botbuilder](https://github.com/microsoft/botbuilder-python), [botpress](https://github.com/botpress/botpress), [rasa](https://github.com/RasaHQ/rasa).
Повертаюсь до ідеї рану зі скрипта, далі буде видно.
