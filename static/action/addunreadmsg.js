export default function addUnreadMsg(chat_id){
	return{
		type:'ADD_UNREAD_MSG',
		chat_id
	};
}