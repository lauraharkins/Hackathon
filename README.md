# GPTHack: Turning Language in Platforms

## Description
This is our submission to the Encode AI London Hackathon Virtual Protocol: Best AI Use Case for Gaming, Social or Digital Entertainment bounty. In this project, we created an inifinite platforming game with a twist,
the levels are generated by a language model! 

Instead of using a standard, more traditional level generation routine, we exploited the sequence-based and context aware nature of generative language models to create playable
levels following a defined schematic. This demonstrates the potential of these models, as they are not only powerful for language applications but, with some out of the box thinking, can be used to generate visual worlds using only text.

## Use Case
This project demostrates a proof-of-concept of content-generation ability of current open source language models in the visual domain. We show that with the right fine-tuning, the [distilgpt2](https://huggingface.co/distilbert/distilgpt2) model
can generate unique, playable levels for a platformer-style video game. This has an inital use case of enhancing video game development as it allows the easy creation of unique and varied levels. In this case, we used a platformer as the example, however it would be possible to extend this technology further to other game designs, such as biome generation for a sandbox game like MineCraft. Our solution is suited to this task as language models are inherently context-aware, meaning they can react to the exisiting environment and update or expand upon it in a natural fashion. This is different to tradition level generation where rules have to be manually coded into the game to ensure level generation feels smooth and varied without compromising on playability. For example, traditionally you may have to require generation to place the start and end goal in specific locations, however with generative AI, we found the model learnt the desired start and end location for the levels during the training process without requiring specific instruction.

This project also points to a further use case for language models to complete any generation based task with a well-defined output scheme. By using fine-tuning, we were able to generate consistent level schematics from the language model, however in theory you could generate a schematic for anything using this approach.

## Demo


## Audience
The audience for this project is firstly video game players as using generative AI to create levels allows players to experience more diverse gaming experiences, particularly in inifinite/sandbox games where generative AI would be able to continually generate new, exciting terrain for the player to explore. The experience is enhanced by the fact that language models can build on the content they've previously generated, enabling smooth transitions between areas and levels. This could be combined with using language models for more obvious tasks, such as NPC dialogue and location descriptions to give players access to a rich environment that continually grows to challenge the player.

Secondly, video game developers, particularly indie video game developers, would be able to make extensive use of this technology to simplify traditionally challenging tasks in the development process. This project shows that instead of writing hours of code to produce infinite level generation, developers could create a small number of examples of the levels they are looking for and then finetune a model to produce that. Not only does this save the developer time and effort, allowing them to invest more into areas such as game aesthetics or story, but also could generate richer, more varied worlds and levels than traditional algorithmic techniques could manage. Overall, this technology impacts both the consumer and the supplier, benefiting both in different ways.

## Market Impact


## Technical Details
