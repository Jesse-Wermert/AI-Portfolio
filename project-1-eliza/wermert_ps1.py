import random
import re
import datetime

NOON = 12
SUNDOWN = 18


class WermertChatAgent:

    def generate_reply(self, in_string):
        """
        Generates a reply based on the given input.
        :param in_string: input to be analyzed
        :return: the smartest reply based on user's input
        """
        if 'math' in in_string:
            return self.generate_calculation()
        for patterns, responses in self.Pairs:
            match = re.match(patterns, in_string.rstrip(".!"))
            if match:
                response = random.choice(responses)
                return response.format(*[self.reflect(x) for x in match.groups()])
        else:
            rand_function = random.choice(self.Reply_Function_List)
            reply = rand_function(in_string)
            return reply

    def reflect(self, substring):
        items = substring.lower().split()
        for i,j in enumerate(items):
            if j in self.Pairs:
                items[i] = self.Pairs[j]
        return ' '.join(items)

    def generate_calculation(self):
        """
        Calculates the user's equation if they'd like to do some math.
        :return: the calculation to the user's equation
        """
        math_prompt = eval(input("Type your equation in"))
        return math_prompt

    def get_current_time(self):
        """
        Gets the current time.
        :return: the time
        """
        current_time = datetime.datetime.now()
        if current_time.hour < NOON:
            return self.good_morning()
        elif NOON <= current_time.hour < SUNDOWN:
            return self.good_afternoon()
        else:
            return self.good_evening()

    def good_morning(self):
        return "Good morning!"

    def good_afternoon(self):
        return "Good afternoon!"

    def good_evening(self):
        return "Good evening!"

    def driver_loop(self):
        """
        The main driver loop for the chat agent
        """
        reply = self.Time + " How are you today? Type 'math' for calculator! Type 'self-destruct' to quit!"
        while True:
            response = input(reply)
            self.Response_List.append(response)
            reply = self.generate_reply(response)

    def swap_person(self, in_word):
        """
        Replace 'I' with 'You', etc. Switches perspective (2nd->1st), (1st->2nd)
        :param in_word: Pronoun to be swapped
        :return: the swapped pronoun
        """
        if in_word in self.Pronoun_Dictionary.keys():
            return self.Pronoun_Dictionary[in_word]
        else:
            return in_word

    def switch_person(self, in_string):
        """
        Swaps 2nd to 1st person, or vice versa.
        :param in_string: input from user
        """
        in_word_list = str.split(in_string)
        swap_person = map(self.swap_person, in_word_list)
        return ' '.join(swap_person)

    def change_person_and_add_prefix(self, in_string):
        """
        Changes perspective (1st->2nd person or vice versa).
        :param in_string: input from user
        :return: The message (with p.o.v. swapped) and a prefix added to it
        """
        reply = self.switch_person(in_string)
        random_prefix = random.choice(self.Prefix_List)
        return ''.join([random_prefix, reply])

    def generate_hedge(self, in_string):
        """
        Produces a hedge in response to user input
        :param in_string: user input
        :return: a hedge from the hedge list
        """
        return random.choice(self.Hedge_List)

    def refer_back(self, in_string):
        """
        Refers back to something the user said earlier in the conversation, and asks them more about it
        :param in_string: the user input
        :return: a full message based on something the user mentioned earlier in the conversation
        """
        past_prefix = random.choice(self.Past_Tense_Responses)
        past_response = random.choice(self.Response_List)
        past_response = self.switch_person(past_response)
        elab_msg = ", Can you elaborate on that please?"
        return ''.join([past_prefix, past_response + elab_msg])

    def __init__(self):
        self.Time = self.get_current_time()
        self.Response_List = []
        self.Pronoun_Dictionary = {'i': 'you', 'I': 'you', 'am': 'are', 'you': 'I', 'were': 'was', 'was': 'were',
                                   'my': 'your', 'are': 'am', 'yours': 'mine', 'your': 'my', 'mine': 'yours'}
        self.Hedge_List = ["Hmm", "That is fascinating", "Let's change the subject", "Ughhhhh", "That is interesting to"
                           "say the least", "That's awful, sorry to hear that", "Oh, nice", "Oh, that's tough"]
        self.Prefix_List = ["Why do you say that ", "What do you mean that ", "What do you mean ", "Why do you say ",
                            "How come "]
        self.Past_Tense_Responses = ["Earlier you said that ", "Why did you say that ", "What did you mean ",
                                     "When you said "]
        self.Reply_Function_List = [self.generate_hedge, self.switch_person, self.change_person_and_add_prefix,
                                    self.refer_back]
        self.Pairs = [
           [r'I need (.*)',
            ["Why do you need {0}?",
             "Are you sure you need {0}?"]],
           [r'I am (.*)',
            ["Did you come to me because you are {0}?",
             "Are you always {0}?"]],
           [r'What (.*)',
            ["What do you think?",
             "Can you not read? I think I was pretty straight forward"]],
           [r'How (.*)',
            ["How do you suppose?",
             "How, what?"]],
           [r'Because (.*)',
            ["Do you think that is the real reason?",
             "Do you think there is another reason behind that {0}?"]],
           [r'(.*) sorry (.*)',
            ["No apology is truly necessary",
             "I will always forgive you",
             "Are you truly sorry?"]],
           [r'Hello(.*)',
            ["Hey there, how are you feeling today?",
             "Hey, nice to hear from you!"]],
           [r'I think (.*)',
            ["Do you really think that {0}",
             "You think that {0}"]],
           [r'(.*) friend (.*)',
            ["Would you like to talk more about your friends?",
             "Are your friends there for you?"]],
           [r'Yes',
            ["You seem certain",
             "Could you talk more about that, other than just yes?"]],
           [r'Is it (.*)',
            ["You think it is {0}?",
             "It could be {0}"]],
           [r'It is (.*)',
            ["You seem very certain about that",
             "Are you sure it's that?"]],
           [r'You are(.*)',
            ["You think I am {0}?",
             "Maybe you want me to be {0}, but I don't know what to think."]],
           [r'I feel(.*)',
            ["Do you feel {0} often?",
             "What do you do when you feel {0}?"]],
           [r'I have(.*)',
            ["Why do you feel the need to tell me you have {0}",
             "Is that right?"]],
           [r'Is there (.*)',
            ["Do you think that there is {0}?",
             "Would you want there to be {0}?"]],
           [r'My(.*)',
            ["Why does your {0}?",
             "Does your {0} make you feel better?"]],
           [r'You (.*)',
            ["This is your session, let's talk more about you and less about me.",
             "You don't need to know too much about me besides that I am your computer bot."]],
           [r'Why(.*)',
            ["What do you think?",
             "You think {0}? Maybe you're right."]],
           [r'I want(.*)',
            ["Do you really want {0}? Or is that only for temporary pleasure?",
             "What will you get out of having {0}?"]],
           [r'(.*) mother (.*)',
            ["Tell more about your mother",
             "What type of relationship do you and your mother have?",
             "Does she abuse you physically, mentally, or emotionally?",
             "Has your mother affected your feelings that you possess today?"]],
           [r'(.*) father (.*)',
            ["Tell more about your father",
             "What type of relationship do you and your mother have?",
             "Does he abuse you physically, mentally, or emotionally?",
             "Has your father affected your feelings that you possess today?"]],
           [r'(.*) mom (.*)',
            ["Tell more about your mom",
             "What type of relationship do you and your mom have?",
             "Does she abuse you physically, mentally, or emotionally?",
             "Has your mom affected your feelings that you possess today?"]],
           [r'(.*) dad (.*)',
            ["Tell more about your dad",
             "What type of relationship do you and your dad have?",
             "Does he abuse you physically, mentally, or emotionally?",
             "Has your dad affected your feelings that you possess today?"]],
           [r'(.*) kid (.*)',
            ["Tell me more about your kid.",
             "What type of relationship do you and your kid have?",
             "Has your kid affected the way that you feel today or are feeling right now?"]],
           [r'(.*) son (.*)',
            ["Tell me more about your son.",
             "What type of relationship do you and your son have?",
             "Has your son affected the way that you feel today or are feeling right now?"]],
           [r'(.*) daughter (.*)',
            ["Tell me more about your daughter.",
             "What type of relationship do you and your daughter have?",
             "Has your daughter affected the way that you feel today or are feeling right now?"]],
           [r'(.*)\?',
            ["Why do you ask that?",
             "That question I believe you might be able to answer on your own. Come back to me about it",
             "Why don't you ask your friends about that one?"]],
           [r'self-destruct',
            ["Thank you, hope our conversation helped you!",
             "Have a good rest of your day. Come back soon, I'll miss you!"]]
        ]


if __name__ == '__main__':
    random.seed()
    agent = WermertChatAgent()
    agent.driver_loop()
