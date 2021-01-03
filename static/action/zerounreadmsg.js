export default function zeroUnreadMsg(chat_id){
	return{
		type:'ZERO_UNREAD_MSG',
		chat_id
	};
}