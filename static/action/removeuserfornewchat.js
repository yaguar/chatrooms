export default function removeUserForNewChat(users_for_new_chat){
	return{
		type:'USERS_FOR_NEW_CHAT_REMOVE',
		users_for_new_chat
	};
}