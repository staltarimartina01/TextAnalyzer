#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dataset Generator per TextAnalyzer
Genera un dataset bilanciato di testi AI e umani per calibrazione e validazione
"""

import random
import json
import os
from typing import List, Dict, Any

# Sample di testi umani (varie epoche e stili)
HUMAN_TEXTS = [
    # Edgar Allan Poe - Stile gotico
    """TRUE!—nervous—very, very dreadfully nervous I had been and am; but why will you say that I am mad? The disease had sharpened my senses—not destroyed—not dulled them. Above all was the sense of hearing acute. I heard all things in the heaven and in the earth. I heard many things in hell. How, then, am I mad?""",

    """It is impossible to say how first the idea entered my brain; but once conceived, it haunted me day and night. Object there was none. Passion there was none. I loved the old man. He had never wronged me. He had never given me insult. For his gold I had no desire.""",

    # Charles Dickens - Stile Victorian
    """It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, it was the season of Darkness, it was the spring of hope, it was the winter of despair.""",

    """Mr. Dombey was a gentleman of some energy and decision, as the reader has been given to understand. He was a man of a cool temper, and of strong will, not easily worked upon, and not very pliable.""",

    # Jane Austen - Stile Regency
    """It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife. However little known the feelings or views of such a man may be on his first entering a neighbourhood, this truth is so well fixed in the minds of the surrounding families, that he is considered the rightful property of some one or other of their daughters.""",

    """Elizabeth's astonishment was beyond expression. She had never seen a place where nature and art were so happily combined. The gentle rise of the hill, the varied outline of the wood, the shining river, all were as if painted by a master's hand.""",

    # Mark Twain - Stile americano
    """We said there warn't no home like a raft, after all. Other places do seem so cramped up and smothery, but a raft don't. You feel mighty free and easy and comfortable on a raft.""",

    """The Adventures of Huckleberry Finn was written in a very interesting way. The author used the language of the common people, which made the story feel real and honest.""",

    # George Orwell - Stile moderno
    """It was a bright cold day in April, and the clocks were striking thirteen. Winston Smith, his chin nuzzled into his breast in an effort to escape the vile wind, slipped quickly through the glass doors of Victory Mansions.""",

    # Toni Morrison - Stile contemporaneo
    """She was dead. No one around her knew. The baby, wrapped in a towel, quiet as a test. The old woman stood at the stove, her back to the room, a steamy broth simmering. A knife stuck in a potato.""",

    # Virginia Woolf - Stile stream of consciousness
    """Mrs. Dalloway said she would buy the flowers herself. For Lucy had her work cut out for her. The doors would be taken off their hinges; Rumpelmayer's men were coming. And then, thought Clarissa Dalloway, what a morning—fresh as if issued to children.""",

    # Hemingway - Stile minimalista
    """There is no end to the river. The water flows through the night, past the sleeping town, past the bridge, under the moonlight. Everything is quiet except for the sound of water against the stones.""",

    # F. Scott Fitzgerald - Stile Jazz Age
    """In my younger and more vulnerable years my father gave me some advice that I've carried with me ever since. Whenever you feel like criticizing anyone, just remember that all the people in this world haven't had the advantages that you've had.""",

    # James Joyce - Stile modernista
    """Stately, plump Buck Mulligan came from the stairhead, bearing a bowl of lather on which a mirror and a razor lay crossed. A yellow dressinggown, ungirdled, was sustained gently behind him by the mild morning air.""",

    # Ray Bradbury - Stile futuristico
    """It was a pleasure to burn. It was a special pleasure to see things eaten, to see things blackened and changed. With the brass nozzle in his fists, with this great python spitting its venomous kerosene upon the world, the fire swelled his mind as he held it back.""",
]

