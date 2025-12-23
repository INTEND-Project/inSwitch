# CONTROLLER
# Handles HTTP requests

from services import intent_service as service

from flask import jsonify, request, render_template

def register_routes(app):
    """
    Register all HTTP routes related to intent management in the Flask application.
    """

    # GET METHODS

    @app.get("/")
    def get_homepage():
        """
        Homepage displaying available API endpoints.

        Returns
        -------
        Response
            Rendered HTML template for the homepage.
        int
            HTTP status code.
        """
        return render_template('index.html')

    @app.get("/intent")
    def get_intents():
        """
        Function used to retrieve the list of intent.

        Returns
        -------
        JSON
            List of intents and their attributes.
        int
            HTTP status code.
        """
        try:
            intents = service.get_all_intents()
            if intents:
                return jsonify(intents), 200
            else:
                return '', 204
        except Exception as e:
            return str(e), 500 

    @app.get("/intent/json-ld")
    def get_intents_json_ld():
        """
        Function used to retrieve the list of intent as RDF in JSON-LD format.

        Returns
        -------
        JSON
            List of intents and their attributes as RDF in JSON-LD format.
        int
            HTTP status code.
        """
        try:
            intents = service.get_all_intents_json_ld()
            if intents:
                return jsonify(intents), 200
            else:
                return '', 204
        except Exception as e:
            return str(e), 500

    @app.get("/intent/<string:intent_id>")
    def get_intent_from_id(intent_id : str):
        """
        Function used to retrieve an intent from its ID.

        Parameters
        ----------
        intent_id : str
            The ID of the intent.

        Returns
        -------
        JSON
            An intent and its attributes.
        int
            HTTP status code.
        """
        try:
            intent = service.select_intent_from_id(intent_id)
            if intent:
                return jsonify(intent), 200
            else:
                return '', 204
        except Exception as e:
            return str(e), 500

    @app.get("/intent/<string:intent_id>/json-ld")
    def get_intent_json_ld_from_id(intent_id : str):
        """
        Function used to retrieve an intent from its ID as RDF in JSON-LD format.

        Parameters
        ----------
        intent_id : str
            The ID of the intent.

        Returns
        -------
        JSON
            An intent and its attributes as RDF in JSON-LD format.
        int
            HTTP status code.
        """
        try:
            intent = service.select_intent_json_ld_from_id(intent_id)
            if intent:
                return jsonify(intent), 200
            else:
                return '', 204
        except Exception as e:
            return str(e), 500
        

    # Intent Report

    @app.get("/intent/<string:intent_id>/intentReport")
    def get_intent_report_of_intent_id(intent_id : str):
        """
        Function used to retrieve the list of intent reports of an intent.

        Parameters
        ----------
        intent_id : str
            The ID of the intent.

        Returns
        -------
        JSON
            List of intent reports and their attributes.
        int
            HTTP status code.
        """
        try:
            intent_reports = service.get_all_intent_reports_of_intent(intent_id)
            if intent_reports:
                return jsonify(intent_reports), 200
            else:
                return '', 204
        except Exception as e:
            return str(e), 500

    @app.get("/intent/<string:intent_id>/intentReport/<string:report_id>")
    def get_intent_report_from_id_of_intent_id(intent_id : str, report_id : str):
        """
        Function used to retrieve an intent report of an intent from their IDs.

        Parameters
        ----------
        intent_id : str
            The ID of the intent.
        report_id :
            The ID of the intent report.

        Returns
        -------
        JSON
            An intent and its attributes.
        int
            HTTP status code.
        """
        try:
            intent_report = service.get_intent_report_of_intent(intent_id, report_id)
            if intent_report:
                return jsonify(intent_report), 200
            else:
                return '', 204
        except Exception as e:
            return str(e), 500


    # POST METHODS

    @app.post("/intent")
    def add_intent():
        """
        Function used to create a new intent.

        Returns
        -------
        JSON
            The intent with its intent report.
        int
            HTTP status code.
        """
        if request.is_json:
            try:
                added_intent = request.get_json()

                if "author" in added_intent and added_intent["author"] != "" and "content" in added_intent and added_intent["content"] != "":
                    intent_and_report = service.create_intent(added_intent["author"], added_intent["content"])

                    if not intent_and_report:
                        return {"error": "Error during adding a new intent"}, 415

                    return jsonify(intent_and_report), 201
                else:
                    return {"error": "The JSON request is not correct"}, 415
            except Exception as e:
                print(e)
                return str(e), 500
        else:
            return {"error": "Request must be JSON"}, 415
        

    # PATCH METHODS

    @app.patch("/intent/<string:intent_id>")
    def update_intent(intent_id : str):
        """
        Function used to update an existing intent.

        Parameters
        ----------
        intent_id : str
            The ID of the intent.

        Returns
        -------
        JSON
            The modified intent and its new intent report.
        int
            HTTP status code.
        """
        if request.is_json:
            updated_intent = request.get_json()

            if "content" in updated_intent and updated_intent["content"] != "":
                try:
                    intent_and_report = service.update_partially_intent(intent_id, updated_intent["content"])

                    if not intent_and_report:
                        return {"error": "Error during updating the intent"}, 415

                    return intent_and_report, 201
                except Exception as e:
                    return str(e), 500
            else:
                return {"error": "The JSON request is not correct"}, 415
        else:
            return {"error": "Request must be JSON"}, 415
            

    # DELETE METHODS

    @app.delete("/intent/<string:intent_id>")
    def delete_intent(intent_id : str):
        """
        Function used to delete an existing intent.

        Parameters
        ----------
        intent_id : str
            The ID of the intent.

        Returns
        -------
        JSON
            Message of deletion.
        int
            HTTP status code.
        """
        try:
            response = service.delete_intent_from_id(intent_id)
            if response:
                return jsonify({"message": "Intent deleted successfully"}), 200
            else:
                return jsonify({"error": "Error during the deletion of the intent."}), 500
        except Exception as e:
            return str(e), 500

    @app.delete("/intent/<string:intent_id>/intentReport/<string:report_id>")
    def delete_intent_report_from_intent(intent_id : str, report_id : str):
        """
        Function used to delete an existing intent report of an intent.

        Parameters
        ----------
        intent_id : str
            The ID of the intent.
        report_id : str
            The ID of the intent report.

        Returns
        -------
        JSON
            Message of deletion.
        int
            HTTP status code.
        """
        try:
            response = service.delete_report_from_id(intent_id, report_id)
            if response:
                return jsonify({"message": "Intent report deleted successfully"}), 200
            else:
                return jsonify({"error": "Error during the deletion of the intent report."}), 500
        except Exception as e:
            return str(e), 500