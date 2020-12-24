export default function changeActiveChat(chat_id){
	return{
		type:'CHANGE_ACTIVE_CHAT',
		chat_id
	};
}