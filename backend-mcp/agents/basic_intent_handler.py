
def handle_intent(intent, create_intent_report):

    try:
        intent_id = intent.get("id", None)
        content = intent.get("content", None)

        if not intent_id or not content:
            raise ValueError("Intent must have 'id' and 'content' fields.")

        # Process the intent (business logic can be added here)

        # Create an intent report if the flag is set
        if create_intent_report:
            report = create_intent_report(intent_id, f"I am tring to handle intent {intent_id} with content: {content}")
            return {"status": "success", "report": report}
        else:
            return {"status": "success", "message": "Intent processed without report."}


    except Exception as e:
        return {"status": "error", "message": str(e)}