# Sample di testi AI (pattern più uniformi e prevedibili)
AI_TEXTS = [
    # ChatGPT-like responses
    """Artificial intelligence represents a revolutionary advancement in modern technology. This field encompasses machine learning, natural language processing, and complex algorithmic systems designed to simulate human cognitive functions. AI has the potential to transform various industries, including healthcare, transportation, and education. The implications of widespread AI adoption are far-reaching and require careful consideration of ethical implications and societal impacts. Scientists and researchers continue to develop more sophisticated AI systems that can perform increasingly complex tasks with greater efficiency and accuracy.""",

    """The integration of artificial intelligence in modern business environments has shown significant promise. Companies across multiple sectors have implemented AI-driven solutions to optimize operations, reduce costs, and improve customer experiences. Machine learning algorithms analyze vast amounts of data to identify patterns and trends that humans might overlook. These insights enable organizations to make data-driven decisions that enhance productivity and competitiveness. The future of AI in business looks increasingly promising as technology continues to evolve.""",

    # Structured academic writing
    """This research paper examines the multifaceted relationship between artificial intelligence and human creativity. The study utilizes a mixed-methods approach combining quantitative analysis with qualitative interviews. The results indicate a complex interplay between technological innovation and artistic expression. Future research should explore the implications for creative industries and educational methodologies. The findings have significant implications for policymakers and technology developers seeking to balance innovation with human values.""",

    """The proliferation of digital technologies has fundamentally altered the landscape of human communication. This phenomenon represents a paradigm shift in how information is created, shared, and consumed. The implications extend beyond technological considerations to encompass social, cultural, and psychological dimensions. Understanding these changes requires interdisciplinary approaches that draw from fields including sociology, psychology, and communication studies. This analysis contributes to the growing body of literature on digital transformation.""",

    # Corporate/Technical writing
    """Our company is committed to delivering innovative solutions that meet the evolving needs of our customers. We leverage cutting-edge technologies to create value and drive sustainable growth. Our team of experienced professionals works collaboratively to ensure exceptional results. Customer satisfaction remains our highest priority, and we continuously strive to exceed expectations through quality and innovation.""",

    # Data-driven analysis
    """Statistical analysis reveals significant correlations between various factors in the dataset. The results demonstrate consistent patterns across multiple variables. This analysis provides valuable insights for decision-making processes. The methodology employed ensures reliability and validity of the findings. Recommendations based on these results can inform strategic planning initiatives.""",

    # Informational content
    """The history of artificial intelligence spans several decades of research and development. Early pioneers in the field established foundational concepts that continue to influence modern AI systems. The evolution of computational power has enabled increasingly sophisticated applications. Current research focuses on areas such as deep learning, natural language understanding, and computer vision. Future developments promise even more remarkable advances in machine intelligence.""",

    # Product descriptions
    """This innovative product offers exceptional quality and performance at an affordable price. Advanced features include multiple customization options and user-friendly design. Customers consistently rate this product highly for reliability and value. The comprehensive warranty ensures peace of mind for all users. Experience the difference with this cutting-edge solution."""
]

class DatasetGenerator:
    """Genera dataset bilanciato per training e validazione"""

    def __init__(self):
        self.human_texts = HUMAN_TEXTS
        self.ai_texts = AI_TEXTS
        self.dataset = []

    def generate_dataset(self, total_samples: int = 100) -> List[Dict[str, Any]]:
        """Genera dataset bilanciato"""
        print(f"🎯 Generating dataset with {total_samples} samples...")

        # Calcola quantità per classe (metà AI, metà Umano)
        samples_per_class = total_samples // 2

        dataset = []
        id_counter = 1

        # Aggiungi testi umani
        for i in range(samples_per_class):
            text = random.choice(self.human_texts)

            # Applica variazioni per aumentare diversità
            if random.random() > 0.7:
                # Aggiungi/rimuovi righe
                paragraphs = text.split('\n\n')
                if len(paragraphs) > 1 and random.random() > 0.5:
                    text = random.choice(paragraphs)

            dataset.append({
                'id': id_counter,
                'text': text,
                'label': 'human',
                'source': 'literature',
                'length': len(text.split())
            })
            id_counter += 1

        # Aggiungi testi AI
        for i in range(samples_per_class):
            text = random.choice(self.ai_texts)

            # Applica variazioni
            if random.random() > 0.7:
                sentences = text.split('. ')
                if len(sentences) > 3:
                    # Estrai sottoinsieme di frasi
                    start = random.randint(0, len(sentences) - 3)
                    text = '. '.join(sentences[start:start+3])

            dataset.append({
                'id': id_counter,
                'text': text,
                'label': 'ai',
                'source': 'generated',
                'length': len(text.split())
            })
            id_counter += 1

        # Shuffle
        random.shuffle(dataset)

        self.dataset = dataset
        print(f"✅ Generated {len(dataset)} samples")
        print(f"   📊 Human: {sum(1 for d in dataset if d['label'] == 'human')}")
        print(f"   🤖 AI: {sum(1 for d in dataset if d['label'] == 'ai')}")

        return dataset

    def save_dataset(self, filename: str = "validation_dataset.json"):
        """Salva dataset su file"""
        if not self.dataset:
            print("⚠️ Dataset empty, generating first...")
            self.generate_dataset()

        os.makedirs("data", exist_ok=True)
        filepath = f"data/{filename}"

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.dataset, f, indent=2, ensure_ascii=False)

        print(f"💾 Dataset saved to: {filepath}")
        return filepath

    def get_statistics(self) -> Dict[str, Any]:
        """Ottieni statistiche del dataset"""
        if not self.dataset:
            return {}

        human = [d for d in self.dataset if d['label'] == 'human']
        ai = [d for d in self.dataset if d['label'] == 'ai']

        stats = {
            'total_samples': len(self.dataset),
            'human_count': len(human),
            'ai_count': len(ai),
            'avg_length_human': sum(d['length'] for d in human) / len(human) if human else 0,
            'avg_length_ai': sum(d['length'] for d in ai) / len(ai) if ai else 0,
            'min_length': min(d['length'] for d in self.dataset),
            'max_length': max(d['length'] for d in self.dataset)
        }

        return stats


if __name__ == "__main__":
    generator = DatasetGenerator()
    dataset = generator.generate_dataset(100)
    generator.save_dataset()

    stats = generator.get_statistics()
    print("\n📈 Dataset Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
