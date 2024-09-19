import abc
import json
import logging
import os
import random
import re
import requests
import threading
import wikipediaapi
from abc import ABCMeta
from threading import Thread
from typing import Literal, Optional, Generator

import spacy

from story import Story, SectionType

# Load SpaCy transformer model
nlp = spacy.load("en_core_web_trf")

character_descriptions = [
    "A man in his thirties, Alexander's muscular build is encased in a plaid flannel shirt and jeans, his rugged features softened by a scruffy beard, his piercing green eyes a mischievous spirit.",
    "Granny Clara Jenkins is old but still rocking, wrapped in a floral print dress and shorts, her wispy white hair pulled back into a bun, her wrinkled face adorned with darkened glasses perched on the tip of her nose, her kind eyes twinkling with wisdom and a hint of mischief.",
    "A petite figure draped in a flowy sundress, sandals, and a wide-brimmed hat, Ella's bright smile lights up her heart-shaped face framed by cascading curls of chestnut hair.",
    "An elderly gentleman in his seventies, Henry's stooped posture is adorned with a tweed jacket and a flat cap, his wispy white hair framing a weathered face with deep laugh lines and twinkling blue eyes filled with wisdom and kindness.",
    "A woman in her late twenties, Isabella's slender figure is draped in a form-fitting black dress and stiletto heels, her sleek black hair cascading down her back in loose waves, her sharp cheekbones and intense brown eyes exuding confidence and determination.",
    "Maria's elegant figure is draped in a tailored pantsuit and high heels, her sleek brown hair pulled back into a neat bun, her angular features softened by a warm smile and brown eyes filled with intelligence.",
    "A boy of around fifteen, Noah's gangly frame is clad in worn jeans and an orange hoodie, his messy brown hair falling into his eyes.",
    "A young dark-skinned girl of around ten, Sofia's petite frame is clad in colorful leggings and a mismatched sweater, her curly brown hair tied back, her round face dotted with freckles and her hazel eyes wide with innocence and curiosity.",
]

class LLM(metaclass=abc.ABCMeta):
    GENERATION_PROMPTS = {
        "en": {
            SectionType.TITLE: "Give me an idea for the title of a short story. Write a maximum of 10 words, give me the title only. No explanations.",
            SectionType.INTRO: "Write a short first act/exposition with less than 120 words for a witty short story entitled"
            '"{}". Do not add the title to the text. Use the following protagonist:\n',
            SectionType.SECTION: 'Continue the witty short story with a second act/confrontation. Write less than 120 words. Take the following idea into account: "{}"',
            SectionType.OUTRO: 'Finish the witty short story with a third act/resolution leading to a turning point/climax. Write less than 120 words and take the following idea into account: "{}"',
            SectionType.SECTION_CAPTION: 'Describe very briefly and precisely what can be seen in an image that fits to the following text. "{}" Describe especially the main character of the scene, what happens, and/or what the scene looks like, but not how the character looks. Use 75 tokens maximally. No NSFW or extreme violence',
            SectionType.TITLE_CAPTION: 'Describe very briefly and precisely what can be seen in a title image of a book with the title "{}" and the following content: "{}" Describe especially the main character of the scene, what happens, and/or what the scene looks like, but not how the character looks. Use 75 tokens maximally. No NSFW or extreme violence',
        },
        "de": {
            SectionType.TITLE: "Gib mir eine Idee für den Titel einer Kurzgeschichte. Schreibe maximal 10 Wörter, gib mir nur den Titel. Keine Erklärungen. Antworte auf Deutsch.",
            SectionType.INTRO: "Schreibe auf Deutsch einen kurzen ersten Akt/Exposition mit weniger als 120 Wörtern für eine witzige Kurzgeschichte mit dem Titel "
            '"{}". Füge den Titel nicht in den Text ein. Verwende den folgenden Protagonisten:\n',
            SectionType.SECTION: 'Setze die witzige deutsche Kurzgeschichte mit einem zweiten Akt/einer Konfrontation fort. Schreibe weniger als 120 Wörter. Berücksichtige die folgende Idee: "{}"',
            SectionType.OUTRO: 'Beende die witzige deutsche Kurzgeschichte mit einem dritten Akt/Auflösung, der zu einem Wendepunkt/Klimax führt. Schreibe weniger als 120 Wörter und berücksichtige dabei die folgende Idee: "{}"',
            SectionType.SECTION_CAPTION: 'Describe in English very briefly and precisely what can be seen in an image that fits to the following German text. "{}" Describe especially the main character of the scene, what happens, and/or what the scene looks like, but not how the character looks. Use 75 tokens maximally. No NSFW or extreme violence',
            SectionType.TITLE_CAPTION: 'Describe in English very briefly and precisely what can be seen in a title image of a book with the German title "{}" and the following German content: "{}" Describe especially the main character of the scene, what happens, and/or what the scene looks like, but not how the character looks. Use 75 tokens maximally. No NSFW or extreme violence',
        }
    }


    def __init__(self, lang: Literal["en", "de"]):
        self.lang = lang
        self.prompts = LLM.GENERATION_PROMPTS[lang]

    @abc.abstractmethod
    def infer_stream(
        self, prompt: str, section_type: SectionType, story: Optional[Story], **kwargs
    ) -> Generator[str, None, None]:
        pass

    @abc.abstractmethod
    def infer(
        self, prompt: str, section_type: SectionType, story: Optional[Story], **kwargs
    ) -> str:
        pass


