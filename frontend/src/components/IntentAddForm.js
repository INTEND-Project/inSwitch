import { useState } from "react";
import axios from 'axios';

const DEFAULT_INTENTS_URL = "http://localhost:5001/intent"

/**
 * IntentAddForm Component
 * 
 * This component provides a form to add an existing intent.
 * It allows users to add an intent and submit it via a POST request.
 *  
 * @component
 * @param {Object} props - Component props
 * @param {Function} props.onIntentAdded - Callback called after successful add to refresh parent data.
 */
const IntentAddForm = ({ onIntentAdded }) => {
    const [author, setAuthor] = useState('');
    const [content, setContent] = useState('');

    /**
     * Handles the form submission to add an intent.
     *
     * @param {React.FormEvent} e - The form submission event
     */
    const handleSubmit = async (e) => {
        e.preventDefault();

        const intentData = {
            author,
            content
        };

        try {
            await axios.post(DEFAULT_INTENTS_URL, intentData);
            onIntentAdded();
        } catch (error) {
            console.error("Error adding intent:", error);
        }
    };

    return (
        <div>
            <h2>Add an intent</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" id="author" value={author} onChange={(e) => setAuthor(e.target.value)} placeholder="Author" required />
                <input type="text" id="content" value={content} onChange={(e) => setContent(e.target.value)} placeholder="Content" required />
                <button type="submit">
                    Add
                </button>
            </form>
        </div>
    );
};

export default IntentAddForm;