import { useState, useEffect } from "react";
import axios from 'axios';

const DEFAULT_INTENTS_URL = "http://localhost:5000/intent"

/**
 * IntentEditForm Component
 * 
 * This component provides a form to edit an existing intent.
 * It allows users to update the `content` of an intent and submit it via a PATCH request.
 *  
 * @component
 * @param {Object} props - Component props
 * @param {Function} props.onIntentEdited - Callback called after successful edit to refresh parent data.
 * @param {string} props.idEditedIntent - The ID of the intent being edited.
 * @param {string} props.contentEditedIntent - The initial content of the intent to pre-fill the form.
 * @param {Function} props.setShowEditForm - Function to toggle the visibility of the edit form.
 */
const IntentEditForm = ({ onIntentEdited, idEditedIntent, contentEditedIntent, setShowEditForm }) => {
    const [content, setContent] = useState(contentEditedIntent);

    useEffect(() => {
        setContent(contentEditedIntent);
    }, [contentEditedIntent]);

    /**
     * Handles the edit submission of the intent.
     * 
     * @param {React.FormEvent} e - The form submission event
     */
    const handleSubmit = async (e) => {
        e.preventDefault();

        const intentData = {
            content
        };

        try {
            await axios.patch(DEFAULT_INTENTS_URL+"/"+idEditedIntent, intentData);
            onIntentEdited();
        } catch (error) {
            console.error("Error editing intent:", error);
        }
    };

    return (
        <div>
            <button onClick={() => setShowEditForm(false)}>➖ Cancel edit</button>
            <h2>Edit intent</h2>
            <h3>ID : {idEditedIntent}</h3>
            <form onSubmit={handleSubmit}>
                <input type="text" id="content" value={content} onChange={(e) => setContent(e.target.value)} placeholder="Content" required />
                <button type="submit">
                    Edit
                </button>
            </form>
        </div>
    );
};

export default IntentEditForm;