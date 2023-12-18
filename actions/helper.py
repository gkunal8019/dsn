from typing import List

# Constants
from rasa_sdk import Tracker

SOMETHING_IS_WRONG = "Something is Wrong"
VERTICAL_BUTTON_TYPE = 'vertical'

def get_slot_value(tracker: Tracker, slot_name):
    return tracker.slots.get(slot_name)


def create_button(button_message_details: List):
    button_details = []
    for message in button_message_details:
        button_details.append({"title": message, "payload": message})
    return button_details


def create_hyper_link(url: str, url_description: str):
    return f'<a href="{url}">{url_description}</a>'


def create_yes_or_no_button():
    return create_button(["Yes", "No"])


def required_slots(slots: List, search_text: str):
    return [slot for slot in slots if slot.startswith(search_text)]


def get_database_message(key_value: str):
    messages = {"Levofem": "Levofem is a safe, low-dose, combined oral contraceptive used to prevent pregnancy. Each "
                           "pack contains 21 active yellow tablets and 7 placebo(inactive) tablets which should be "
                           "taken around the same time daily. How to Use\n"
                           " 1. Take your first pill from the packet "
                           "marked with the correct day of the week, or the first pill of the first colour (phasic "
                           "pills)\n"
                           " 2. Continue to take a pill at the same time each day until the pack is finished. "
                           "Continue taking pills for seven days (during these seven days you will get a bleed).\n"
                           " 3. Start your next pack of pills on the eighth day, whether you are still bleeding or"
                           " not. This should be the same day of the week as when you took your first pill\n"
                           "You can buy Levofem at any pharmacy or health store around you.",
                "Desofem": "Desofem is a safe and effective daily pill used in the treatment of certain menstrual "
                           "disorders as well as to prevent pregnancy. How to Use One pill is taken around the same "
                           "time daily for 21 days followed by a 7-day break, then continue with the next pack.",
                "Dianofem": "Dianofem is a safe and effective pill that contains a combination of an antiandrogen ("
                            "Cyprolerone Acetate 2mg) and estrogen (Ethinylestradiol 0.035mg) used for the treatment "
                            "of dermatological and gynecological conditions in women. It also prevents pregnancy. It "
                            "contains 21 tablets with no placebo (inactive pills). How to Use Take one tablet daily "
                            "for 21 days, followed by a 7-day break where no tablets are taken. Start the next pack "
                            "after the 7-day break.",
                "Postpill": "Postpill is a one-dose emergency contraceptive pill by DKT. It contains 1.5 mg "
                            "Levongestrel. POSTPILL should be taken orally as soon as possible within 24 hours but can "
                            "still be taken within 5 days (120 hours) of unprotected\n"
                            "You can click on the audio below to listen to a short introduction of Postpill "
                            "in Pidgin if you want to.\n"
                            f"{create_hyper_link(url='https://drive.google.com/file/d/15O1QpDcxI9Zf1XvoR8REp788YVQcC-Hp/view?usp=drive_link', url_description='Audio embedding (Postpill)')}\n"
                            f"You can buy Postpill at any pharmacy or health store around you.",
                "Postinor 2": "POSTINOR is an Emergency Contraceptive Pill (ECP) that safely prevents unwanted "
                              "accidental pregnancy within 72 hours after unprotected sexual intercourse. "
                              "It doesn’t work if you are already pregnant and will not harm an already established pregnancy. The sooner you take "
                              "POSTINOR, the more effective it is.\n"
                              "You can buy it at any pharmacy or health store around you.",
                "Progesta": "Progesta is an injectable contraceptive, a highly safe and effective contraceptive, "
                            "injected intramuscularly and sometimes into the anus for 3 months continuously.\n "
                            "Its mechanism of action are\n"
                            "• thicken cervical mucus.\n"
                            "• inhibits ovulation.\n"
                            "• thins uterus walls to prevent ovulation.\n"
                            "Advantages of progesta include\n"
                            "• Safe, highly effective, discontinued at will.\n"
                            "• Long-acting,\n"
                            "• Provided outside the clinic,\n"
                            "• Reversible, easy to use, private, and non-contraceptive benefit.\n"
                            "Users include heavy smokers, thyroid disorders, diabetes, those 18 years old or younger, "
                            "breastfeeding mothers, and pelvic inflammatory diseases.\n "
                            "How to use\n"
                            "• Injected in the upper arm or buttocks, start at any time during the menstrual cycle.\n"
                            "• 5 days after menstrual period, abstain from sex for the next 7 days.\n"
                            "• It can be administered after abortion.\n"
                            "• Start 6 weeks after delivery for a breastfeeding woman.\n"
                            "You can click on the audio below to listen to a short introduction to Progesta in Pidgin "
                            "if you want to.\n "
                            f"{create_hyper_link(url='https://drive.google.com/file/d/1rKNyg-etSIiFn1U-XwKNyNkRW8yw_ZSr/view?usp=drive_link', url_description='Audio embedding (Progesta)')}",
                "Kiss": """Kiss condoms are gently lubricated to provide you with a silky, natural feeling for increased pleasure and sensitivity.
You can buy the Kiss condom at any pharmacy or health store around you.
""",
                "Fiesta": """Fiesta is a premium condom brand that comes in 14 exciting variants of styles, colours, textures, flavors, shapes and sizes that increase the sensation for both partners.
1. They provide great protection from both pregnancy and STIs/HIV
2. Exciting variants offer enhanced sexual pleasure for both partners.
3. Ensure STIs/HIV protection for women on other family planning methods.
4. Can be used for oral, anal and vaginal sex.
5. 100% electronically tested and manufactured to meet the highest international quality standards.
You can buy the Fiesta condom at any pharmacy or health store around you.""",
                "Durex": """Durex is a brand of condoms and personal lubricants owned by the British-Dutch company Reckitt Benckiser.
You can visit your nearest health shop to purchase
""",
                "Trojan": """Trojan brand latex condoms are made from premium quality latex to help reduce the risk of unintended pregnancy and sexually transmitted infections. Every condom is electronically tested to help ensure reliability. There are more than 30 varieties of Trojan brand condoms.
You can visit your nearest health shop to buy.
""",
                "Gold Circle": """Gold Circle (GC) Condom is SFH Nigeria's pinnacle product. They offer dual protection to encourage family planning and prevent sexually Transmitted Infections. Gold Circle Condoms are made of latex, well lubricated and shrinked-wrapped for maximum pleasure.
You can visit you nearest health shop to purchase.
""",
                "Levoplant": "LEVOPLANT which is a subdermal contraceptive implant, Levoplant has two small flexible "
                             "rods about matchstick size. It is WHO-prequalified and highly effective for 3 years, "
                             "it is suitable for most women except pregnant women.\n"
                             "Advantages\n"
                             "• Immediate return to fertility.\n"
                             "• Fewer side effects.\n "
                             "• Thinner trocar for the insertion process.\n"
                             "• High quality and most affordable 3-year implant in Nigeria.\n"
                             "Common side effects:\n"
                             "• Menstrual changes.\n"
                             "• Headaches.\n"
                             "• Dizziness.\n"
                             "• Weight changes (loss/Gain)- which is a buildup of water not fat.\n"
                             "• Breast tenderness",
                "Jadelle": "Jadelle is a contraceptive implant that consists of two small flexible "
                           "rods (as short as a match stick but thinner) that is inserted under the skin of "
                           "a woman’s upper arm. It contains 75mg of the hormone Levonorgestrel in each rod. "
                           "Jadelle implants are over 99% effective and can prevent pregnancy "
                           "for a period of 5 years. This method is completely and quickly reversible"
                           " because it releases very low dose of hormone which leaves the body quickly when removed, "
                           "so the woman can get pregnant without delay.",
                "Implanon NXT": "Implanon NXT is a contraceptive implant that consists of one small "
                                "flexible rod that is inserted under the skin of a woman’s upper arm. "
                                "It contains 65mg of the hormone Etonorgestrel in each rod. "
                                "Implanon NXT is over 99% effective and can prevent pregnancy for 3 years. "
                                "Also, it can be stopped anytime the woman wants by asking a health provider "
                                "to remove it. This method is completely and quickly reversible "
                                "because it releases a very low dose of hormone, which leaves the body quickly "
                                "when removed, so you woman can get pregnant without delay."
}
    return messages.get(key_value, SOMETHING_IS_WRONG)
