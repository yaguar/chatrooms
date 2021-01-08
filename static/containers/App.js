import React from 'react';
import 'react-chat-elements/dist/main.css';
import { MessageBox, ChatItem, ChatList } from 'react-chat-elements';
import SearchField from "react-search-field";
import addMessage from '../action/addmessage';
import changeActiveChat from '../action/change_active_chat';
import rewriteMessages from '../action/rewritemessages';
import rewriteDialogs from '../action/rewritedialogs';
import upDialog from '../action/updialog';
import updateVisibleNewDialog from "../action/updatevisiblenewdialog";
import Input from '../components/Input';
import ModalNewDialog from '../components/modalNewDialog';
import DivSearchField from "../components/searchField";
import {connect} from "react-redux";
import deleteMessage from "../action/deletemessage";
import {store} from "../index";
import zeroUnreadMsg from "../action/zerounreadmsg";
import addUnreadMsg from "../action/addunreadmsg";
import rewriteMaybeUserForNewChat from '../action/rewritemaybeuserfornewchat';
import newDialog from '../action/newdialog'

class App extends React.Component {

    ws = new WebSocket('ws://' + window.location.host + '/ws')
    componentDidMount() {
        this.ws.onopen = () => {
            // on connecting, do nothing but log it to the console
            console.log('connected')
            let body = JSON.stringify({
                type: 'GET_CHATS',
                search: ''
            })
            this.ws.send(body)
        }
        this.ws.onmessage = evt => {
            let data = JSON.parse(evt.data)
            if (data['type'] == 'POST_MESSAGE') {
                this.props.addMsg(data, this.props.active_chat)
                if (this.props.active_chat != data['chat_id']) {
                    var audio = new Audio('static/media/getmsg.mp3');
                    audio.play();
                }
            } else if (data['type'] == 'GET_MESSAGES') {
                this.props.rewriteMsgsGet(JSON.parse(data['msgs']), this.props.active_chat)
            } else if (data['type'] == 'GET_CHATS') {
                this.props.rewriteDlg(JSON.parse(data['chats']))
            } else if (data['type'] == 'NEW_CHAT') {
                this.props.newDlg(JSON.parse(data['chat']))
            } else if (data['type'] == 'GET_LOGINS') {
                this.props.rewriteLogins(JSON.parse(data['logins']))
            }
        }
    };

    render () {
        return (
            <div className="row">
                <div className="col-sm-3" >
                    <br />
                    <DivSearchField updateVND={this.props.updateVND} websocket={this.ws}/>
                    <br />
                    <div className="panel-chat">
                        <div className="panel-body-chat">
                        {this.props.dialogs.map((dlg, index) => (
                            <div className={dlg.id === this.props.active_chat ? "border border-primary" : ""}>
                                <ChatItem
                                    avatar={'https://upload.wikimedia.org/wikipedia/commons/2/21/Che_Guevara_vector_SVG_format.svg'}
                                    alt={'Reactjs'}
                                    title={dlg.login}
                                    subtitle={'msg' in dlg ? dlg.msg : ''}
                                    unread={'unread' in dlg ? dlg.unread : 0}
                                    onClick={()=>this.props.rewriteMsgsPost(dlg.id, this.ws)}
                                    style={{color: 'red'}}
                                />
                            </div>
                        ))}
                        </div>
                    </div>
                </div>
                <ModalNewDialog
                    websocket={this.ws}
                    show={this.props.visible_new_dialog}
                    visible={this.props.updateVND}
                    maybe_users={this.props.maybe_users_for_new_chat}
                    users={this.props.users_for_new_chat}
                />
                <div className="col-sm-9" >
                    <br />
                    <div className="panel panel-primary">
                        <div className="panel-body">
                        {this.props.messages.map((msg, index) => (
                            <MessageBox
                                key={index}
                                position={msg.user === this.props.main_info.login ? 'right' : 'left'}
                                type={'text'}
                                text={msg.msg}
                                index={index}
                                title={msg.user}
                                date={new Date(msg.time)}
                            />
                        ))}
                        </div>
                    </div>
                    <br />
                    <div className="panel-footer">
                        <Input active_chat={this.props.active_chat} websocket={this.ws}/>
                    </div>
                </div>
            </div>
        );
    }
};

const mapDispatchToProps = (dispatch) => {
	return {
	    addMsg: (message, active_chat) => {
	        console.log(message, active_chat)
	        dispatch(upDialog(message))
	        if (active_chat == message['chat_id']) {
                dispatch(addMessage(message))
            } else {
	            dispatch(addUnreadMsg(message['chat_id']))
            }
        },
        updateVND: (visible) => {dispatch(updateVisibleNewDialog(visible))},
        rewriteLogins: (logins) => {dispatch(rewriteMaybeUserForNewChat(logins))},
        newDlg: (dialog) => {dispatch(newDialog(dialog))},
        rewriteDlg: (dialogs) => {dispatch(rewriteDialogs(dialogs))},
        rewriteMsgsGet: (messages) => {dispatch(rewriteMessages(messages))},
        rewriteMsgsPost: (chat_id, ws) => {
	        dispatch(zeroUnreadMsg(chat_id))
	        dispatch(changeActiveChat(chat_id))
            let body = JSON.stringify({
                    type: 'GET_MESSAGES',
                    chat_id: chat_id
                })
            ws.send(body)
	    }
	}
}

const mapStateToProps = (state) => {
	let props = {
		messages: state.messages.messages,
        dialogs: state.dialogs.dialogs,
        main_info: state.main_info.main_info,
        active_chat: state.active_chat.active_chat,
        visible_new_dialog: state.visible_new_dialog.visible_new_dialog,
        users_for_new_chat: state.users_for_new_chat.users_for_new_chat,
        maybe_users_for_new_chat: state.maybe_users_for_new_chat.maybe_users_for_new_chat
	};
	return props;
}

const mainApp = connect(
	mapStateToProps,
    mapDispatchToProps
)(App);

export default mainApp;
