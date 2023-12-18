from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import EventType, ActiveLoop, SlotSet, FollowupAction
from rasa_sdk.types import DomainDict
from actions.helper import *


class AskForSlot12YearsMethod(Action):
    def name(self) -> Text:
        return "action_ask_1_2_years_method"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = "You can use either the daily pills, the emergency pills, the injectables or the implants.\n" \
                  "Choose any them from the options to get the full details about them."
        buttons = create_button(['Daily contraceptive pills', 'Emergency contraceptive pills',
                                 'Injectable contraceptives', 'Contraceptive implants'])
        dispatcher.utter_message(text=message, buttons=buttons, button_type=VERTICAL_BUTTON_TYPE)
        return []


class AskForSlotImplantsAdvantage(Action):
    def name(self) -> Text:
        return "action_ask_implants_advantage"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = "Contraceptive implants are small, flexible rods inserted under the skin, " \
                  "typically in the arm. They release hormones (usually progestin) to prevent pregnancy. " \
                  "They are long-term birth control methods also called long-acting reversible contraception, " \
                  "or LARC. They provide contraception, lasting up to 3 - 5 years but can be removed at any time. " \
                  "They work by preventing the release of egg and thickening the cervical mucus making it " \
                  "difficult for sperm to reach the egg.\n" \
                  "Click to listen to a short explanation of implants in Pidgin, if you want to.\n" \
                  f"{create_hyper_link(url_description='Audio embedding (Implants)', url='https://drive.google.com/file/d/1_xdNkGpLTO-y3zWcJTMk7eRz7qTG-1a9/view?usp=drive_link')}\n" \
                  "Now let me tell you some of the advantages and disadvantages of contraceptive implants.\n" \
                  "Advantages\n" \
                  "1. They can be used at any time in the menstrual cycle, are very effective, and are removed whenever you want to get pregnant.\n" \
                  " 2. It gives total privacy, no one will know you have it and does not interfere with sex.\n" \
                  "3. No frequent clinical follow-up is needed after initial insertion.\n" \
                  "4. It is estrogen-free so many people can use it\n" \
                  "5. They are long-acting and may help prevent ectopic pregnancy.\n" \
                  "6. Does not disturb breast milk production.\n" \
                  "7. There is no delay in return to fertility when they are removed.\n" \
                  "Do you understand"
        dispatcher.utter_message(text=message)
        return []


class AskForSlotImplantsDisadvantage(Action):
    def name(self) -> Text:
        return "action_ask_implants_disadvantage"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = "Now to the disadvantages of contraceptive implants.\n" \
                  "Disadvantages\n" \
                  "1. Insertion and removal involve minor surgery and must be performed by a trained professional.\n" \
                  "2. You cannot discontinue the method by yourself.\n" \
                  "3. They might have some side effects such as:\n" \
                  "a. Headache.\n" \
                  "b. Nausea or vomiting.\n" \
                  "c. Dizziness.\n" \
                  "d. Breast tenderness.\n" \
                  "e. Weight gain.\n" \
                  "f. Menstrual changes.\n" \
                  "g. Spotting and irregular vaginal bleeding.\n" \
                  "Are you with me\n"
        dispatcher.utter_message(text=message, buttons=create_yes_or_no_button(), button_type='vertical')
        return []


class AskForSlotImplantsWhoCanAndCannotUse(Action):
    def name(self) -> Text:
        return "action_ask_implants_who_can_and_cannot_use"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = "On who can use and who cannot use implants.\n" \
                  "Who can use\n" \
                  "1. You can use an implant if you want to prevent pregnancy for up to 1 to 3 years.\n" \
                  "2. If you are a breastfeeding mother (from 6 weeks after birth)\n" \
                  "3. If you cannot estrogen.\n" \
                  "4. If you don't have migrainous headaches.\n" \
                  "5. If you have endometrial or ovarian cancer, you can still use this method.\n" \
                  "Do you get me"
        dispatcher.utter_message(text=message)
        return []


class AskForSlotImplantsMedicalCondition(Action):
    def name(self) -> Text:
        return "action_ask_implants_medical_condition"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = "So do you have any of the medical conditions listed?"
        buttons = create_button(["Yes", "No", "I don't know"])
        dispatcher.utter_message(text=message, buttons=buttons, button_type='vertical')
        return []


class AskForSlotImplantsDatabase(Action):
    def name(self) -> Text:
        return "action_ask_implants_database"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        message = "Let me tell you some of the effective and available contraceptive implants.\n" \
                  "Click on any of them to get their full details."
        buttons = create_button(["Levoplant", "Jadelle", "Implanon NXT"])
        dispatcher.utter_message(text=message, buttons=buttons, button_type='vertical')
        return []


class ValidateRequest02YearsForm(FormValidationAction):

    def name(self):
        return 'validate_request_1_2_years_form'

    def validate_implants_who_can_and_cannot_use(self,
                                                 slot_value: Any,
                                                 dispatcher: CollectingDispatcher,
                                                 tracker: Tracker,
                                                 domain: DomainDict,
                                                 ):
        if slot_value is not None:
            dispatcher.utter_message(text="Who cannot use\n"
                                          "You cannot use implants if you have any of the following medical "
                                          "conditions.\n "
                                          "a. Uncontrolled hypertension.\n"
                                          "b. Venous thromboembolism.\n"
                                          "c. Stroke.\n"
                                          "d. Heart Disease.\n"
                                          "e. Liver Disease.\n"
                                          "f. Breast Cancer.\n"
                                          "g. Kidney infection.\n"
                                          "h. Vaginal bleeding.")
        return {'implants_who_can_and_cannot_use': slot_value}

    def validate_implants_medical_condition(self,
                                            slot_value: Any,
                                            dispatcher: CollectingDispatcher,
                                            tracker: Tracker,
                                            domain: DomainDict,
                                            ):
        if slot_value and slot_value.lower() == 'yes':
            dispatcher.utter_message(text="Ok, sorry about your medical condition but it is not advisable "
                                          "for you to use contraceptive implants."
                                          " Please speak to your doctor before using this method of contraception.\n"
                                          "Do you understand? It is very important.")

        return {'implants_medical_condition': slot_value}

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
                         "Contraceptive implants": "implants",
                         }
        slots = domain_slots.copy()
        if get_slot_value(tracker, '1_2_years_method'):
            slots = required_slots(slots, slot_mappings.get(get_slot_value(tracker, '1_2_years_method'), "Dummy"))

        return slots

    async def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
    ) -> List[EventType]:
        print(f"value in run and value is prevent_pregnancy_time: {tracker.slots.get('prevent_pregnancy_time')}")
        if tracker.slots.get('prevent_pregnancy_time') != '1-2 years':
            return [ActiveLoop(None), SlotSet('requested_slot', None)]
        await super().run(dispatcher, tracker, domain)
