from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import EventType, ActiveLoop, SlotSet, FollowupAction
from rasa_sdk.types import DomainDict
from actions.helper import *
from actions.action_0_2years import *


class ActionPath(Action):
    def name(self) -> Text:
        return "action_path"

    async def run(self,
                  dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        buttons = [{"title": "I want to ask about family planning.", "payload": "I want to ask about family planning."},
                   {"title": "I want the nearest family planning clinic to me.",
                    "payload": "I want the nearest family planning clinic to me."},
                   {"title": "Other reproductive health issues.", "payload": "Other reproductive health issues."}]
        dispatcher.utter_message("What would you like to know about?", buttons=buttons, button_type="vertical")
        return []


class ActionFamilyMethod(Action):

    def name(self) -> Text:
        return "action_family_method"

    async def run(self,
                  dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        buttons = [{"title": "I want to start using a method.", "payload": " I want to start using a method."},
                   {"title": " I want to start using another method.",
                    "payload": " I want to start using another method."},
                   {"title": "  I want to know about side effects.",
                    "payload": "  I want to know about side effects."},
                   {"title": "  I want to know about family planning products.",
                    "payload": " I want to know about family planning products."}]
        dispatcher.utter_button_message("What would you like to know about?", buttons)
        return []


class ValidateRequestFamilyPlanningUsingMethodForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_request_family_planning_using_method_form"

    async def required_slots(
            self,
            domain_slots: List[Text],
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
    ) -> List[Text]:
        updated_slots = domain_slots.copy()

        print(get_slot_value(tracker, 'is_planned_family_planning_before'))
        if get_slot_value(tracker, 'is_planned_family_planning_before') == "No":
            updated_slots.remove("followed_method_before")
            updated_slots.remove("satisfied_last_method")
            updated_slots.remove("reason_for_not_satisfied")

        if get_slot_value(tracker, 'satisfied_last_method') == 'Yes':
            updated_slots.remove("reason_for_not_satisfied")

        print(f"updated Slots: {updated_slots}")
        return updated_slots


class ActionNextActions(Action):

    def name(self):
        return "action_next_options"

    async def run(self,
                  dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        next_response = {'0-3 months': 'utter_0_3_months_response',
                         '1-2 years': 'utter_1_2_years_response',
                         '3-4 years': 'utter_3_4_years_response',
                         '5-10 years': 'utter_5_10_years_response',
                         '1-2 permanently': 'utter_permanently_response',

                         }

        dispatcher.utter_message(response=next_response.get(get_slot_value(tracker, 'prevent_pregnancy_time'),
                                                            "Invalid Option Selected"))
        return []


# 0_3 Months flow

class AskForSlot03MonthsMethod(Action):
    def name(self) -> Text:
        return "action_ask_0_3_months_method"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        button_details = create_button(["Daily contraceptive pills", "Emergency contraceptive pills",
                                        "Injectable contraceptives", "Diaphragm", "Female condom", "Male condom"])
        dispatcher.utter_message(text="The short-term family planning methods are: \n "
                                      "1. Daily contraceptive pills\n"
                                      "2. Emergency contraceptive pills\n"
                                      "3. The barrier contraceptives which are the diaphragms and "
                                      "condoms and then the Injectables.\n"
                                      "Click on any of them to get the full details about them.",
                                 buttons=button_details, button_type="vertical")
        return []


class AskForSlotDailyPillsAdvantage(Action):
    def name(self) -> Text:
        return "action_ask_daily_pills_advantage"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        audio_link = create_hyper_link(url='https://drive.google.com/file/d/1XLnrE5GF2eW8A8_9uJ0M3IhAzzpu0ijx/view'
                                           '?usp=drive_link',
                                       url_description='Audio embedding (Daily pills)')
        message = "Daily pills are combined oral contraceptive (COC) pills for pregnancy prevention, dermatological " \
                  "and gynecological conditions, and management of menstrual irregularities (heavy bleeding, " \
                  "painful menstruation, premenstrual syndrome). " \
                  "They work by thickening the mucus around the cervix, which makes it difficult for sperm to enter " \
                  "the uterus and reach any eggs that may have been released. " \
                  "Most combination pills come in either a 21-day pack (Dianofem and Desofem) or a 28-day pack (" \
                  "Levofem). One pill is taken each day at about the same time for 21 days. Depending on your pack, " \
                  "you will either have a 7-day break (as in the 21-day pack) or you will take the pill that contains " \
                  "Iron for 7 days (the 28-day pack). \n" \
                  "Click to listen to a short introduction of daily pills in Pidgin, if you want to.\n" \
                  f"{audio_link}\n" \
                  f"Now let me tell you some of the advantages and disadvantages of daily pills.\n" \
                  f"Advantages \n" \
                  f"1. They are very effective if used correctly.\n" \
                  f"2. Very safe for the majority of women.\n" \
                  f"3. Return to fertility is very fast.\n" \
                  f"4. They regularize the menstrual cycle, reduce heavy menstrual flow, and " \
                  f"reduce menstrual and ovulation pain.\n" \
                  f"5. They are simple and easy to use.\n" \
                  f"Do you understand?"
        dispatcher.utter_message(text=message)
        return []


class AskForSlotDailyPillsDisadvantage(Action):
    def name(self) -> Text:
        return "action_ask_daily_pills_disadvantage"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = "Now to the disadvantages of daily pills.\n" \
                  "Disadvantages\n" \
                  "1. They must be taken daily which might be difficult to comply with.\n" \
                  "2. They might cause mild and temporary side effect which usually goes away after some weeks such " \
                  "as:\n" \
                  "a. Mild headache.\n" \
                  "b. Nausea or vomiting.\n" \
                  "c. Spotting or bleeding at intervals.\n" \
                  "d. Breast tenderness and soreness to touch.\n" \
                  "e. Mood changes.\n" \
                  "Are you with me?"
        button_details = create_button(["Yes", "No"])
        dispatcher.utter_message(text=message, buttons=button_details, button_type="vertical")
        return []


class AskForSlotWhoCanAndCannotDailyPills(Action):
    def name(self) -> Text:
        return "action_ask_daily_who_can_use_pills"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = "On who can use and who cannot use daily pills.\n Who can use \n" \
                  "1.You can use daily pills if you want a short-term contraceptive method.\n" \
                  "2. If you are a breastfeeding mother (from six months after birth)\n" \
                  "3. If you have irregular menstrual cycle.\n" \
                  "4. If you don't have migrainous headaches.\n" \
                  "5. If you are taking antibiotics, antifungal or antiparasitic medications.\n" \
                  "Do you understand?"
        dispatcher.utter_message(text=message)
        return []


class AskForSlotMedicalConditions(Action):
    def name(self) -> Text:
        return "action_ask_daily_medical_conditions"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = "Who cannot use\n" \
                  "1. If you are a breastfeeding mother from 6 weeks to 6 months postpartum.\n" \
                  "2. If you are a smoker and over 35 years old.\n" \
                  "3. If you have any of the following medical conditions, it is not advisable to take daily piils:\n" \
                  "a. Blood Pressure\n" \
                  "b. Venous thromboembolism\n" \
                  "c. Stroke.\n" \
                  "d. Heart Disease.\n" \
                  "e. Liver Disease\n" \
                  "f. Breast Cancer\n" \
                  "g. Diabetes\n" \
                  "h. Sickle-cell Anaemia"
        dispatcher.utter_message(text=message)
        message = "Do you have any of the medical conditions listed?"
        buttons = create_button(["Yes", "No", "I don't know"])
        dispatcher.utter_message(text=message, buttons=buttons, button_type="vertical")
        return []


class AskForSlotDailyContraceptiveDatabase(Action):
    def name(self) -> Text:
        return "action_ask_daily_contraceptive_database"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = "Let me tell you some of the effective and available daily contraceptive pills.\n" \
                  "Click on any of them to get their full details."
        buttons = create_button(["Levofem", "Desofem", "Dianofem"])
        dispatcher.utter_message(text=message, buttons=buttons, button_type="vertical")
        return []


# Emergency
class AskForSlotEmergencyPillExplanation(Action):
    def name(self) -> Text:
        return "action_ask_emergency_pill_explanation"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = "Emergency contraceptive pills are pills taken immediately after unprotected sex to prevent " \
                  "pregnancy. They contain 1.5mg Levonorgestrel and it is a one-dose medication. They work by " \
                  "stopping the release of an egg from your ovary. It may prevent sperm from fertilizing the egg and " \
                  "if fertilization occurs, it may prevent the fertilized egg from attaching to the womb. Emergency " \
                  "pills are very effective when taken before sex especially during ovulation or within 24 to 72 " \
                  "hours after unprotected sex. Please note that they have no effect on already established " \
                  "pregnancy. \n" \
                  "Do you understand?"
        dispatcher.utter_message(text=message)
        return []


class AskForSlotEmergencyPillAdvantage(Action):
    def name(self) -> Text:
        return "action_ask_emergency_pill_advantage"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = "Now let me tell you some of the advantages and disadvantages of emergency pills. Advantages\n" \
                  "1. Emergency pills are safe for all women including breastfeeding mothers with babies 6 weeks or " \
                  "older.\n" \
                  "2. They are convenient, readily available and easy to use.\n" \
                  "3. The one-dose regimen ensures compliance.\n" \
                  "4. They reduce the need for abortion.\n" \
                  "5.Their side effects are of very short duration.\n" \
                  "6. Quick and easiest option for preventing unplanned pregnancy.\n" \
                  "Do you understand?"
        dispatcher.utter_message(text=message)
        return []


class AskForSlotEmergencyPillDisadvantage(Action):
    def name(self) -> Text:
        return "action_ask_emergency_pill_disadvantage"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = "Now to the disadvantages of emergency pills.\n" \
                  " Disadvantages \n" \
                  "1. They must be taken daily within 3 days of unprotected sex.\n" \
                  " 2. They are less effective than regular contraceptives. \n" \
                  "3. They might cause mild and temporary side effect which usually goes away after some days such as: " \
                  "a. Mild headache.\n" \
                  "b. Nausea or vomiting.\n" \
                  "c. Dizziness.\n" \
                  "d. Breast tenderness.\n" \
                  "e. Lower abdominal discomfort.\n" \
                  "f. Menstrual change (period may come early)\n" \
                  "Are you with me?"
        buttons = create_button(["Yes", "No"])
        dispatcher.utter_message(text=message, buttons=buttons, button_type="vertical")
        return []


class AskForSlotEmergencyWhoCanAndCannotUseContraceptive(Action):
    def name(self) -> Text:
        return "action_ask_emergency_who_can_and_cannot_use_contraceptive"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = "On who can use and who cannot use emergency pills.\n Who can use \n" \
                  "All women can use emergency contraceptive pills safely and effectively, including women who cannot " \
                  "use continuing hormonal contraceptive methods\n. " \
                  "Because of the short-term nature of their use there are no medical conditions that make " \
                  "emergency contraceptive pills unsafe for any woman. " \
                  "Who cannot use\n " \
                  "Not suitable for women wth confirmed or suspected pregnancy.\n" \
                  "Do you understand?"
        dispatcher.utter_message(text=message)
        return []


class AskForSlotEmergencyContraceptiveDatabase(Action):
    def name(self) -> Text:
        return "action_ask_emergency_contraceptive_database"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = "Let me tell you some of the effective and available daily contraceptive pills. \n" \
                  "Click on any of them to get their full details."
        buttons = create_button(["Postpill", "Postinor 2"])
        dispatcher.utter_message(text=message, buttons=buttons, button_type="vertical")
        return []


class AskForSlotInjectableExplanation(Action):
    def name(self) -> Text:
        return "action_ask_injectable_explanation"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = "Injectable contraceptives are a form of hormonal birth control for women. They consist of monthly " \
                  "injections of combined formulations containing an estrogen and a progestin to prevent pregnancy. " \
                  "The injection works by preventing the ovaries from releasing an egg each month. It also thickens " \
                  "the fluid around the cervix. They can be used for pregnancy prevention for 1 to 3 months.\n" \
                  "Do you understand?"
        dispatcher.utter_message(text=message)
        return []


class AskForSlotInjectableAdvantage(Action):
    def name(self) -> Text:
        return "action_ask_injectable_advantage"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = "Ok, let me tell you some of the advantages and disadvantages of injectable contraceptives.\n" \
                  "Advantages\n" \
                  "1. They are highly effective and safe.\n" \
                  "2. They do not interfere with sexual intercourse." \
                  "3. They can be self administered or provided by a trained non-medical personnel." \
                  "4. They protect against ectopic pregnancy." \
                  "5.They reduce symptoms of endometriosis." \
                  "6. They are convenient, easy to use and administered once in a month.\n" \
                  "Do you understand?"
        dispatcher.utter_message(text=message)
        return []


class AskForSlotInjectableDisadvantage(Action):
    def name(self) -> Text:
        return "action_ask_injectable_disadvantage"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = "Now to the disadvantages of injectable contraceptives." \
                  "Disadvantages\n" \
                  "1. They require regular visit to the to the clinic (monthly)" \
                  "2. Return to fertility is delayed.\n" \
                  "3.Their common sides effects include:" \
                  "a. Weight changes.\n" \
                  "b. Headache.\n" \
                  "c. Dizziness.\n" \
                  "d. Breast tenderness.\n" \
                  "e. Mood changes.\n" \
                  "f. Menstrual change.\n" \
                  "g. Decreased libido.\n" \
                  "But don't worry, these side effects goes away with time.\n" \
                  "Are you with me?."
        dispatcher.utter_message(text=message, buttons=create_yes_or_no_button(), button_type="vertical")
        return []


class AskForSlotInjectablesWhoCanAndCannotUseInjectables(Action):
    def name(self) -> Text:
        return "action_ask_injectable_who_can_and_cannot_use_injectables"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = "On who can use and who cannot use injectables.\n" \
                  "Who can use\n" \
                  "1. Women who cannot use combined oral contraceptives.\n" \
                  "2. If you are a breastfeeding mother (from six months after birth)\n" \
                  "3. If you just had an abortion or miscarriage and still want to prevent pregnancy.\n" \
                  "4. If you dont't have migrainous headaches.\n" \
                  "5. If you have endometrial or ovarian cancer, you can still use this method.\n" \
                  "Do you get me"
        dispatcher.utter_message(text=message)
        return []


class AskForSlotInjectablesMedicalConditions(Action):
    def name(self) -> Text:
        return "action_ask_injectable_medical_conditions"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = "Do you have any of the medical conditions listed?"
        dispatcher.utter_message(text=message, buttons=create_button(["Yes", "No", "I don't know"]),
                                 button_type="vertical")
        return []


class AskForSlotInjectableDatabase(Action):
    def name(self) -> Text:
        return "action_ask_injectable_database"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = "Let me tell you some of the effective and available Injectable contraceptives.\n" \
                  "Click on any of them to get their full details."
        dispatcher.utter_message(text=message, buttons=create_button(["Progesta", "Sayana Press"]),
                                 button_type="vertical")
        return []


class AskForSlotDiaphragmExplanation(Action):
    def name(self) -> Text:
        return "action_ask_diaphragm_explanation"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = "A diaphragm is a  type of barrier contraceptive device inserted into the vagina before sex to " \
                  "cover the cervix so that sperm can't get into the womb (uterus). You need to use" "spermicide with " \
                  "it (spermicides kill sperm). The diaphragm must be left in place for at least 6 hours after sex.  " \
                  "The diaphragm is a vaginal barrier contraceptive that is" "woman-controlled, nonhormonal, " \
                  "and appropriate for women who cannot or do not want to use hormonal contraceptive methods, " \
                  "intrauterine devices, or condoms.\n" \
                  f"{create_hyper_link(url='https://drive.google.com/file/d/1iRQyVnIdZ4MznYlUUVzyhwaPSSlDjobY/view?usp=drive_link', url_description='Audio  embedding (Diaphragm)')}"
        dispatcher.utter_message(text=message)
        return []


class AskForSlotDiaphragmAdvantage(Action):
    def name(self) -> Text:
        return "action_ask_diaphragm_advantage"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = "Now let me tell you some of the advantages and disadvantages of Diaphragms.\n" \
                  "Advantages\n" \
                  "1. Diaphragms do not have hormones, so no side effects.\n" \
                  "2. Good option for women who prefer non-hormonal contraceptive methods.\n" \
                  "3. They may be fitted at any time (post-partum mothers must wait for 6 weeks after delivery or mid-trimester abortion)\n" \
                  "4. They can be inserted up to 6 hours before sex to avoid interruption.\n" \
                  "5. Only used when needed and gives the woman absolute control.\n" \
                  "6. One size fits most women.\n" \
                  "7. Portable and convenient - it comes with a specially designed case that is discreet and fits in a bag.\n" \
                  "8. Easy to use - insertion and removal gets better with practice.\n" \
                  "9. Can be used for up to 2 years with proper care.\n" \
                  "Do you understand"
        dispatcher.utter_message(text=message)
        return []


class AskForSlotDiaphragmDisadvantage(Action):
    def name(self) -> Text:
        return "action_ask_diaphragm_disadvantage"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = """"Now to the disadvantages of using a Diaphragm.
Disadvantages
1. They are not readily available in Nigeria.
2. They may be expensive to some users.
3. The user must remember to insert the diaphragm before intercourse and keep it in place for at least 6 hours after sex (but not more than 24 hours) 
4. They require special care and storage.
5. They can cause urinary tract infections.
6. A different size of diaphragm may be required after childbirth or if a woman gains weight.
7. They can be damaged by excessive use or poor storage \n
Are you with me?"
"""
        dispatcher.utter_message(text=message)
        return []


class AskForSlotDiaphragmWhoCanAndCannotUse(Action):
    def name(self) -> Text:
        return "action_ask_diaphragm_who_can_and_cannot_use"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = """On who can use and who cannot use diaphragms.
Who can use
1. If you want a safe and effective non-hormonal form of contraceptive.
2. If you cannot use hormonal methods of contraception for medical reasons.
3. If you are breastfeeding.
4. If you have sexual intercourse occasionally.
Who cannot use
1. If you have an allergy or are sensitive to latex rubber or spermicide.
2. If you have severe uterine prolapse (when the uterus descends toward or into the vagina)
3. If have recurrent urinary tract infections.
4. If you lack facilities (soap and water) to taking care of the diaphragm.\n
Do you understand
"""
        dispatcher.utter_message(text=message, buttons=create_yes_or_no_button(), button_type="vertical")
        return []


class AskForSlotDiaphragmShow(Action):
    def name(self) -> Text:
        return "action_ask_diaphragm_show"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = """Ok, let me show you what a diaphragm looks like and how to use it."""
        dispatcher.utter_message(text=message)
        return []


class AskForSlotFemaleCondom(Action):
    def name(self) -> Text:
        return "action_ask_female_condom"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = """Female condoms are a barrier method of contraception worn inside the vagina. They are made of thin soft plastic and have two ﬂexible rings – a removable ring at the closed end to help insertion and a fixed ring at the open end, which sits on the vulva to hold the condom in place They prevent pregnancy by stopping sperm from meeting an egg. 
"Some of its advantages include:
1. No medical prescription is required.
2. Female condoms are widely available.
3. They have no side effects.
4. They protect against sexually transmitted infections.
5. They are cheap.
6. Woman has control over usage and use only when needed."
and one of its disadvantages is that it might make unpleasant noise during intercourse.\n
Do you understand"""
        dispatcher.utter_message(text=message, buttons=create_yes_or_no_button(), button_type="vertical")
        return []


class AskForSlotFemaleWhoCanAndCannotUseCondom(Action):
    def name(self) -> Text:
        return "action_ask_female_who_can_and_cannot_use_condom"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = """On who can use and who cannot use female condoms.
Who can use
1. If you want a safe and effective non-hormonal form of contraceptive.
2. If you cannot use hormonal methods of contraception for medical reasons.
3. If you have sexual intercourse occasionally.
4. If you have multiple sexual partners
Then if you have genital /uterine prolapse (when the uterus descends toward or into the vagina), you cannot use the female condom.\n
Do you understand"""
        dispatcher.utter_message(text=message, buttons=create_yes_or_no_button(), button_type="vertical")
        return []


class AskForSlotFemaleCondomShow(Action):
    def name(self) -> Text:
        return "action_ask_female_condom_show"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = """Ok, let me show you what a female condom looks like and how to use it.
        You can visit your nearest health shop to purchase
Female condoms are a barrier method of contraception worn inside the vagina. 
They are made of thin, soft plastic and have two ﬂexible rings – a removable ring at the closed end to help insertion and a fixed ring at the open end, which sits on the vulva to hold the condom in place. 
They prevent pregnancy by stopping sperm from meeting an egg. 
You can click to watch a video on how to insert and remove a female condom in Pidgin.
You can visit your nearest chemist/pharmacy to buy."""
        dispatcher.utter_message(text=message)
        return []


class AskForSlotAskMaleCondomExplanation(Action):
    def name(self) -> Text:
        return "action_ask_male_condom_explanation"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = """"""
        dispatcher.utter_message(text=message)
        return []


class AskForSlotMaleCondomDatabase(Action):
    def name(self) -> Text:
        return "action_ask_male_condom_database"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = """A condom is a thin covering that fits over a hard penis. It decreases the risk of pregnancy and sexually transmitted infections (STIs) by stopping sperm and body fluids from passing between partners.
You can click the audio to listen to how to insert a condom correctly in Pidgin if you want to.\n
Let me tell you some of the effective and available condoms.
Click on any of them to get their full details."""
        dispatcher.utter_message(text=message, buttons=create_button(["Kiss", "Fiesta", "Durex", "Trojan",
                                                                      "Gold Circle"]), button_type="vertical")
        return []


class ValidateRequest03MonthsForm(FormValidationAction):

    def name(self):
        return 'validate_request_0_3_months_form'

    def validate_daily_medical_conditions(self,
                                          slot_value: Any,
                                          dispatcher: CollectingDispatcher,
                                          tracker: Tracker,
                                          domain: DomainDict,
                                          ):
        print("in validate medical condition")
        print(slot_value)
        if slot_value.lower() == 'yes':
            dispatcher.utter_message(text="Ok, it is not advisable for you to take daily pills. "
                                          "Please speak to your doctor before using this method of contraceptive.")

        return {'daily_medical_conditions': slot_value}

    def validate_daily_contraceptive_database(self,
                                              slot_value: Any,
                                              dispatcher: CollectingDispatcher,
                                              tracker: Tracker,
                                              domain: DomainDict,
                                              ):

        print(f"in solt validate daily contraceptive database: {slot_value}")
        dispatcher.utter_message(text=get_database_message(slot_value))
        return {'daily_contraceptive_database': slot_value}

    def validate_emergency_contraceptive_database(self,
                                                  slot_value: Any,
                                                  dispatcher: CollectingDispatcher,
                                                  tracker: Tracker,
                                                  domain: DomainDict,
                                                  ):
        dispatcher.utter_message(text=get_database_message(slot_value))
        return {'emergency_contraceptive_database': slot_value}

    def validate_injectable_who_can_and_cannot_use_injectables(self,
                                                               slot_value: Any,
                                                               dispatcher: CollectingDispatcher,
                                                               tracker: Tracker,
                                                               domain: DomainDict,
                                                               ):
        if slot_value is not None:
            dispatcher.utter_message(text="Who cannot use\n"
                                          "1. If you are a breastfeeding mother from 6 weeks to 6 months postpartum.\n"
                                          "2. If you are a smoker and over 35 years old.\n"
                                          "3. If you have any of the following medical conditions, it is not "
                                          "advisable to take daily piils:\n "
                                          "a. Blood Pressure.\n"
                                          "b. Venous thromboembolism.\n"
                                          "c. Stroke.\n"
                                          "d. Heart Disease.\n"
                                          "e. Liver Disease.\n"
                                          "f. Breast Cancer.\n"
                                          "g. Diabetes.\n"
                                          "h. Vascular Disease.\n"
                                          "i. Vaginal bleeding")
            return {'injectable_who_can_and_cannot_use_injectables': slot_value}

    def validate_injectable_database(self,
                                     slot_value: Any,
                                     dispatcher: CollectingDispatcher,
                                     tracker: Tracker,
                                     domain: DomainDict,
                                     ):
        if slot_value is not None:
            dispatcher.utter_message(text=get_database_message(slot_value))

        return {'injectable_database': slot_value}

    def validate_male_condom_database(self,
                                     slot_value: Any,
                                     dispatcher: CollectingDispatcher,
                                     tracker: Tracker,
                                     domain: DomainDict,
                                     ):

        if slot_value is not None:
            dispatcher.utter_message(text=get_database_message(slot_value))

        return {'male_condom_database': slot_value}

    def validate_injectable_medical_conditions(self,
                                     slot_value: Any,
                                     dispatcher: CollectingDispatcher,
                                     tracker: Tracker,
                                     domain: DomainDict,
                                     ):
        if slot_value and slot_value.lower() == 'yes':
            dispatcher.utter_message(text=""""Ok, sorry about your medical condition but it is not advisable for you to adopt this method of contraception. 
            Please speak to your doctor before using this method of contraceptive.\n
            Do you understand? It is very important.""")

        return {'injectable_medical_conditions': slot_value}

    async def required_slots(
            self,
            domain_slots: List[Text],
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
    ) -> List[Text]:
        slot_mappings = {"Daily contraceptive pills": "daily",
                         "Emergency contraceptive pills": "emergency",
                         "Injectable contraceptives": "injectable",
                         "Diaphragm": "diaphragm",
                         "Female condom": "female",
                         "Male condom": "male"
                         }
        slots = domain_slots.copy()
        # print(f"Before calling required: {slots}")
        if get_slot_value(tracker, '0_3_months_method'):
            slots = required_slots(slots, slot_mappings.get(get_slot_value(tracker, '0_3_months_method'), "Dummy"))
        # print(f"After calling required: {slots}")
        if get_slot_value(tracker, 'daily_medical_conditions') == "Yes":
            slots.remove('daily_contraceptive_database')

        return slots

    async def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
    ) -> List[EventType]:
        print(f"value in run and value is prevent_pregnancy_time: {tracker.slots.get('prevent_pregnancy_time')}")
        if tracker.slots.get('prevent_pregnancy_time') != '0-3 months':
            return [ActiveLoop(None), SlotSet('requested_slot', None)]
        await super().run(dispatcher, tracker, domain)
