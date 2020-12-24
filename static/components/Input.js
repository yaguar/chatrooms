import React from 'react';
import {useFormik} from 'formik';


const Input = (props) => {
    const formik = useFormik({
        initialValues: {
            message: '',
        },
        onSubmit: values => {
            fetch('/messages', {
                method: 'post', headers: {
                    'Accept': 'application/json, text/plain, */*',
                    'Content-Type': 'application/json'
                }, body: JSON.stringify({
                    message: values.message,
                    chat_id: props.active_chat
                })
            })
                .then(
                    function (response) {
                        if (response.status != 200) {
                            console.log('Looks like there was a problem. Status Code: ' +
                                response.status);
                            return 0;
                        }

                        return 1;

                    }
                )
                .catch(function (err) {
                    console.log('Fetch Error :-S', err);
                });
            formik.resetForm();
        },
    });

    return (
        <form onSubmit={formik.handleSubmit} class="sticky-bottom">
            <div className="form-group">
                <textarea id="message" name="message" type="text" className="form-control input-sm chat_input"
                placeholder="Write your message here..." onChange = {formik.handleChange} value = {formik.values.message}></textarea>
            </div>
            <button className="btn btn-primary" type="submit" onClick = {formik.handleSubmit}>Send</button>
        < /form>
    );
}

export default Input;