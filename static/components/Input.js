import React from 'react';
import {useFormik} from 'formik';


const Input = (props) => {
    const formik = useFormik({
        initialValues: {
            message: '',
        },
        onSubmit: values => {
            let body = JSON.stringify({
                    type: 'POST_MESSAGE',
                    message: values.message,
                    chat_id: props.active_chat
                })
            props.websocket.send(body)
            formik.resetForm();
        },
    });

    return (
        <form onSubmit={formik.handleSubmit} class="sticky-bottom">
            <div className="form-group">
                <textarea id="message" name="message" type="text" className="form-control input-sm chat_input"
                placeholder="Write your message here..." onChange = {formik.handleChange} value = {formik.values.message}/>
            </div>
            <button className="btn btn-primary" type="submit" onClick = {formik.handleSubmit}>Send</button>
        < /form>
    )
}

export default Input;