class llama3(LLM):
    def __init__(self, lang: Literal["en", "de"]):
        super().__init__(lang)
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.ERROR)

    def request_llama3(self, prompt: str):
        url = "https://llm.srv.webis.de/api/generate"
        data = {
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }

        try:
            # Send a POST request to the API endpoint
            response = requests.post(url, json=data)
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return None

    def infer_stream(
        self, prompt: str, section_type: SectionType, story: Optional[Story], **kwargs
    ) -> Generator[str, None, None]:
        llama_response = self.request_llama3(prompt)
        if llama_response:
            generated_text = llama_response.get("text", "")
            if generated_text:
                yield generated_text

    def infer(
        self, prompt: str, section_type: SectionType, story: Optional[Story], **kwargs
    ) -> str:

        llama_response = self.request_llama3(prompt)

        if llama_response:
            return llama_response.get('response')
        else:
            return ""
        
    # _encode Method not used in the code
    def _encode(self, prompt: str, section_type: SectionType, story: Optional[Story], main_character_name: str):
        character_description = next((desc for desc in character_descriptions if main_character_name.lower() in desc.lower()), random.choice(character_descriptions))
        messages = []
        if story is not None:
            for section in story.sections:
                messages.append(
                    {
                        "role": "user",
                        "content": self.prompts[section.section_type].format(story.title),
                    }
                )
                messages.append({"role": "assistant", "content": section.content})

        prompt += "\n" + character_description

        messages.append({"role": "user", "content": prompt})
        return messages

    def retrieve_wikipedia_summary(self, title: str):
        doc = nlp(title)  # Apply the SpaCy NLP model to the title
        wiki_wiki = wikipediaapi.Wikipedia('RagProj', 'en')
        summaries = []
        entity_info = []

        # Check if there are any named entities
        if not doc.ents:
            return "No relevant named entities found in the title.", []

        for ent in doc.ents:  # Iterate over the named entities detected in the title
            page = wiki_wiki.page(ent.text)
            if page.exists():
                summaries.append(f"{ent.text}: {page.summary}...")  
                entity_info.append((ent.text, page.fullurl))

        summary_text = "\n".join(summaries) if summaries else "No relevant information found on Wikipedia."
        return summary_text, entity_info

    def generate_story(self, title: str):
        main_character_name = random.choice(character_descriptions)
        story_without_rag = {}
        story_with_rag = {}

    # Generate each part of the story
        for section_type in [SectionType.INTRO, SectionType.SECTION, SectionType.OUTRO]:
            prompt = self.prompts[section_type].format(title)

        # Add character description to every section
            character_description = next((desc for desc in character_descriptions if main_character_name.lower() in desc.lower()), random.choice(character_descriptions))
            prompt += "\n" + character_description

        # Generate part of the story without RAG
            generated_text = self.infer(prompt, section_type, None)
            story_without_rag[section_type] = generated_text

        # Retrieve Wikipedia summary for RAG
            wiki_summary, entity_info = self.retrieve_wikipedia_summary(title)
            augmented_prompt = prompt + "\n\nContext from Wikipedia:\n" + wiki_summary

        # Generate part of the story with RAG
            generated_text_with_rag = self.infer(augmented_prompt, section_type, None)
            story_with_rag[section_type] = generated_text_with_rag

        full_story_without_rag = "\n\n".join(story_without_rag.values())
        full_story_with_rag = "\n\n".join(story_with_rag.values())

        return full_story_without_rag, full_story_with_rag, entity_info

# Example usage:
if __name__ == "__main__":
    model = llama3(lang="en")
    title = "A driving journey with Tundra"
    full_story_without_rag, full_story_with_rag, entity_info = model.generate_story(title)

    print("Title:")
    print(title)
    print("\nExtracted Entities and Wikipedia Links:")
    for entity, link in entity_info:
        print(f"{entity}: {link}")

    print("\nStory without RAG:")
    print(full_story_without_rag)
    print("\nStory with RAG:")
    print(full_story_with_rag)