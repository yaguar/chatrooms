import React from 'react';
import { useFormik } from 'formik';
import Modal from 'react-bootstrap/Modal'
import Button from 'react-bootstrap/Button'
import SearchField from "react-search-field";
import Autosuggest from 'react-autosuggest';
import {store} from "../index";
import rewriteMaybeUserForNewChat from '../action/rewritemaybeuserfornewchat';
import addUserForNewChat from '../action/adduserfornewchat'
import {ChatItem, MessageBox} from "react-chat-elements";
import removeUserForNewChat from "../action/removeuserfornewchat";

const ModalNewDialog = (props) => {
    const formik = useFormik({
        initialValues: {
          chatName: '',
        },
        onSubmit: values => {
            values['users'] = props.users
            let url = '/new_chat'
        fetch(url, {
                method: 'post', headers: {
                    'Accept': 'application/json, text/plain, */*',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(values)
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
        },
  });

    const onChange = (value) => {
        let url = '/login_list?q=' + value
        fetch(url, {
                method: 'get', headers: {
                    'Accept': 'application/json, text/plain, */*',
                    'Content-Type': 'application/json'
                }
            })
            .then(
                function (response) {
                    if (response.status != 200) {
                        console.log('Looks like there was a problem. Status Code: ' +
                            response.status);
                        return 0;
                    }
                    response.json().then(function(data) {
                        store.dispatch(rewriteMaybeUserForNewChat(data))
                    });
                    return 1;
                }
            )
            .catch(function (err) {
                console.log('Fetch Error :-S', err);
            });
    }
    const onClickAdd = (user) => {
        store.dispatch(rewriteMaybeUserForNewChat([]))
        store.dispatch(addUserForNewChat(user))
    }
    const onClickRemove = (user) => {
        store.dispatch(removeUserForNewChat(user))
    }
    const handleClose = () => props.visible(false)
    return (
        <Modal show={props.show} onHide={handleClose}>
            <form onSubmit={formik.handleSubmit}>
        <Modal.Header closeButton>
            <Modal.Title>Создать чат</Modal.Title>
        </Modal.Header>
        <Modal.Body>
            {/*<span style={{position: "relative"}}>*/}
                <input
                    style={{width: "100%"}}
                    placeholder="Название чата"
                    id="chatName"
                    name="chatName"
                    type="text"
                    onChange={formik.handleChange}
                    value={formik.values.lastName}
                />

            <p></p>
            <SearchField onChange={onChange} className="modal" placeholder="Добавить человека"/>
            <p></p>
            <div style={{position: "relative"}}>
            <span>
                {props.users.map((user, index) => (
                    // <li key={index} onClick={() => onClickAdd(user)} className="list-group-item">{user.login}</li>
                    <ChatItem
                        key={index}
                        avatar={'https://upload.wikimedia.org/wikipedia/commons/2/21/Che_Guevara_vector_SVG_format.svg'}
                        alt={user.login}
                        title={user.login}
                        subtitle={''}
                        unread={0}
                        onClick={()=>{onClickRemove(user)}}
                    />
                ))}
            </span>
            <ul className="list-group" style={{position: "absolute", top:0,left:0, width: "100%"}}>
                {props.maybe_users.map((user, index) => (
                    <li key={index} onClick={() => onClickAdd(user)} className="list-group-item">{user.login}</li>
                ))}
            </ul></div>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Закрыть
          </Button>
          <Button type="submit" variant="primary">
            Создать чат
          </Button>
        </Modal.Footer>
            </form>
      </Modal>
    );
}

export default ModalNewDialog;